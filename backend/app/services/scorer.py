from sqlalchemy.orm import Session
import numpy as np

def cosine_similarity(a, b) -> float:
    a = np.array(a)
    b = np.array(b)
    print(f"Cosine similarity - a norm: {np.linalg.norm(a)}, b norm: {np.linalg.norm(b)}")
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))