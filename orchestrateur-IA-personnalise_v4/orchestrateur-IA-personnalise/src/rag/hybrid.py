import math, os, pickle, re
from collections import Counter, defaultdict
from typing import List, Dict, Any, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix

def _tokenize(s: str) -> List[str]:
    s = s.lower()
    s = re.sub(r"[^a-z0-9àâäçéèêëîïôöùûüÿœ\-\s]", " ", s)
    return [t for t in s.split() if t]

class BM25Index:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.doc_freq = Counter()
        self.docs_tokens: List[List[str]] = []
        self.avgdl = 0.0

    def fit(self, docs: List[str]):
        self.docs_tokens = [_tokenize(d) for d in docs]
        self.doc_freq = Counter()
        for toks in self.docs_tokens:
            for w in set(toks):
                self.doc_freq[w] += 1
        self.avgdl = sum(len(t) for t in self.docs_tokens) / max(1, len(self.docs_tokens))

    def idf(self, term: str, N: int) -> float:
        df = self.doc_freq.get(term, 0) + 0.5
        return math.log((N - df + 0.5) / df + 1.0)

    def scores(self, query: str) -> List[float]:
        q = _tokenize(query)
        N = len(self.docs_tokens)
        scores = np.zeros(N, dtype=float)
        for i, toks in enumerate(self.docs_tokens):
            tf = Counter(toks)
            dl = len(toks)
            s = 0.0
            for term in q:
                if tf[term] == 0: 
                    continue
                idf = self.idf(term, N)
                num = tf[term] * (self.k1 + 1)
                den = tf[term] + self.k1 * (1 - self.b + self.b * dl / (self.avgdl or 1))
                s += idf * num / (den or 1e-9)
            scores[i] = s
        return scores.tolist()

class HybridRetriever:
    """
    Hybrid of TF-IDF cosine and BM25; with an optional rerank hook (e.g. Cohere) if env provides key.
    Index is produced by build_index.py (TF-IDF matrix + metadata). BM25 is rebuilt locally from chunks.
    """
    def __init__(self, index_path: str = "data/index.pkl", alpha: float = 0.5):
        self.index_path = index_path
        self.alpha = alpha
        self.loaded = False
        self._load()

    def _load(self):
        if not os.path.exists(self.index_path):
            self.loaded = False
            return
        payload = pickle.loads(open(self.index_path, "rb").read())
        self.chunks: List[str] = payload.get("chunks", [])
        self.meta: List[Dict[str, Any]] = payload.get("meta", [])
        vocab = payload.get("vocabulary", {})
        idf = np.array(payload.get("idf", []))
        self.vectorizer = TfidfVectorizer(vocabulary=vocab, ngram_range=(1,2))
        self.vectorizer._tfidf._idf_diag = None
        self.vectorizer._tfidf.idf_ = idf
        shape = tuple(payload.get("X_shape", (0,0)))
        indices = np.array(payload.get("X_indices", []))
        indptr = np.array(payload.get("X_indptr", []))
        data = np.array(payload.get("X_data", []), dtype=float)
        self.X = csr_matrix((data, indices, indptr), shape=shape)
        # BM25
        self.bm25 = BM25Index()
        self.bm25.fit(self.chunks)
        self.loaded = True

    def _rerank(self, query: str, candidates: List[Tuple[int, float]]) -> List[Tuple[int, float]]:
        # Optional Cohere-like reranker hook (no external calls unless COHERE_API_KEY is set)
        if not os.getenv("COHERE_API_KEY"):
            return candidates
        # Placeholder: keep order; users can implement real rerank call here safely.
        return candidates

    def search(self, query: str, k: int = 6) -> List[Dict[str, Any]]:
        if not self.loaded or self.X.shape[0] == 0:
            return []
        # TF-IDF cosine
        qv = self.vectorizer.transform([query])
        tfidf = (qv @ self.X.T).toarray().ravel()
        # BM25
        bm25 = np.array(self.bm25.scores(query))
        # Normalize
        if tfidf.max() > 0: tfidf = tfidf / (tfidf.max() or 1)
        if bm25.max() > 0: bm25 = bm25 / (bm25.max() or 1)
        # Fuse
        scores = self.alpha * tfidf + (1 - self.alpha) * bm25
        idx = scores.argsort()[::-1][: max(k*3, k)]
        cand = [(int(i), float(scores[i])) for i in idx if scores[i] > 0]
        cand = self._rerank(query, cand)[:k]
        out = []
        for i, sc in cand:
            out.append({"text": self.chunks[i], "source": self.meta[i]["source"], "score": sc})
        return out
