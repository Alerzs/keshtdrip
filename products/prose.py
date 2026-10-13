import re

WORD = re.compile(r"\S+")
SENTENCE = re.compile(r"[^.!?؟]+[.!?؟]?")
FORBIDDEN = re.compile(r"ن?می[\u200c\s]*باشد")
CONJUNCTION = {"و", "یا", "اما", "ولی", "بعد", "سپس"}


def word_count(text):
    return len(WORD.findall(text or ""))


def sentences(text):
    return [part.strip() for part in SENTENCE.findall(text or "") if part.strip()]


def _finish(text):
    text = (text or "").strip().strip("،,;؛")
    text = re.sub(r"^(?:و|یا)\s+", "", text)
    if not text:
        return ""
    if text[-1] not in ".!?؟":
        text += "."
    return text


def _cut(parts):
    best = None
    limit = min(20, len(parts) - 1)
    for index in range(5, limit):
        token = parts[index]
        bare = token.strip("،,;؛")
        followed = index + 1 < len(parts) and parts[index + 1].strip("،,;؛") in CONJUNCTION
        if bare in CONJUNCTION:
            candidate = index
        elif token[-1] in "،,;؛" or followed:
            candidate = index + 1
        else:
            continue
        remain = len(parts) - candidate
        if candidate < 6 or candidate > 20 or remain < 4:
            continue
        score = -abs(candidate - 14)
        if best is None or score > best[0]:
            best = (score, candidate)
    if best:
        return best[1]
    return min(16, len(parts) - 4)


def tighten_sentence(sentence):
    sentence = (sentence or "").strip()
    if not sentence:
        return []
    parts = WORD.findall(sentence)
    if len(parts) <= 20:
        done = _finish(sentence)
        return [done] if done else []
    cut = _cut(parts)
    left = _finish(" ".join(parts[:cut]))
    right = " ".join(parts[cut:])
    return ([left] if left else []) + tighten_sentence(right)


def tighten(text):
    pieces = []
    for sentence in sentences(text):
        pieces.extend(tighten_sentence(sentence))
    return " ".join(pieces)


def pack_blocks(text):
    tightened = tighten(text)
    blocks = []
    current = []
    count = 0
    for sentence in sentences(tightened):
        size = word_count(sentence)
        if current and count + size > 100:
            blocks.append(" ".join(current))
            current = [sentence]
            count = size
        else:
            current.append(sentence)
            count += size
    if current:
        blocks.append(" ".join(current))
    if len(blocks) >= 2 and word_count(blocks[-1]) < 60:
        if word_count(blocks[-2]) + word_count(blocks[-1]) <= 100:
            blocks[-2] = f"{blocks[-2]} {blocks[-1]}"
            blocks.pop()
    return [
        {"text": block, "words": word_count(block), "is_paragraph": 60 <= word_count(block) <= 100}
        for block in blocks
        if block.strip()
    ]
