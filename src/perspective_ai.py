import os
import json
from dotenv import load_dotenv
from googleapiclient import discovery
from logger import logger  # Ensure you have a logger configured

# Load environment variables from .env
load_dotenv()


def get_api():
    return os.getenv("perspective_api")


def set_client():
    API_KEY = get_api()
    if not API_KEY:
        raise ValueError("PERSPECTIVE_API environment variable not set")

    logger.debug("API KEY fetched.")

    try:
        client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=API_KEY,
            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
            static_discovery=False,
        )
        logger.debug("Client initialized successfully.")
    except Exception as e:
        logger.error(f"Client initialization failed: {str(e)}")
        raise
    return client


def send_req(comment):
    try:
        analyze_request = {
            'comment': {'text': comment},
            'requestedAttributes': {
                'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {},
                'INSULT': {}, 'PROFANITY': {}, 'THREAT': {}
            }
        }
        response = set_client().comments().analyze(body=analyze_request).execute()
        logger.debug("Response body: {}".format(json.dumps(response, indent=4)))
        return response  # Return raw dictionary
    except Exception as e:
        logger.error(f"Request sending error | {e}")
        return None


def extract_attribute_scores(response_dict):
    attribute_scores = response_dict.get("attributeScores", {})
    result = {}

    for attr, data in attribute_scores.items():
        spans = data.get("spanScores", [])
        result[attr] = []
        for span in spans:
            result[attr].append({
                "begin": span["begin"],
                "end": span["end"],
                "score": span["score"]["value"]
            })
    return result


# Example usage
# comment = "Hello how are you?"
# response = send_req(comment)
#
# if response:
#     scores = extract_attribute_scores(response)
#     print(scores)
#     # print(json.dumps(scores, indent=2))
# else:
#     print("No response received from Perspective API.")
