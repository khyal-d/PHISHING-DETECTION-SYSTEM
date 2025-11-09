# file: word_with_nlp.py
import re

class nlp_class:
    def check_word_random(self, domain: str) -> int:
        d = domain.lower()
        if re.search(r"\d", d):
            return 1
        if re.search(r"[bcdfghjklmnpqrstvwxyz]{4,}", d):
            return 1
        return 0
