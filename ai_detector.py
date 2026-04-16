"""
AI vs Human Text Detection Module
Uses heuristic-based features to determine if feedback is AI-generated or human-written.
Features: vocabulary diversity, sentence length consistency, repetition patterns,
          punctuation regularity, and formality indicators.
"""

import re
import string
import math


def _tokenize(text: str) -> list:
    """Simple word tokenizer."""
    text = text.lower().strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return [w for w in text.split() if w]


def _split_sentences(text: str) -> list:
    """Split text into sentences."""
    sentences = re.split(r'[.!?]+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def vocabulary_diversity(text: str) -> float:
    """
    Type-Token Ratio (TTR): unique words / total words.
    AI text tends to have lower diversity (more repetitive vocabulary).
    """
    words = _tokenize(text)
    if not words:
        return 0.0
    return len(set(words)) / len(words)


def sentence_length_consistency(text: str) -> float:
    """
    Standard deviation of sentence lengths.
    AI text tends to have more uniform sentence lengths (lower std dev).
    Returns normalized score (0 = very consistent, 1 = very varied).
    """
    sentences = _split_sentences(text)
    if len(sentences) < 2:
        return 0.5

    lengths = [len(s.split()) for s in sentences]
    mean = sum(lengths) / len(lengths)
    variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
    std_dev = math.sqrt(variance)

    # Normalize: human text typically has std_dev of 5-15 words
    normalized = min(std_dev / 15.0, 1.0)
    return normalized


def repetition_score(text: str) -> float:
    """
    Measure bigram and trigram repetition.
    AI text often has more repeated phrases.
    Returns 0-1 score (higher = more repetitive = more likely AI).
    """
    words = _tokenize(text)
    if len(words) < 4:
        return 0.0

    # Bigrams
    bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words) - 1)]
    bigram_unique = len(set(bigrams)) / len(bigrams) if bigrams else 1

    # Trigrams
    trigrams = [f"{words[i]} {words[i+1]} {words[i+2]}" for i in range(len(words) - 2)]
    trigram_unique = len(set(trigrams)) / len(trigrams) if trigrams else 1

    # Lower uniqueness ratio means more repetition
    rep_score = 1 - ((bigram_unique + trigram_unique) / 2)
    return max(0.0, min(rep_score, 1.0))


def formality_score(text: str) -> float:
    """
    Measure text formality. AI text tends to be more formal.
    Checks for contractions, informal language, first-person pronouns, etc.
    Returns 0-1 (higher = more formal = more likely AI).
    """
    text_lower = text.lower()

    informal_markers = [
        "i'm", "i've", "i'd", "i'll", "can't", "won't", "don't", "doesn't",
        "didn't", "isn't", "aren't", "wasn't", "weren't", "hasn't", "haven't",
        "couldn't", "wouldn't", "shouldn't", "it's", "that's", "there's",
        "lol", "omg", "btw", "tbh", "imo", "imho", "gonna", "wanna", "gotta",
        "kinda", "sorta", "dunno", "yeah", "nah", "yep", "nope", "ok", "okay",
        "!", "!!", "...", "haha", "hehe"
    ]

    formal_markers = [
        "furthermore", "moreover", "consequently", "nevertheless", "however",
        "therefore", "additionally", "in conclusion", "it is important",
        "it should be noted", "one might argue", "in summary", "overall",
        "comprehensive", "significant", "substantial", "facilitate", "utilize",
        "implement", "demonstrate", "acknowledge", "emphasize"
    ]

    informal_count = sum(1 for m in informal_markers if m in text_lower)
    formal_count = sum(1 for m in formal_markers if m in text_lower)

    total = informal_count + formal_count
    if total == 0:
        return 0.5

    return formal_count / total


def punctuation_regularity(text: str) -> float:
    """
    AI text tends to have very regular punctuation patterns.
    Returns 0-1 (higher = more regular = more likely AI).
    """
    sentences = _split_sentences(text)
    if len(sentences) < 2:
        return 0.5

    # Check if all sentences end with the same punctuation
    endings = []
    for match in re.finditer(r'[.!?]+', text):
        endings.append(match.group())

    if not endings:
        return 0.5

    # If all endings are the same, it's more AI-like
    unique_endings = len(set(endings))
    regularity = 1 - (unique_endings / len(endings))
    return max(0.0, min(regularity, 1.0))


def detect_ai(text: str) -> dict:
    """
    Main detection function. Combines multiple heuristic features.
    Returns classification, confidence score, and feature breakdown.
    """
    if not text or not text.strip():
        return {
            'classification': 'Insufficient Text',
            'confidence': 0.0,
            'features': {},
            'explanation': 'Please provide text for analysis.'
        }

    # Calculate features
    vocab_div = vocabulary_diversity(text)
    sent_consistency = sentence_length_consistency(text)
    rep_score = repetition_score(text)
    formality = formality_score(text)
    punct_reg = punctuation_regularity(text)

    # AI indicators (weighted scoring)
    # Low vocabulary diversity → AI
    vocab_ai = max(0, 1 - vocab_div * 1.5)
    # Low sentence variation → AI
    consistency_ai = max(0, 1 - sent_consistency * 2)
    # High repetition → AI
    rep_ai = rep_score
    # High formality → AI
    formality_ai = formality
    # High punctuation regularity → AI
    punct_ai = punct_reg

    # Weighted average
    weights = {
        'vocabulary': 0.20,      # Slightly lower weight
        'consistency': 0.30,     # Higher weight for uniform sentence structure
        'repetition': 0.15,
        'formality': 0.25,
        'punctuation': 0.10
    }

    ai_score = (
        vocab_ai * weights['vocabulary'] +
        consistency_ai * weights['consistency'] +
        rep_ai * weights['repetition'] +
        formality_ai * weights['formality'] +
        punct_ai * weights['punctuation']
    )

    ai_score = round(max(0.0, min(ai_score, 1.0)), 4)

    # Classification
    if ai_score >= 0.55:         # Lowered from 0.60
        classification = 'Likely AI'
    elif ai_score >= 0.22:       # Lowered from 0.30 to catch high-quality templates
        classification = 'Possibly AI'
    else:
        classification = 'Human'

    features = {
        'vocabulary_diversity': round(vocab_div, 4),
        'sentence_consistency': round(sent_consistency, 4),
        'repetition': round(rep_score, 4),
        'formality': round(formality, 4),
        'punctuation_regularity': round(punct_reg, 4)
    }

    # Generate explanation
    explanations = []
    if vocab_ai > 0.5:
        explanations.append("Low vocabulary diversity suggests templated language.")
    if consistency_ai > 0.5:
        explanations.append("Very uniform sentence lengths typical of AI generation.")
    if rep_ai > 0.3:
        explanations.append("Repetitive phrase patterns detected.")
    if formality_ai > 0.6:
        explanations.append("Highly formal tone often associated with AI text.")
    if punct_ai > 0.6:
        explanations.append("Very regular punctuation patterns.")

    if not explanations:
        if classification == 'Human':
            explanations.append("Text shows natural variation in vocabulary and structure.")
        else:
            explanations.append("Some features suggest possible AI generation.")

    return {
        'classification': classification,
        'confidence': ai_score,
        'features': features,
        'explanation': ' '.join(explanations)
    }
