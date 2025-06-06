from langdetect import detect, LangDetectException
from logger import logger

def detect_lang(user_comment: str)-> str:
    """
        Detects the language of a given text comment.

        Args:
            user_comment (str): The comment text to detect language from.

        Returns:
            str: The detected language code (e.g., 'en', 'fr'), or 'unknown' on failure.
    """
    try:
        cleaned_comment = user_comment.strip()
        if not cleaned_comment:
            logger.warning("Empty or whitespace-only comment provided for language detection.")
            return "unknown"

        lang = detect(cleaned_comment)
        preview_comment = cleaned_comment[:30].replace('\n','') + "..."
        logger.info(f"Detected language: {lang} | Input: '{preview_comment}'")
        return lang
    except LangDetectException as e:
        logger.error(f"Language detection failed: {e} | Input: '{user_comment[:30]}...'")
        return "unknown"


# detect_lang("how are you tu page h pata nahi tuje i think you are talking about?")