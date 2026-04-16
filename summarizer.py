"""
Feedback Summarization Module
Generates insights, key themes, keyword extraction, and alert detection
from a collection of feedback entries.
"""

from collections import Counter
from sentiment import analyze_sentiment, extract_keywords, preprocess_text, remove_stopwords


def summarize_feedback(feedbacks: list) -> dict:
    """
    Generate a comprehensive summary from a list of feedback entries.
    
    Args:
        feedbacks: List of dicts with at least 'text', 'sentiment', 'score' keys.
    
    Returns:
        Dictionary with summary statistics, insights, keywords, and alerts.
    """
    if not feedbacks:
        return {
            'total': 0,
            'positive_pct': 0,
            'negative_pct': 0,
            'neutral_pct': 0,
            'avg_score': 0,
            'insights': ['No feedback data available yet.'],
            'top_keywords': [],
            'alerts': [],
            'trend': 'stable'
        }

    total = len(feedbacks)
    positive = sum(1 for f in feedbacks if f.get('sentiment') == 'Positive')
    negative = sum(1 for f in feedbacks if f.get('sentiment') == 'Negative')
    neutral = sum(1 for f in feedbacks if f.get('sentiment') == 'Neutral')

    scores = [f.get('score', 0) for f in feedbacks]
    avg_score = round(sum(scores) / len(scores), 4) if scores else 0

    positive_pct = round((positive / total) * 100, 1)
    negative_pct = round((negative / total) * 100, 1)
    neutral_pct = round((neutral / total) * 100, 1)

    # Keyword extraction from all feedback
    all_text = ' '.join(f.get('text', '') for f in feedbacks)
    top_keywords = extract_keywords(all_text, top_n=10)

    # Extract keywords from negative feedback specifically
    negative_texts = ' '.join(f.get('text', '') for f in feedbacks if f.get('sentiment') == 'Negative')
    complaint_keywords = extract_keywords(negative_texts, top_n=5) if negative_texts else []

    # Generate insights
    insights = _generate_insights(
        total, positive, negative, neutral,
        positive_pct, negative_pct, neutral_pct,
        avg_score, top_keywords, complaint_keywords
    )

    # Alert detection
    alerts = _detect_alerts(negative_pct, avg_score, feedbacks)

    # Trend analysis (simple: based on recent vs older)
    trend = _analyze_trend(feedbacks)

    return {
        'total': total,
        'positive': positive,
        'negative': negative,
        'neutral': neutral,
        'positive_pct': positive_pct,
        'negative_pct': negative_pct,
        'neutral_pct': neutral_pct,
        'avg_score': avg_score,
        'insights': insights,
        'top_keywords': top_keywords,
        'complaint_keywords': complaint_keywords,
        'alerts': alerts,
        'trend': trend
    }


def _generate_insights(total, positive, negative, neutral,
                        pos_pct, neg_pct, neu_pct,
                        avg_score, keywords, complaint_kw):
    """Generate human-readable insights from statistics."""
    insights = []

    # Overall sentiment insight
    if pos_pct > 60:
        insights.append(f"Overall sentiment is strongly positive ({pos_pct}% positive feedback). Users are generally satisfied with the experience.")
    elif pos_pct > 40:
        insights.append(f"Sentiment is moderately positive ({pos_pct}% positive). There's room for improvement but the overall reception is favorable.")
    elif neg_pct > 50:
        insights.append(f"⚠️ Majority of feedback is negative ({neg_pct}%). Immediate attention is needed to address user concerns.")
    elif neg_pct > 30:
        insights.append(f"A significant portion of feedback is negative ({neg_pct}%). Consider investigating common complaint themes.")
    else:
        insights.append(f"Feedback sentiment is mixed — {pos_pct}% positive, {neg_pct}% negative, {neu_pct}% neutral.")

    # Score-based insight
    if avg_score > 0.5:
        insights.append(f"Average sentiment score of {avg_score} indicates strong positive reception.")
    elif avg_score > 0:
        insights.append(f"Average sentiment score of {avg_score} suggests a slightly positive but cautious reception.")
    elif avg_score < -0.3:
        insights.append(f"Average sentiment score of {avg_score} signals widespread dissatisfaction that needs addressing.")
    elif avg_score < 0:
        insights.append(f"Average sentiment score of {avg_score} leans slightly negative — user satisfaction could be improved.")

    # Keyword-based insights
    if keywords:
        kw_str = ', '.join(keywords[:5])
        insights.append(f"Most discussed topics: {kw_str}.")

    if complaint_kw:
        ckw_str = ', '.join(complaint_kw[:3])
        insights.append(f"Top complaint themes: {ckw_str}. These areas should be prioritized for improvement.")

    # Volume insight
    if total >= 20:
        insights.append(f"With {total} feedback entries, the data provides a reliable statistical overview.")
    elif total >= 5:
        insights.append(f"Based on {total} feedback entries. A larger sample may reveal additional patterns.")
    else:
        insights.append(f"Only {total} feedback entries collected. Gather more data for stronger conclusions.")

    return insights


def _detect_alerts(negative_pct, avg_score, feedbacks):
    """Detect alert conditions requiring immediate attention."""
    alerts = []

    if negative_pct >= 50:
        alerts.append({
            'level': 'critical',
            'message': f'🔴 Critical: {negative_pct}% of feedback is negative. Immediate action required!'
        })
    elif negative_pct >= 30:
        alerts.append({
            'level': 'warning',
            'message': f'🟡 Warning: {negative_pct}% negative feedback detected. Investigation recommended.'
        })

    if avg_score < -0.5:
        alerts.append({
            'level': 'critical',
            'message': f'🔴 Critical: Average sentiment score is {avg_score}. Users are highly dissatisfied.'
        })
    elif avg_score < -0.2:
        alerts.append({
            'level': 'warning',
            'message': f'🟡 Warning: Average sentiment score is {avg_score}. Satisfaction trending down.'
        })

    # Check for consecutive negative feedback
    recent = feedbacks[-5:] if len(feedbacks) >= 5 else feedbacks
    recent_negative = sum(1 for f in recent if f.get('sentiment') == 'Negative')
    if recent_negative >= 4:
        alerts.append({
            'level': 'critical',
            'message': '🔴 Critical: Most recent feedback entries are predominantly negative.'
        })
    elif recent_negative >= 3:
        alerts.append({
            'level': 'warning',
            'message': '🟡 Warning: Recent feedback trend is turning negative.'
        })

    return alerts


def _analyze_trend(feedbacks):
    """Simple trend analysis based on comparing recent vs older feedback scores."""
    if len(feedbacks) < 4:
        return 'insufficient_data'

    mid = len(feedbacks) // 2
    older = feedbacks[:mid]
    newer = feedbacks[mid:]

    older_avg = sum(f.get('score', 0) for f in older) / len(older) if older else 0
    newer_avg = sum(f.get('score', 0) for f in newer) / len(newer) if newer else 0

    diff = newer_avg - older_avg
    if diff > 0.15:
        return 'improving'
    elif diff < -0.15:
        return 'declining'
    else:
        return 'stable'
