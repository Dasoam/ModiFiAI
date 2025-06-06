from lang_detect import detect_lang
from profanity_filter import detect_profanity
from perspective_ai import send_req, extract_attribute_scores
from bert_based_model_predict import get_predictions
from llm_based_analysis import get_groq_response
from explainable_ai import get_groq_explanation
from logger import logger

def start_pipeline(comment):
    step_1_results=None
    lang=detect_lang(comment)
    if lang=="unknown":
        response=use_llm_for_unknown_language(comment)
        return response
    else:
        if lang=="en":
            step_1_results=detect_profanity(comment,lang)
        elif lang=="hi":
            step_1_results=detect_profanity(comment,lang)
        else:
            response = use_llm_for_unknown_language(comment)
            return response

    if step_1_results['profane_count'] >=1:
        reason=check_3(comment)
        return {'comment':comment,'published':'false', 'reason':reason}
    else:
        step_2_result=check_2(comment)
        if step_2_result=="publish":
            return publish(comment)
        else:
            reason = check_3(comment)
            if step_2_result[1]>80:
                return {'comment': comment, 'published': 'false', 'reason': reason}
            else:
                return {'comment': comment, 'published': 'check', 'reason': reason}

def check_2(comment):
    result=get_predictions(comment)
    label = 0 if result[0]['label'] == 'LABEL_0' else 1
    score = result[0]['score']

    perspective=send_req(comment)
    p_scores = extract_attribute_scores(perspective)
    max_scores = {}
    for category, entries in p_scores.items():
        max_score = max(entry['score'] for entry in entries)
        max_scores[category] = max_score

    final_score=max(score,max_scores['TOXICITY'])
    if label==1 and final_score>60:
        reason=check_3(comment)
        return [reason,final_score]
    else:
        return "publish"

def check_3(comment):
    return get_groq_explanation(comment)

def use_llm_for_unknown_language(comment):
    tag = get_groq_response(comment)
    if tag == 'Safe':
        return publish(comment)
    else:
        logger.info(f"groq prediction on unknown language: {tag}")
        reason = check_3(comment)
        return {'comment': comment, 'published': 'false', 'reason': reason}

def publish(comment):
    return {'comment':comment,'published':'true', 'reason':'Comment is not toxic.'}