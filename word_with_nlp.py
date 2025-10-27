# file: word_with_nlp.py
import re

class nlp_class:
    """
    Minimal NLP helper for feature_extractor.
    Used for random_domain() feature detection.
    """

    def check_word_random(self, domain: str) -> int:
        d = domain.lower()

        # Heuristic 1: contains digits
        if re.search(r"\d", d):
            return 1

        # Heuristic 2: too many consonants in a row (>=4)
        if re.search(r"[bcdfghjklmnpqrstvwxyz]{4,}", d):
            return 1

        # Looks normal
        return 0
