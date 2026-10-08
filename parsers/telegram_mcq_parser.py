import re
from typing import Dict, List

LETTER_MAP = {"A": 0, "B": 1, "C": 2, "D": 3}


def _clean(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())


def parse_mcq(text: str) -> Dict:
    """Parse a common Telegram MCQ post into the structure used by generators."""
    lines = [_clean(x) for x in text.splitlines() if _clean(x)]
    if not lines:
        raise ValueError("Telegram post is empty.")

    question = ""
    options: List[str] = []
    answer_index = None
    explanation = ""
    exam = "General MCQ"

    option_re = re.compile(r"^(?:([A-D])\s*[.)]|\(?([A-D])\)\s*)(.*)$", re.I)
    answer_re = re.compile(r"^(?:answer|ans|correct answer)\s*[:=-]?\s*([A-D])(?:\b|\\.)", re.I)

    for line in lines:
        low = line.lower()
        if low.startswith(("exam:", "exam -", "exam=")):
            exam = line.split(":", 1)[1].strip() if ":" in line else re.split(r"[-=]", line, 1)[1].strip()
            continue
        m = option_re.match(line)
        if m:
            options.append(m.group(3).strip())
            continue
        m = answer_re.match(line)
        if m:
            answer_index = LETTER_MAP[m.group(1).upper()]
            continue
        if low.startswith(("explanation:", "explanation -", "explain:")):
            explanation = re.split(r"[:=-]", line, 1)[1].strip()
            continue
        if not question:
            question = re.sub(r"^(?:q(?:uestion)?\s*[:.)-]?\s*)", "", line, flags=re.I)
        elif not explanation:
            explanation = line

    if len(options) != 4:
        raise ValueError(f"Expected 4 options, found {len(options)}.")
    if answer_index is None:
        raise ValueError("Answer not found. Add 'Answer: B' (for example).")
    if not question:
        raise ValueError("Question not found.")

    return {
        "exam": exam,
        "question": question,
        "options": options,
        "answer_index": answer_index,
        "answer_label": chr(65 + answer_index),
        "explanation": explanation,
        "cta": "Join our Telegram for more MCQs →",
    }


if __name__ == "__main__":
    sample = """Exam: SSC JE Civil\nQ. The purpose of providing weep holes in a retaining wall is to:\nA) Increase the strength of the wall\nB) Relieve the hydrostatic pressure behind the wall\nC) Prevent seepage of rainwater into the wall\nD) Improve the appearance of the wall\nAnswer: B\nExplanation: Weep holes allow water behind the wall to drain, reducing hydrostatic pressure."""
    print(parse_mcq(sample))
