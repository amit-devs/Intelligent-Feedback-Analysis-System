"""
Intelligent Feedback Analysis System - Flask Application
Main application server with REST API endpoints.
"""

import json
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from sentiment import analyze_sentiment, extract_keywords
from ai_detector import detect_ai
from chatbot import generate_feedback, get_available_options
from summarizer import summarize_feedback

app = Flask(__name__)
CORS(app)

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')


def load_data() -> list:
    """Load feedback data from JSON file."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_data(data: list):
    """Save feedback data to JSON file."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# --- Routes ---

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze feedback text.
    Input: { "text": "feedback text" }
    Output: sentiment analysis + AI detection results
    """
    data = request.get_json()
    if not data or not data.get('text', '').strip():
        return jsonify({'error': 'Please provide feedback text.'}), 400

    text = data['text'].strip()

    # Sentiment analysis
    sentiment_result = analyze_sentiment(text)

    # AI detection
    ai_result = detect_ai(text)

    # Keyword extraction
    keywords = extract_keywords(text)

    # Store in data
    entry = {
        'id': len(load_data()) + 1,
        'text': text,
        'sentiment': sentiment_result['label'],
        'score': sentiment_result['score'],
        'details': sentiment_result['details'],
        'ai_detection': ai_result['classification'],
        'ai_confidence': ai_result['confidence'],
        'ai_features': ai_result['features'],
        'ai_explanation': ai_result['explanation'],
        'keywords': keywords,
        'timestamp': datetime.now().isoformat()
    }

    feedbacks = load_data()
    feedbacks.append(entry)
    save_data(feedbacks)

    return jsonify({
        'success': True,
        'sentiment': sentiment_result,
        'ai_detection': ai_result,
        'keywords': keywords,
        'entry': entry
    })


@app.route('/generate', methods=['POST'])
def generate():
    """
    Generate feedback using the chatbot.
    Input: { "domain": "hotel", "tone": "positive" }
    Output: generated feedback text
    """
    data = request.get_json()
    domain = data.get('domain', 'hotel') if data else 'hotel'
    tone = data.get('tone', 'positive') if data else 'positive'

    result = generate_feedback(domain, tone)

    return jsonify({
        'success': True,
        'result': result
    })


@app.route('/stats', methods=['GET'])
def stats():
    """
    Get analytics and statistics.
    Output: summary, charts data, insights, alerts
    """
    feedbacks = load_data()
    summary = summarize_feedback(feedbacks)

    # Prepare chart data
    sentiment_distribution = {
        'labels': ['Positive', 'Negative', 'Neutral'],
        'data': [summary.get('positive', 0), summary.get('negative', 0), summary.get('neutral', 0)],
        'colors': ['#10B981', '#EF4444', '#F59E0B']
    }

    # Feedback trend over time (group by date)
    trend_data = _build_trend_data(feedbacks)

    return jsonify({
        'success': True,
        'summary': summary,
        'sentiment_distribution': sentiment_distribution,
        'trend_data': trend_data
    })


@app.route('/history', methods=['GET'])
def history():
    """
    Get feedback history.
    Output: list of all feedback entries (most recent first)
    """
    feedbacks = load_data()
    feedbacks.reverse()
    return jsonify({
        'success': True,
        'feedbacks': feedbacks,
        'total': len(feedbacks)
    })


@app.route('/clear', methods=['POST'])
def clear():
    """Clear all stored feedback data."""
    save_data([])
    return jsonify({'success': True, 'message': 'All feedback data cleared.'})


@app.route('/options', methods=['GET'])
def options():
    """Get available chatbot options."""
    return jsonify({
        'success': True,
        'options': get_available_options()
    })


def _build_trend_data(feedbacks: list) -> dict:
    """Build trend chart data grouped by date."""
    if not feedbacks:
        return {'labels': [], 'positive': [], 'negative': [], 'neutral': []}

    date_groups = {}
    for f in feedbacks:
        ts = f.get('timestamp', '')
        date = ts[:10] if ts else 'Unknown'
        if date not in date_groups:
            date_groups[date] = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
        sentiment = f.get('sentiment', 'Neutral')
        if sentiment in date_groups[date]:
            date_groups[date][sentiment] += 1

    sorted_dates = sorted(date_groups.keys())

    return {
        'labels': sorted_dates,
        'positive': [date_groups[d]['Positive'] for d in sorted_dates],
        'negative': [date_groups[d]['Negative'] for d in sorted_dates],
        'neutral': [date_groups[d]['Neutral'] for d in sorted_dates]
    }


if __name__ == '__main__':
    app.run(debug=True, port=5000)
