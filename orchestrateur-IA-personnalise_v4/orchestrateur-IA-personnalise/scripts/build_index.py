import argparse, os, glob, json, re, pickle
from pathlib import Path
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer

def read_texts(input_dir: str) -> List[Tuple[str, str]]:
    files = []
    for ext in ("*.md", "*.txt"):
        for p in glob.glob(os.path.join(input_dir, ext)):
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                files.append((p, f.read()))
    return files

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 80) -> List[str]:
    # simple word-based chunking
    words = re.split(r"\s+", text)
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += (chunk_size - overlap)
    return chunks

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Folder with .md/.txt files")
    ap.add_argument("--index", required=True, help="Path to write index pickle")
    args = ap.parse_args()

    docs = read_texts(args.input)
    if not docs:
        print("No docs found in", args.input)
        Path(args.index).write_bytes(pickle.dumps({"chunks": [], "paths": [], "v": None, "X": None}))
        return

    corpus = []
    meta = []
    for path, text in docs:
        chunks = chunk_text(text)
        for i, ch in enumerate(chunks):
            corpus.append(ch)
            meta.append({"source": f"{os.path.relpath(path)}#chunk={i}"})
    vec = TfidfVectorizer(min_df=1, ngram_range=(1,2))
    X = vec.fit_transform(corpus)

    payload = {"chunks": corpus, "meta": meta, "vocabulary": vec.vocabulary_, "idf": vec.idf_.tolist()}
    # Save sparse matrix as CSR components to avoid heavy pickle
    payload["X_shape"] = X.shape
    payload["X_indices"] = X.indices.tolist()
    payload["X_indptr"] = X.indptr.tolist()
    payload["X_data"] = X.data.tolist()

    Path(args.index).write_bytes(pickle.dumps(payload))
    print(f"Indexed {len(corpus)} chunks from {len(docs)} files → {args.index}")

if __name__ == "__main__":
    main()
