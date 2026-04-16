"""
Feedback Generator Chatbot Module
Generates structured feedback based on domain and tone using rule-based templates.
Supports multiple domains and tones with varied, realistic outputs.
"""

import random


# --- Feedback Templates ---

TEMPLATES = {
    'hotel': {
        'positive': [
            "The hotel was absolutely wonderful! The rooms were spotless, the staff was incredibly friendly and attentive. The breakfast buffet had an amazing spread with fresh fruits and pastries. The pool area was beautiful and well-maintained. I would highly recommend this hotel to anyone visiting the area.",
            "What a fantastic stay! From check-in to check-out, everything was seamless. The concierge helped us plan amazing day trips. The room had a gorgeous view and the bed was incredibly comfortable. The restaurant served delicious local cuisine. Five stars all the way!",
            "Exceptional experience from start to finish. The lobby was elegant, the room was spacious and modern with all amenities. The spa services were top-notch and very relaxing. Staff remembered our names and preferences. Truly a premium hospitality experience.",
            "Our family had an amazing time at this hotel. Kids loved the pool and play area. The family suite was perfect with separate sleeping areas. Room service was quick and the food was delicious. Location was convenient for sightseeing. Will definitely return!",
            "The boutique hotel exceeded all expectations. Charming decor, personalized service, and attention to every detail. The rooftop bar had stunning views and creative cocktails. Breakfast was fresh and locally sourced. A hidden gem that deserves recognition."
        ],
        'negative': [
            "Terrible experience. The room was dirty with stains on the sheets and hair in the bathroom. The air conditioning didn't work properly and the WiFi kept disconnecting. Front desk staff was rude and unhelpful when we complained. Would never stay here again.",
            "Very disappointing stay. The hotel looks nothing like the photos online. Walls were thin and we could hear everything from neighboring rooms. The elevator was broken for two days. Breakfast options were very limited and stale. Not worth the price at all.",
            "The worst hotel I've ever stayed at. Found bugs in the room and the carpet was filthy. The hot water ran out constantly and towels were threadbare. The neighborhood felt unsafe and parking was overpriced. Management showed zero concern for our complaints.",
            "Do not stay here! Room smelled like smoke despite booking non-smoking. The mattress was lumpy and uncomfortable. Room service took over an hour. The pool was closed for maintenance with no prior notice. Complete waste of money.",
            "Horrible service and facilities. Check-in took 45 minutes. The bathroom had mold and the toilet was running all night. Noise from the bar downstairs made it impossible to sleep. Continental breakfast was just stale bread and bad coffee. Avoid this place."
        ],
        'neutral': [
            "The hotel was okay for the price. The room was clean but small. Location was decent with some restaurants nearby. Staff was polite but not particularly proactive. Nothing special but nothing terrible either. It served its purpose for a short stay.",
            "Average experience overall. The room was functional with basic amenities. Breakfast was standard continental fare. The gym was small but usable. Check-in was smooth. It's a decent option for budget travelers who just need a place to sleep.",
            "The hotel was adequate for a business trip. Room was clean and the WiFi worked well. The meeting rooms were well-equipped. Restaurant food was mediocre but convenient. Location was close to the convention center which was the main priority.",
            "Nothing remarkable about this stay. Clean room, working facilities, standard breakfast. The decor is a bit dated but everything functions properly. Staff was professional. It's a reliable mid-range option without any standout features.",
            "Decent hotel for the price point. Rooms are basic but well-maintained. The location is convenient for public transport. No major complaints but no wow factors either. Good enough for short stays when you need accessibility to the city center."
        ],
        'mixed': [
            "The hotel had a great location and beautiful lobby, but the rooms were smaller than expected. Staff at reception was very friendly, however the restaurant service was slow. The pool was nice but closed early. Good value for money despite some shortcomings.",
            "Mixed feelings about this stay. The suite was gorgeous with an amazing view, but the bathroom fixtures were outdated. Breakfast was excellent with lots of variety, but dinner at the hotel restaurant was overpriced and underwhelming. Would consider staying again at a discount.",
            "Some things were great, others not so much. The bed was incredibly comfortable and the room was quiet. However, the elevator was painfully slow and the parking situation was chaotic. The spa was wonderful but overbooked. A hotel with potential that needs consistency.",
            "The location and amenities were fantastic — rooftop pool, gym, and great bar. However, our room wasn't cleaned properly on the second day and maintenance was slow to fix the shower. When things worked, they were excellent. Inconsistency is the main issue.",
            "Beautiful property with some operational issues. The architecture and gardens are stunning. Room was well-designed. However, we experienced long wait times at check-in, the air conditioning was too noisy, and the WiFi was unreliable. Great bones but needs better management."
        ]
    },
    'college': {
        'positive': [
            "Excellent academic institution with dedicated faculty who genuinely care about student success. The campus is beautiful and well-maintained. Library resources are extensive and the career counseling center helped me land my dream internship. Highly recommend for serious students.",
            "The college transformed my career prospects completely. Professors are industry experts who bring real-world experience to the classroom. The lab facilities are state-of-the-art and the placement cell has strong connections with top companies. Best decision I ever made.",
            "Outstanding learning environment with a perfect balance of academics and extracurriculars. The entrepreneurship cell is very active and helped me start my own venture. Peer quality is excellent and the alumni network is incredibly supportive. World-class education.",
            "This college provides incredible value. Scholarship opportunities are abundant, faculty mentorship is personalized, and the research facilities rival top universities. The cultural festivals and tech fests are highlights of campus life. Truly a transformative experience.",
            "I had an amazing four years here. The curriculum is modern and regularly updated. International exchange programs broadened my perspective. Sports facilities are excellent and clubs cover every interest imaginable. The campus community is diverse and welcoming."
        ],
        'negative': [
            "Very disappointing academic experience. Most professors just read from slides and are unapproachable outside class. The syllabus is outdated and doesn't match industry requirements. Placement statistics are inflated and career support is minimal. Save your money.",
            "The college overpromises and underdelivers. Infrastructure is falling apart, labs have outdated equipment, and the library has limited books. Administration is bureaucratic and unresponsive. Hostel conditions are poor with frequent water and electricity issues.",
            "Terrible management and zero focus on student welfare. Attendance policies are unnecessarily strict, exam schedules are chaotic, and results take months. The canteen food is terrible and overpriced. No real extracurricular opportunities despite claims on the website.",
            "Worst educational investment I made. Faculty is underqualified and some teachers barely understand what they're teaching. No industry exposure, no workshops, no seminars. The degree is just a piece of paper with no real learning value. Deeply regret joining.",
            "Do not believe the brochure. The campus looks nothing like the photos. Classes are overcrowded, labs are shared between too many batches, and the fee keeps increasing without any improvements. Student complaints are ignored by the administration consistently."
        ],
        'neutral': [
            "The college is average in most respects. Some faculty members are good while others are mediocre. Infrastructure is functional but not impressive. Placements are decent for the top students but average for the rest. It gets the job done if you put in the effort.",
            "A standard educational institution. The curriculum covers the basics adequately. Some professors are engaging while others are not. Campus facilities are clean but nothing special. It's a reasonable choice if you're looking for an affordable degree in the region.",
            "Middle-of-the-road experience. Academic rigor varies by department — some are strong while others are weak. The campus has the essential facilities. Social life is okay with a few clubs and events throughout the year. Neither outstanding nor terrible.",
            "The college provides a basic education. Lab facilities are adequate for coursework requirements. Some elective courses are interesting. The placement process exists but isn't very aggressive. It's a safe, predictable choice without any major risks or rewards.",
            "Fair institution with room for improvement. Teaching quality is inconsistent across departments. Administrative processes are somewhat slow but functional. The college has a reasonably good reputation locally. Good enough for students who are self-motivated."
        ],
        'mixed': [
            "The college has excellent faculty in certain departments but others are severely lacking. Campus infrastructure is modern but maintenance is poor. Placements are great for CS and IT branches but weak for others. Very department-dependent experience overall.",
            "Some really great aspects mixed with frustrating ones. The research opportunities and lab access are excellent, but the administrative bureaucracy is maddening. Core courses are well-taught but electives are limited. Great potential held back by poor management.",
            "The academic experience was solid with some brilliant professors, but campus life was lacking. Limited hostel capacity, average canteen, and few recreational facilities. However, the industry collaborations and internship opportunities were genuinely valuable.",
            "Good college with notable highs and lows. The tech fest is nationally recognized and entrepreneurship support is strong. However, regular coursework feels monotonous and the examination system needs a complete overhaul. Strong extracurriculars compensate for academic gaps.",
            "Great peers and networking opportunities, but institutional support is inconsistent. Some departments have cutting-edge labs while others use equipment from a decade ago. Career services helped some students enormously but were slow for many others."
        ]
    },
    'app': {
        'positive': [
            "This app is a game-changer! The interface is incredibly intuitive and the features are exactly what I needed. Performance is smooth with zero lag. The developers clearly put thought into the user experience. Regular updates keep adding useful features. Best app in its category!",
            "Absolutely love this app. It has simplified my daily routine significantly. The design is clean and modern, navigation is seamless, and the sync across devices works perfectly. Customer support responded within hours when I had a question. Five stars well deserved.",
            "Outstanding application that exceeds expectations. The AI-powered features are surprisingly accurate and save me hours of work. The premium subscription is totally worth it for the advanced analytics. No crashes, no bugs, just a polished product. Highly recommended!",
            "This app is exactly what I've been looking for. Easy setup, beautiful UI, and packed with features. The offline mode is a lifesaver when traveling. Data export options are comprehensive. The development team is very responsive to feature requests. A top-tier experience.",
            "Impressive app with attention to detail. Dark mode looks gorgeous, animations are smooth, and the widget support is perfect. Battery usage is minimal which is impressive given the functionality. Privacy controls are transparent and thorough. A model for how apps should be built."
        ],
        'negative': [
            "Terrible app that crashes constantly. Lost all my data twice. The UI is confusing and cluttered with unnecessary features. Customer support is non-existent — sent three emails with no response. And now they want a subscription for basic features? Uninstalling immediately.",
            "This app is a disaster. It drains my battery in hours and uses way too much storage. Push notifications are excessive and annoying even after adjusting settings. The latest update broke core functionality. Feels like a beta product being sold as finished.",
            "Do not download this app. It's full of ads that pop up every few seconds. The free version is basically unusable and the premium version is overpriced for what you get. Performance is sluggish and the interface looks like it was designed in 2010.",
            "Worst app experience I've had. Registration requires too much personal information, the permissions requested are invasive, and the privacy policy is concerning. Features advertised in the store listing don't actually exist. This feels like a scam app.",
            "Incredibly frustrating app. Search function barely works, filters are unreliable, and data frequently fails to sync. Customer service only sends automated responses. Three months of bug reports and nothing gets fixed. Moving to a competitor immediately."
        ],
        'neutral': [
            "The app works fine for basic tasks. Interface is clean enough but nothing groundbreaking. It does what it says it does without any extras. Loading times are acceptable. Free version has limitations but is functional for casual users. A decent utility app.",
            "It's an okay app. Gets the job done for what I need. Some features are useful, others I never touch. No major bugs but the performance could be snappier. Updates are infrequent but they seem to fix things when they come. Average overall.",
            "Standard app in its category. Works as expected with no surprises good or bad. The UI is functional but could use a design refresh. Notifications work properly and settings are straightforward. It's a reliable choice if you don't need anything fancy.",
            "The app serves its purpose adequately. Not the most feature-rich option available but stability is good. Data syncing is reliable. The user interface is basic but easy to navigate. Free tier is limited but the pricing is reasonable for premium.",
            "Middle-of-the-pack app. Has the essential features you'd expect without any standout functionality. Performance is consistent and there are rarely any issues. Could benefit from better customization options. Suitable for users with basic requirements."
        ],
        'mixed': [
            "The app has amazing features but the execution is inconsistent. The AI recommendations are spot-on but the app randomly crashes during intensive tasks. Beautiful design on iOS but the Android version looks rushed. Great concept that needs more polish.",
            "Love the core functionality but hate the monetization model. The best features are locked behind an expensive subscription. The free version is good enough to show you what you're missing but frustrating to use daily. Wish there was a one-time purchase option.",
            "Great potential with some annoying issues. Photo editing tools are excellent and filters are creative. However, export quality is sometimes lower than expected and the app occasionally freezes. Cloud backup is seamless though. Worth using despite the quirks.",
            "The app excels in some areas and fails in others. Task management is intuitive and the calendar integration is perfect. But collaboration features are clunky and file sharing is unreliable. Solo users will love it; teams might struggle.",
            "Solid app with room for improvement. The core experience is smooth and the design is modern. However, battery consumption is higher than competitors and some advanced features have a steep learning curve. Good customer support partially offsets the frustrations."
        ]
    },
    'product': {
        'positive': [
            "Absolutely amazing product! The build quality is outstanding and it performs exactly as advertised. Setup was effortless and the design is sleek and modern. After three months of daily use, it still works like new. Best purchase I've made this year without a doubt.",
            "Exceeded all my expectations. The attention to detail in the design is impressive. It's durable, functional, and looks great. The instruction manual was clear and setup took minutes. Customer service was extremely helpful when I had a pre-purchase question. Worth every penny.",
            "Premium quality product that justifies the price. The materials feel luxurious and the craftsmanship is evident. It outperforms competing products I've tried in the past. The warranty and return policy gave me confidence to buy. Highly recommend to anyone considering it.",
            "This product is a must-have. It solved a problem I've been struggling with for months. The innovative design makes daily use effortless. Energy efficient and quiet operation. Packaging was eco-friendly and the unboxing experience was delightful. Five stars!",
            "Incredible value for money. The features you get at this price point are unmatched. Build quality rivals products twice the cost. Easy maintenance and impressive durability. Quick shipping and secure packaging. I've already recommended it to friends and family."
        ],
        'negative': [
            "Complete waste of money. The product broke within a week of normal use. Cheap materials and poor construction quality throughout. The description online was misleading about the size and capabilities. Return process was complicated and customer service was unhelpful.",
            "Very disappointed with this purchase. The product doesn't perform as advertised. It's loud, it overheats, and the finish is already scratching after minimal use. Instructions were poorly written and missing steps. Expected much better at this price range.",
            "Terrible product quality. Arrived with a visible defect and when I contacted support, they blamed the shipping company. The replacement was slightly better but still felt cheaply made. Features are limited compared to what's listed. Would not recommend to anyone.",
            "Do not buy this product. It looks nothing like the pictures. The color is completely off, the material feels flimsy, and it's much smaller than indicated. Started malfunctioning after two weeks. No response from the company after filing a complaint.",
            "Worst purchase ever. The product is poorly designed with obvious ergonomic issues. Gets extremely hot during use which is a safety concern. The accessories included are cheap and barely functional. Returned it and got a competitor's product which works perfectly."
        ],
        'neutral': [
            "The product is acceptable for the price. It works as described without any special features. Build quality is decent but not premium. Does what it needs to do. Packaging was standard. If you need a basic option without frills, this will do.",
            "Average product overall. Functions correctly and looks okay. Nothing about it stands out positively or negatively. Setup was straightforward. Durability seems reasonable based on a month of use. A safe, unremarkable purchase.",
            "Gets the job done but nothing more. The product is functional and reliable for basic needs. Design is simple and utilitarian. Price is fair for what you get. No complaints but no enthusiasm either. A practical choice.",
            "Standard product in its category. Quality matches the price point appropriately. Performance is consistent and predictable. The design is dated but functional. Would be great if it had a couple more features but it covers the basics well.",
            "Meets basic expectations. The product arrived on time and works as described. It's neither impressive nor disappointing. Materials are okay and the construction seems durable enough. Fair value for a budget-friendly option."
        ],
        'mixed': [
            "The product has excellent features but the build quality doesn't match the premium price. The technology inside is impressive and performance is great, but the plastic casing feels cheap and the buttons are wobbly. Functionally great, aesthetically disappointing.",
            "Great product with some notable drawbacks. The core functionality is top-notch and the design is creative. However, the battery life is shorter than advertised and the charging cable is proprietary which is inconvenient. Would buy again but with adjusted expectations.",
            "Love the concept, mixed on execution. The innovative features are genuinely useful and set it apart from competitors. But reliability is inconsistent — works perfectly most days but occasionally glitches. Customer support is responsive which helps offset the issues.",
            "Good product held back by poor accessories. The main unit is well-built and performs excellently. But the included accessories are clearly cheap afterthoughts. Had to buy third-party replacements. The core product deserves five stars but the total package gets three.",
            "Impressive in many ways but not without flaws. The design is beautiful and ergonomic. Setup was intuitive. However, the companion app is buggy and some advertised features require a separate subscription. The hardware is five stars; the software ecosystem is two."
        ]
    },
    'restaurant': {
        'positive': [
            "An absolutely delightful dining experience! The food was exquisitely prepared with fresh ingredients you can taste in every bite. The ambiance was warm and inviting with beautiful decor. Our server was knowledgeable about the menu and made excellent recommendations. Will definitely return!",
            "Best restaurant I've been to in months. The chef's special was outstanding — creative flavor combinations that actually worked. Portions were generous and well-presented. The wine selection complemented the menu perfectly. Reasonable prices for the quality. A must-visit!",
            "Exceptional food and service from start to finish. The appetizers were creative, the main courses were perfectly cooked, and the desserts were divine. The restaurant has a wonderful atmosphere with soft lighting and great music. Perfect for both date nights and family dinners.",
            "What a gem of a restaurant! Every dish was burst of flavors. The patio seating was lovely with beautiful garden views. Staff was attentive and friendly without being intrusive. The farm-to-table concept is executed brilliantly. Booking again this weekend!",
            "Outstanding culinary experience. The tasting menu was a journey through incredible flavors. Each course was thoughtfully paired with wines. The kitchen is clearly passionate about their craft. Impeccable presentation and perfect timing between courses. Fine dining at its best."
        ],
        'negative': [
            "Terrible dining experience. Waited 30 minutes for a table despite having a reservation. The food was cold and tasteless. Found a hair in my soup and the manager barely apologized. The restaurant was dirty and the restroom was disgusting. Never coming back.",
            "Highly overrated and overpriced. The portions were tiny and the food was mediocre at best. Pasta was overcooked, salad was wilted, and the bread was stale. Service was painfully slow and our waiter was dismissive. A complete waste of money.",
            "Worst restaurant experience ever. The menu had limited options and most items were unavailable. What we did order was bland and poorly seasoned. The kitchen took over an hour for two simple dishes. The bill had unexplained charges. Absolutely terrible.",
            "Do not eat here. The hygiene standards are questionable — saw kitchen staff without gloves handling food. The dining area had sticky tables and uncomfortable seating. Food was obviously reheated and lacked freshness. The prices are outrageous for what you get.",
            "Disappointing on every front. The restaurant is loud and cramped. The menu descriptions are misleading — dishes look nothing like described. My steak was overcooked despite ordering medium-rare. Dessert was clearly store-bought. Service felt rushed to turn tables."
        ],
        'neutral': [
            "Decent restaurant with standard fare. The food was cooked well enough but nothing memorable. The atmosphere is casual and comfortable. Prices are fair for the area. Service was adequate. A reliable option when you need a meal but aren't looking for anything special.",
            "Average dining experience. The menu has a good variety of options. Food quality is consistent and satisfactory. Nothing blew us away but nothing disappointed either. Wait times were reasonable and the staff was polite. A standard neighborhood restaurant.",
            "The restaurant is okay for a casual lunch. Portions are moderate and the food is decently prepared. The decor is simple and clean. Our order was accurate and arrived in a reasonable time. Prices are moderate. Fine for a quick meal, not for special occasions.",
            "Standard restaurant experience. Some dishes are better than others but overall quality is average. The location is convenient and seating is comfortable. Dessert menu is limited. Service is professional if somewhat impersonal. Gets three out of five stars.",
            "Functional restaurant with predictable quality. The everyday menu items are reliable. Weekend specials can sometimes be surprisingly good. The bar area is pleasant for casual drinks. Nothing remarkable but consistently adequate. A safe, known quantity."
        ],
        'mixed': [
            "The restaurant has amazing food but terrible service. Every dish was beautifully presented and flavorful, but our waiter was neglectful and the wait times were excessive. The atmosphere is lovely but it's hard to enjoy when you're constantly flagging down staff.",
            "Beautiful ambiance and great cocktails, but the food didn't match. The interior design is stunning with incredible attention to detail. Drinks were creative and delicious. However, entrees were underseasoned and overpriced. Great for drinks, not for dinner.",
            "Hit or miss experience. The appetizers and starters were excellent — creative and well-executed. But main courses were inconsistent in quality. The seafood was fresh but the meat dishes were tough. Desserts redeemed the meal somewhat. Uneven but has potential.",
            "Great food, poor value. The dishes are genuinely delicious and use high-quality ingredients. But the portions are extremely small for the prices charged. Add drinks and dessert and the bill becomes astronomical. Worth visiting once for the experience but not regularly.",
            "Loved the concept, had some issues with execution. The fusion menu is creative and most flavor combinations work well. However, some dishes were too experimental and missed the mark. Service was friendly but clearly understaffed. A restaurant with great ideas that needs refinement."
        ]
    },
    'service': {
        'positive': [
            "Exceptional customer service from start to finish. The team was professional, responsive, and genuinely cared about solving my issue. They went above and beyond what was expected. The follow-up call to ensure satisfaction was a nice touch. Will recommend to everyone.",
            "Outstanding service experience. The technician arrived on time, explained everything clearly, and completed the work efficiently. The pricing was transparent with no hidden fees. The quality of work exceeded expectations. This is how service should be done.",
            "Best customer service I've experienced in years. Support team resolved my complex issue within hours. They were patient, knowledgeable, and kept me informed throughout the process. The online portal is user-friendly and the mobile app works great. Truly impressed.",
            "Five-star service all around. From the initial consultation to the final delivery, every interaction was professional and pleasant. The team was flexible with scheduling and delivered ahead of deadline. Pricing was competitive and the quality was premium. Highly recommended.",
            "Incredible service that restored my faith in customer care. The representative understood my frustration and took ownership of the problem. Resolution was quick and they added a courtesy discount for the inconvenience. Proactive, empathetic, and effective. The gold standard."
        ],
        'negative': [
            "Absolutely terrible service. Waited on hold for over an hour only to be transferred three times. The representative was rude and dismissive. My issue still isn't resolved after two weeks and multiple calls. They clearly don't care about their customers.",
            "The worst service experience imaginable. Missed two scheduled appointments without any notification. When the technician finally showed up, they didn't have the right parts. Charged me a service fee for literally nothing being accomplished. Avoid at all costs.",
            "Horrible customer support system. The chatbot is useless, email responses are automated and irrelevant, and the phone line has ridiculous wait times. When I finally spoke to someone, they had no authority to help. A masterclass in how to frustrate customers.",
            "Do not use this service. They completely botched the job and then refused to take responsibility. The work was substandard and needed to be redone by another provider at additional cost. Getting a refund has been a nightmare involving multiple complaints.",
            "Deeply unsatisfied with the service received. The team was unprofessional, showing up late and leaving a mess. Communication throughout was poor with contradictory information from different representatives. Pricing ended up being significantly higher than the original quote."
        ],
        'neutral': [
            "Standard service delivery. The job was done adequately within the expected timeframe. Communication was basic but sufficient. Pricing was in line with market rates. No issues to report but nothing particularly impressive either. A satisfactory experience.",
            "Average service experience. The representative was polite and followed the standard process. Resolution took the expected amount of time. The outcome met basic expectations. Nothing went wrong but there was no extra effort either. Acceptable overall.",
            "The service was functional and met the basic requirements. Scheduling was straightforward and the team showed up as planned. The work was completed to an acceptable standard. Documentation was provided as expected. A routine, unremarkable service call.",
            "Decent service at a fair price. The technician was competent and completed the work without issues. Communication was professional if somewhat minimal. The process was smooth and straightforward. A reliable option for standard service needs.",
            "The service did what it was supposed to do. No frills, no surprises, no complaints. Wait times were reasonable, the staff was professional, and the result was satisfactory. It's a middle-of-the-road provider that delivers consistent, if unspectacular, results."
        ],
        'mixed': [
            "The service quality was excellent but the customer experience was lacking. The actual work performed was top-notch and professional. However, scheduling was a nightmare, communication was inconsistent, and billing had errors. Great at the core service, bad at everything around it.",
            "Mixed experience with this provider. The initial consultation was impressive — thorough and transparent. But the actual service delivery was delayed repeatedly and quality was lower than what was demonstrated. Post-service support has been responsive though. Inconsistent overall.",
            "Good service with some frustrating aspects. The team is clearly skilled and the end result was satisfying. However, the process of getting there was stressful — poor time estimates, scope changes, and additional costs that weren't discussed initially. End result saves it.",
            "The front-line staff is wonderful — helpful, knowledgeable, and caring. But the back-end systems and management are problematic. Billing errors are frequent, appointment confirmations don't always come through, and procedures keep changing. Good people hampered by bad systems.",
            "Solid service quality marred by poor communication. The actual technical work was excellent and resolved our issue completely. But getting updates required constant follow-up from our side, and the project timeline wasn't communicated clearly. Would use again but with managed expectations."
        ]
    }
}


def generate_feedback(domain: str = 'hotel', tone: str = 'positive') -> dict:
    """
    Generate feedback based on domain and tone.
    
    Args:
        domain: One of 'hotel', 'college', 'app', 'product', 'restaurant', 'service'
        tone: One of 'positive', 'negative', 'neutral', 'mixed'
    
    Returns:
        Dictionary with generated feedback, domain, and tone.
    """
    domain = domain.lower().strip()
    tone = tone.lower().strip()

    available_domains = list(TEMPLATES.keys())
    available_tones = ['positive', 'negative', 'neutral', 'mixed']

    if domain not in available_domains:
        domain = 'hotel'
    if tone not in available_tones:
        tone = 'positive'

    feedbacks = TEMPLATES[domain][tone]
    selected = random.choice(feedbacks)

    return {
        'feedback': selected,
        'domain': domain,
        'tone': tone,
        'available_domains': available_domains,
        'available_tones': available_tones
    }


def get_available_options() -> dict:
    """Return available domains and tones."""
    return {
        'domains': list(TEMPLATES.keys()),
        'tones': ['positive', 'negative', 'neutral', 'mixed']
    }
