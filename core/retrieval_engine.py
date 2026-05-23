import numpy as np
import hashlib


class RetrievalEngine:

    def vectorize(self, text):
        h = hashlib.md5(text.encode()).hexdigest()
        return np.array([int(h[i:i+2], 16) for i in range(0, 32, 2)])

    def similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)