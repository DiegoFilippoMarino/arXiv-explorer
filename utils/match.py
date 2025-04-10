def match_keywords(text, keyword_list):
    """
    Match keywords from a list in the given text.
    """
    text_lower = text.lower()
    return [kw for kw in keyword_list if kw.lower() in text_lower]

def safe_split(keyword_string):
    """
    Safely split a comma-separated keyword string.
    """
    try:
        return [kw.strip() for kw in keyword_string.split(",") if kw.strip()]
    except:
        return []