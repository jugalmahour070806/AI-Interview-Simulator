
import re


def analyze_answer(answer, audio_duration=None):

    answer = answer.strip()

    # Word count
    words = re.findall(r"\b[\w']+\b", answer.lower())
    word_count = len(words)

    # Filler word detection
    filler_patterns = [
        r"\bum\b",
        r"\buh\b",
        r"\ber\b",
        r"\bah\b",
        r"\blike\b",
        r"\byou know\b",
        r"\bbasically\b",
        r"\bactually\b",
        r"\bi mean\b"
    ]

    filler_count = 0

    for pattern in filler_patterns:
        filler_count += len(
            re.findall(pattern, answer.lower())
        )

    # Sentence analysis
    sentences = [
        sentence.strip()
        for sentence in re.split(r"[.!?]+", answer)
        if sentence.strip()
    ]

    sentence_count = len(sentences)

    if sentence_count > 0:
        average_sentence_length = word_count / sentence_count
    else:
        average_sentence_length = 0

    # Speaking speed
    speaking_wpm = None

    if audio_duration and audio_duration > 0:
        speaking_wpm = (word_count / audio_duration) * 60

    # Basic communication indicator
    length_points = min(word_count * 0.25, 25)
    structure_points = 10 if sentence_count >= 2 else 5
    filler_penalty = min(filler_count * 5, 20)

    speed_points = 0

    if speaking_wpm is not None:
        if 100 <= speaking_wpm <= 160:
            speed_points = 15
        elif 80 <= speaking_wpm < 100:
            speed_points = 8
        elif 160 < speaking_wpm <= 180:
            speed_points = 8

    confidence_score = (
        50 + length_points + structure_points
        + speed_points - filler_penalty
    )

    confidence_score = round(
        max(0, min(100, confidence_score))
    )

    # Suggestions
    suggestions = []

    if word_count < 25:
        suggestions.append(
            "Try explaining your answer in more detail with an example."
        )

    if filler_count > 2:
        suggestions.append(
            "Reduce filler words such as um, uh and basically."
        )

    if sentence_count <= 1:
        suggestions.append(
            "Use short and clear sentences to organise your answer."
        )

    if speaking_wpm is not None:
        if speaking_wpm < 100:
            suggestions.append(
                "Try speaking a little faster while maintaining clarity."
            )
        elif speaking_wpm > 160:
            suggestions.append(
                "Slow down slightly and pronounce words clearly."
            )
        else:
            suggestions.append(
                "Your speaking speed is within the practice target range."
            )
    else:
        suggestions.append(
            "Record your answer to calculate speaking speed."
        )

    if not suggestions:
        suggestions.append(
            "Good effort! Continue practising structured answers."
        )

    return {
        "word_count": word_count,
        "filler_count": filler_count,
        "sentence_count": sentence_count,
        "average_sentence_length": round(
            average_sentence_length, 1
        ),
        "speaking_wpm": (
            round(speaking_wpm, 1)
            if speaking_wpm is not None else None
        ),
        "confidence_score": confidence_score,
        "suggestions": suggestions
    }
