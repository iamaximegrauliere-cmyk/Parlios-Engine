import os, pickle
from typing import List, Dict, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix

class TFIDFRetriever:
    def __init__(self, index_path: str = "data/index.pkl"):
        self.index_path = index_path
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
        # inject learned idf
        self.vectorizer._tfidf._idf_diag = None
        self.vectorizer._tfidf.idf_ = idf
        shape = tuple(payload.get("X_shape", (0,0)))
        indices = np.array(payload.get("X_indices", []))
        indptr = np.array(payload.get("X_indptr", []))
        data = np.array(payload.get("X_data", []), dtype=float)
        self.X = csr_matrix((data, indices, indptr), shape=shape)
        self.loaded = True

    def search(self, query: str, k: int = 4) -> List[Dict[str, Any]]:
        if not self.loaded or self.X.shape[0] == 0:
            return []
        qv = self.vectorizer.transform([query])
        sims = (qv @ self.X.T).toarray().ravel()
        idx = sims.argsort()[::-1][:k]
        results = []
        for i in idx:
            if sims[i] <= 0:
                continue
            results.append({"text": self.chunks[i], "source": self.meta[i]["source"], "score": float(sims[i])})
        return results
