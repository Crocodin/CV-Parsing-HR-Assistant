from sqlalchemy.orm import Session
import numpy as np

def cosine_similarity(a, b) -> float:
    # convert to numpy arrays to ensure vector operations work correctly
    a = np.array(a)
    b = np.array(b)
    print(f"Cosine similarity - a norm: {np.linalg.norm(a)}, b norm: {np.linalg.norm(b)}")
    # dot product divided by product of magnitudes — result is between -1 and 1,
    # but embedding vectors are non-negative so in practice 0–1
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))