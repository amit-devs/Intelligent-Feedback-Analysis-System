"""
Sentiment Analysis Module
Uses VADER (Valence Aware Dictionary and sentiment Reasoner) for sentiment analysis.
Provides preprocessing, sentiment scoring, and classification.
"""

import re
import string
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- NLTK Stopwords (embedded to avoid download issues) ---
STOP_WORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
    "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
    'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
    'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
    'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because',
    'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
    'between', 'through', 'during', 'before', 'after', 'above', 'below', 'to',
    'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
    'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
    'all', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
    'nor', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
    'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd',
    'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't",
    'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',
    "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
}

analyzer = SentimentIntensityAnalyzer()


def preprocess_text(text: str) -> str:
    """
    Preprocess text: lowercase, remove punctuation, strip extra whitespace.
    """
    text = text.lower().strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text)
    return text


def remove_stopwords(text: str) -> str:
    """Remove stopwords from text."""
    words = text.split()
    filtered = [w for w in words if w not in STOP_WORDS]
    return ' '.join(filtered)


def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment of the given text.
    Returns sentiment label, compound score, and detailed scores.
    """
    if not text or not text.strip():
        return {
            'label': 'Neutral',
            'score': 0.0,
            'details': {'pos': 0.0, 'neu': 1.0, 'neg': 0.0, 'compound': 0.0}
        }

    # VADER works best on raw text (it uses punctuation and casing)
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']

    if compound >= 0.05:
        label = 'Positive'
    elif compound <= -0.05:
        label = 'Negative'
    else:
        label = 'Neutral'

    return {
        'label': label,
        'score': round(compound, 4),
        'details': {
            'pos': round(scores['pos'], 4),
            'neu': round(scores['neu'], 4),
            'neg': round(scores['neg'], 4),
            'compound': round(compound, 4)
        }
    }


def extract_keywords(text: str, top_n: int = 8) -> list:
    """
    Extract top keywords from text by frequency (after preprocessing).
    """
    cleaned = preprocess_text(text)
    cleaned = remove_stopwords(cleaned)
    words = cleaned.split()

    freq = {}
    for w in words:
        if len(w) > 2:
            freq[w] = freq.get(w, 0) + 1

    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words[:top_n]]
