from transformers import pipeline
from transformers_interpret import SequenceClassificationExplainer
from logger import logger

def set_pipeline():
    try:
        model_name = "textdetox/bert-multilingual-toxicity-classifier"
        toxicity_pipeline = pipeline("text-classification", model=model_name, tokenizer=model_name)
        logger.debug("Pipline set up successful.")
        return toxicity_pipeline
    except Exception as e:
        logger.error(f"Error in setting up pipeline for textdetox model: {e}")
        raise

def get_predictions(comment):
    try:
        toxicity_pipeline=set_pipeline()
        result = toxicity_pipeline(comment)
        logger.debug(f"Prediction for {comment} : {result}")
        print(result)
        return result
    except Exception as e:
        logger.error(f"Can't get predictions for textdetox model: {e}")
        raise

# get_predictions("Hello")



