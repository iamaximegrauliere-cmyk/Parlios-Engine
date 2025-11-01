import re
from typing import List

def split_recursive(text: str, target: int = 900, overlap: int = 120) -> List[str]:
    """
    Split by headings > paragraphs > sentences to approach the target size in words.
    Language-agnostic heuristics; avoids breaking mid-sentence when possible.
    """
    # First break by headings or big gaps
    blocks = re.split(r"(?m)^#{1,6}\s.+$|\n\n+", text)
    chunks: List[str] = []
    buf: List[str] = []
    count = 0

    def flush(force=False):
        nonlocal buf, count
        if buf and (force or count >= target):
            chunks.append(" ".join(buf).strip())
            # overlap by words
            if overlap > 0:
                ov = " ".join(" ".join(buf).split()[-overlap:])
                buf = [ov]
                count = len(ov.split())
            else:
                buf = []
                count = 0

    for b in blocks:
        sentences = re.split(r"(?<=[\.!?…])\s+", b.strip())
        for s in sentences:
            w = len(s.split())
            if w == 0:
                continue
            if count + w > target * 1.2:  # avoid bloating too much
                flush(force=True)
            buf.append(s)
            count += w
            if count >= target:
                flush()
    flush(force=True)
    return [c for c in chunks if c]

def split_simple_words(text: str, chunk_size: int = 900, overlap: int = 120) -> List[str]:
    words = text.split()
    out: List[str] = []
    i = 0
    while i < len(words):
        out.append(" ".join(words[i:i+chunk_size]))
        i += max(1, chunk_size - overlap)
    return out
