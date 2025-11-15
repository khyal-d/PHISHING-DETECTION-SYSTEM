from .packages import *
from .config import *
# ===============================================================
# CELL 1: Setup, Imports, and Helper Functions
# ===============================================================

def tokenize_url_words(url: str):
    lowered = url.lower()
    cleaned = re.sub(r'[/:?=&\.\-_~%\+]+', ' ', lowered)
    words = [w for w in cleaned.split() if w]
    return words

def parse_url_bits(url: str):
    parsed = urlparse(url)

    scheme = parsed.scheme
    netloc = parsed.netloc
    path   = parsed.path or ""
    query  = parsed.query or ""

    base_url = f"{scheme}://{netloc}"
    host_only = netloc.split('@')[-1]
    host_no_port = host_only.split(':')[0]

    tld_info = tldextract.extract(url)
    subdomain = tld_info.subdomain or ""
    domain    = tld_info.domain or ""
    suffix    = tld_info.suffix or ""

    full_path_q = path + ("?" + query if query else "")
    words_raw = tokenize_url_words(url)

    return {
        "scheme": scheme,
        "netloc": netloc,
        "host": host_no_port,
        "domain": domain,
        "subdomain": subdomain,
        "suffix": suffix,
        "path": path,
        "query": query,
        "path_plus_query": full_path_q,
        "base_url": base_url,
        "words_raw": words_raw,
        "url": url
    }

def safe_ratio_digits(s: str):
    if len(s) == 0:
        return 0
    return len(re.sub("[^0-9]", "", s)) / len(s)

def brand_in_subdomain(domain_str, subdomain_str):
    for b in allbrand:
        if b in subdomain_str and b != domain_str:
            return 1
    return 0

# ===============================================================
# CELL 2: Group 1 — Basic URL Structure / Syntax
# ===============================================================

def extract_group1_basic(url: str): 
    parts = parse_url_bits(url)

    def has_ip(url):
        match = re.search(
            '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
            '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
            '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)|'  # IPv4 in hexadecimal
            '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
            '[0-9a-fA-F]{7}', url)  # Ipv6
        if match:
            return 1
        else:
            return 0

    def has_prefix_suffix(u):
        return 1 if re.search(r"-", urlparse(u).netloc.split('.')[-2]) else 0

    def has_punycode(u):
        return 1 if "xn--" in u else 0

    def has_tld_in_path(tld, path):
        return 1 if tld and tld in path else 0

    def has_tld_in_subdomain(tld, subdomain):
        return 1 if tld and tld in subdomain else 0

    def abnormal_subdomain(u):
        sub = urlparse(u).netloc.split('.')
        return 1 if len(sub) > 3 else 0

    return {
        "length_url": len(url),
        "length_hostname": len(parts["host"]),
        "ip": has_ip(url),
        "nb_dots": parts["host"].count('.'),
        "port": 1 if ":" in parts["netloc"] else 0,
        "ratio_digits_url": safe_ratio_digits(parts["url"]),
        "ratio_digits_host": safe_ratio_digits(parts["host"]),
        "punycode": has_punycode(url),
        "nb_subdomains": len(parts["subdomain"].split('.')) if parts["subdomain"] else 0,
        "prefix_suffix": has_prefix_suffix(url),
        "shortening_service": 1 if re.search(r"(bit\.ly|goo\.gl|tinyurl\.com|t\.co|ow\.ly)", url) else 0,
        "tld_in_path": has_tld_in_path(parts["suffix"], parts["path_plus_query"]),
        "tld_in_subdomain": has_tld_in_subdomain(parts["suffix"], parts["subdomain"]),
        "abnormal_subdomain": abnormal_subdomain(url),
        "nb_dslash": url.count("//") - 1,
        "http_in_path": 1 if "http" in parts["path_plus_query"] else 0,
        "https_token": 1 if "https" in parts["scheme"] else 0
    }

# ===============================================================
# CELL 3: Group 2 — Symbol Counts and Redirects
# ===============================================================

def extract_group2_chars(url: str):
    parts = parse_url_bits(url)

    try:
        page = requests.get(url, allow_redirects=True, timeout=3)
    except Exception:
        class Dummy:
            history = []
        page = Dummy()

    def count_symbol(u, s): return u.count(s)
    def count_double_slash(u): return u.count("//") - 1

    nb_redirection = len(page.history)
    nb_external_redirection = sum(
        1 for r in page.history if parts["domain"].lower() not in r.url.lower()
    )

    return {
        "nb_hyphens": count_symbol(url, "-"),
        "nb_at": count_symbol(url, "@"),
        "nb_qm": count_symbol(url, "?"),
        "nb_and": count_symbol(url, "&"),
        "nb_or": url.lower().count("|"),
        "nb_eq": count_symbol(url, "="),
        "nb_underscore": count_symbol(url, "_"),
        "nb_tilde": count_symbol(url, '~'),        
        "nb_percent": count_symbol(url, "%"),
        "nb_slash": count_symbol(url, "/"),
        "nb_star": count_symbol(url, "*"),
        "nb_colon": count_symbol(url, ":"),
        "nb_comma": count_symbol(url, ","),
        "nb_semicolumn": count_symbol(url, ";"),
        "nb_dollar": count_symbol(url, "$"),
        "nb_space": count_symbol(url, " "),
        "nb_www": 1 if "www" in url.lower() else 0,
        "nb_com": url.lower().count(".com"),
        "nb_dslash": count_double_slash(url),
        "nb_redirection": nb_redirection,
        "nb_external_redirection": nb_external_redirection,
    }


# ===============================================================
# CELL 4: Group 3 — Word Statistics
# ===============================================================

def extract_group3_wordstats(url: str):
    parts = parse_url_bits(url)
    words = parts["words_raw"]

    def length_words_raw(words): return sum(len(w) for w in words)
    def char_repeat(words): return max([words.count(w) for w in set(words)]) if words else 0
    def shortest(words): return min(map(len, words)) if words else 0
    def longest(words): return max(map(len, words)) if words else 0
    def average(words): return sum(map(len, words)) / len(words) if words else 0

    host = [parts["host"]]
    path = [parts["path"] or ""]

    return {
        "length_words_raw": length_words_raw(words),
        "char_repeat": char_repeat(words),
        "shortest_words_raw": shortest(words),
        "shortest_word_host": shortest(host),
        "shortest_word_path": shortest(path),
        "longest_words_raw": longest(words),
        "longest_word_host": longest(host),
        "longest_word_path": longest(path),
        "avg_words_raw": average(words),
        "avg_word_host": average(host),
        "avg_word_path": average(path),
    }

# ===============================================================
# CELL 5: Group 4 — Phishing / Brand / DNS / TLD Heuristics
# ===============================================================

def extract_group4_phish(url: str):
    parts = parse_url_bits(url)

    def phish_hints(path_q):
        hints = ['wp', 'login', 'includes', 'admin', 'content', 'site', 'images', 'js', 'alibaba', 'css', 'myaccount', 'dropbox', 'themes', 'plugins', 'signin', 'view']
        return 1 if any(h in path_q.lower() for h in hints) else 0

    def domain_in_brand(domain):
        return 1 if domain in allbrand else 0

    def brand_in_path(domain, path_q):
        for b in allbrand:
            if b in path_q and b != domain:
                return 1
        return 0

    def suspecious_tld(tld):
        bad_tlds = ["zip", "xyz", "top", "gq", "tk", "ml", "cf"]
        return 1 if tld in bad_tlds else 0

    def statistical_report(url, domain):
        url_match = re.search('at\.ua|usa\.cc|beget\.tech|16mb\.com', url)
        try:
            ip_address = socket.gethostbyname(domain)
            ip_match = re.search('146\.112\.61\.108|23\.253\.164\.', ip_address)
            if url_match or ip_match:
                return 1
        except:
            pass
        return 0

    return {
        "phish_hints": phish_hints(parts["path_plus_query"]),
        "domain_in_brand": domain_in_brand(parts["domain"]),
        "brand_in_subdomain": brand_in_subdomain(parts["domain"], parts["subdomain"]),
        "brand_in_path": brand_in_path(parts["domain"], parts["path_plus_query"]),
        "suspecious_tld": suspecious_tld(parts["suffix"]),
        "statistical_report": statistical_report(parts["url"], parts["domain"]),
    }


# ===============================================================
# CELL 6: Combine All Feature Groups into One Extractor
# ===============================================================


# ===============================================================
# helper function (used for random_domain feature)
# ===============================================================
def check_word_random(domain: str) -> int:
    d = domain.lower()
    if re.search(r"\d", d):
        return 1
    if re.search(r"[bcdfghjklmnpqrstvwxyz]{4,}", d):
        return 1
    return 0


# ===============================================================
# Combine All Feature Groups into One Extractor
# ===============================================================
def extract_all_url_structure_features(url: str):
    g1 = extract_group1_basic(url)
    g2 = extract_group2_chars(url)
    g3 = extract_group3_wordstats(url)
    g4 = extract_group4_phish(url)

    parts = parse_url_bits(url)

    random_val = check_word_random(parts["domain"])

    features = OrderedDict([
        ("length_url", g1["length_url"]),
        ("length_hostname", g1["length_hostname"]),
        ("ip", g1["ip"]),
        ("nb_dots", g1["nb_dots"]),
        ("nb_hyphens", g2["nb_hyphens"]),
        ("nb_at", g2["nb_at"]),
        ("nb_qm", g2["nb_qm"]),
        ("nb_and", g2["nb_and"]),
        ("nb_or", g2["nb_or"]),
        ("nb_eq", g2["nb_eq"]),
        ("nb_underscore", g2["nb_underscore"]),
        ("nb_tilde", g2["nb_tilde"]),
        ("nb_percent", g2["nb_percent"]),
        ("nb_slash", g2["nb_slash"]),
        ("nb_star", g2["nb_star"]),
        ("nb_colon", g2["nb_colon"]),
        ("nb_comma", g2["nb_comma"]),
        ("nb_semicolumn", g2["nb_semicolumn"]),
        ("nb_dollar", g2["nb_dollar"]),
        ("nb_space", g2["nb_space"]),
        ("nb_www", g2["nb_www"]),
        ("nb_com", g2["nb_com"]),
        ("nb_dslash", g1["nb_dslash"]),
        ("http_in_path", g1["http_in_path"]),
        ("https_token", g1["https_token"]),
        ("ratio_digits_url", g1["ratio_digits_url"]),
        ("ratio_digits_host", g1["ratio_digits_host"]),
        ("punycode", g1["punycode"]),
        ("port", g1["port"]),
        ("tld_in_path", g1["tld_in_path"]),
        ("tld_in_subdomain", g1["tld_in_subdomain"]),
        ("abnormal_subdomain", g1["abnormal_subdomain"]),
        ("nb_subdomains", g1["nb_subdomains"]),
        ("prefix_suffix", g1["prefix_suffix"]),
        ("random_domain", random_val),
        ("shortening_service", g1["shortening_service"]),
        ("path_extension", 1 if "." in parts["path"].split("/")[-1] else 0),
        ("nb_redirection", g2["nb_redirection"]),
        ("nb_external_redirection", g2["nb_external_redirection"]),
        ("length_words_raw", g3["length_words_raw"]),
        ("char_repeat", g3["char_repeat"]),
        ("shortest_words_raw", g3["shortest_words_raw"]),
        ("shortest_word_host", g3["shortest_word_host"]),
        ("shortest_word_path", g3["shortest_word_path"]),
        ("longest_words_raw", g3["longest_words_raw"]),
        ("longest_word_host", g3["longest_word_host"]),
        ("longest_word_path", g3["longest_word_path"]),
        ("avg_words_raw", g3["avg_words_raw"]),
        ("avg_word_host", g3["avg_word_host"]),
        ("avg_word_path", g3["avg_word_path"]),
        ("phish_hints", g4["phish_hints"]),
        ("domain_in_brand", g4["domain_in_brand"]),
        ("brand_in_subdomain", g4["brand_in_subdomain"]),
        ("brand_in_path", g4["brand_in_path"]),
        ("suspecious_tld", g4["suspecious_tld"]),
        ("statistical_report", g4["statistical_report"]),
    ])

    return features






