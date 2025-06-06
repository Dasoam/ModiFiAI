import logging
import os

# Create logs directory if not exists
os.makedirs("logs", exist_ok=True)

# Create and configure logger
logger = logging.getLogger("comment_moderation")
logger.setLevel(logging.DEBUG)

# File handler
file_handler = logging.FileHandler("logs/moderation.log", encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
