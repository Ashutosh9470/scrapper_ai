# processing/brand_detection.py
import re
from functools import lru_cache
from typing import Optional, Dict

from rapidfuzz import fuzz
from sentence_transformers import SentenceTransformer, util

from config import BRAND_ALIASES, BRAND_DESCRIPTIONS


def _normalize(t: str) -> str:
    t = t.lower()
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


@lru_cache(maxsize=1)
def get_semantic_model():
    # small, fast model
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


@lru_cache(maxsize=1)
def get_brand_embeddings() -> Dict[str, "torch.Tensor"]:
    model = get_semantic_model()
    brand_texts = []
    brands = []
    for brand, desc in BRAND_DESCRIPTIONS.items():
        alias_str = " ".join(BRAND_ALIASES.get(brand, []))
        combined = f"{brand}. {desc}. {alias_str}"
        brand_texts.append(combined)
        brands.append(brand)
    embs = model.encode(brand_texts, convert_to_tensor=True, normalize_embeddings=True)
    return {b: emb for b, emb in zip(brands, embs)}


def detect_brand(text: str) -> Optional[str]:
    """
    1. Exact/alias match
    2. Fuzzy alias match
    3. Semantic similarity to brand descriptions
    """
    if not text:
        return None

    norm = _normalize(text)

    # 1) Exact / alias
    for brand, aliases in BRAND_ALIASES.items():
        for alias in aliases:
            alias_norm = _normalize(alias)
            pattern = rf"\b{re.escape(alias_norm)}\b"
            if re.search(pattern, norm):
                return brand

    # 2) Fuzzy alias (handles typos)
    for brand, aliases in BRAND_ALIASES.items():
        for alias in aliases:
            if fuzz.partial_ratio(alias.lower(), norm) > 87:
                return brand

    # 3) Semantic similarity
    brand_embs = get_brand_embeddings()
    model = get_semantic_model()
    text_emb = model.encode(norm, convert_to_tensor=True, normalize_embeddings=True)

    best_brand = None
    best_score = 0.0

    for brand, emb in brand_embs.items():
        sim = float(util.cos_sim(text_emb, emb)[0][0])
        if sim > best_score:
            best_score = sim
            best_brand = brand

    # threshold to avoid random assignment
    if best_score >= 0.55:
        return best_brand

    return None
