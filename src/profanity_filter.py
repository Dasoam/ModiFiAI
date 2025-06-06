import re
from logger import logger

# ----------------------------
# Core Functions
# ----------------------------

def load_wordlist(filepath):
    """Load words from file, ignoring comments and empty lines"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            logger.debug(f"Loaded file path: {filepath}")
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"Warning: {filepath} not found. Using empty list.")
        logger.error(f"File not found at {filepath}")
        return []


def normalize_obfuscations(text):
    """Replace obfuscated characters with their base forms"""
    replacements = {
        '@': 'a', '4': 'a', '^': 'a',
        '!': 'i', '1': 'i', '|': 'i',
        '$': 's', '5': 's', 'z': 's',
        '0': 'o', '()': 'o',
        '+': 't', '7': 't',
        '*': '', '_': '', '-': ''
    }
    # logger.debug("Replacing obfuscated")
    return ''.join(replacements.get(c, c) for c in text.lower())


def generate_obfuscation_pattern(word):
    """Create regex pattern to match obfuscated versions of a word"""
    obfuscation_map = {
        'a': r'[a@4áâàä]',
        'b': r'[b8]',
        'c': r'[c\(<{]',
        'd': r'[dð]',
        'e': r'[e3éêè]',
        'f': r'[f?]',
        'g': r'[g9]',
        'h': r'[h#]',
        'i': r'[i1!íîì]',
        'k': r'[k<]',
        'l': r'[l1]',
        'o': r'[o0óôòö]',
        's': r'[s$5z]',
        't': r'[t+7]',
        'u': r'[uúûù@ü]',
        'x': r'[x%]',
        'y': r'[yý]'
    }
    pattern = []
    for char in word.lower():
        pattern.append(obfuscation_map.get(char, re.escape(char)))
    # logger.debug(f"pattern: {pattern}")
    return r'\b' + ''.join(pattern) + r'(?:ing|ed|s|er)?\b'


def compile_patterns(words):
    """Create compiled regex patterns for all words"""
    return [re.compile(generate_obfuscation_pattern(word), re.IGNORECASE)
            for word in words]


def detect_profanity(comment, lang_code='en'):
    """
    Main detection function
    Returns: {
        'total_words': int,
        'profane_count': int,
        'profane_words': list,
        'normalized_text': str
    }
    """
    # Load appropriate wordlists
    base_words = []
    if lang_code == 'en':
        base_words = load_wordlist('KB/english.txt') + load_wordlist('KB/hinglish.txt')
    elif lang_code == 'hi':
        base_words = load_wordlist('KB/hindi.txt') + load_wordlist('KB/hinglish.txt')

    logger.debug(f"base_words length: {len(base_words)} | lang_code: {lang_code}")
    # Prepare regex patterns
    patterns = compile_patterns(base_words)

    # Normalize text
    normalized_text = normalize_obfuscations(comment)

    # logger.info("Normalized text: %s", normalized_text)
    # Find all matches
    profane_words = set()
    for pattern in patterns:
        matches = pattern.findall(normalized_text)
        if matches:
            profane_words.update(matches)

    # Split into words for counting
    words = re.findall(r'\b\w+\b', normalized_text)

    logger.info(f"total words: {len(words)} | profane_words: {list(profane_words)}")
    return {
        'total_words': len(words),
        'profane_count': len(profane_words),
        'profane_words': list(profane_words),
        'normalized_text': normalized_text
    }

# ----------------------------
# Example Usage
# ----------------------------

# test_comments = [
#     ("F@ck this sh!t and बहनचोद!", 'en'),
#     ("यह चूतिया काम है और m@darch0d भी है", 'hi'),
#     ("Awesome content nothing bad here", 'en')
# ]
#
# for comment, lang in test_comments:
#     result = detect_profanity(comment, lang)
#     print(f"\nInput: {comment}")
#     print(f"Language: {lang.upper()}")
#     print(f"Normalized: {result['normalized_text']}")
#     print(f"Total words: {result['total_words']}")
#     print(f"Profane count: {result['profane_count']}")
#     print(f"Profane words: {result['profane_words']}")
