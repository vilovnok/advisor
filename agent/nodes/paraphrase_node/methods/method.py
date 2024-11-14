import string


def text_converter(question: str) -> str:
    punctuation = string.punctuation.replace('-', '')
    question = question.lower().translate(str.maketrans(punctuation, ' ' * len(punctuation)))    
    question_list = question.split()    
    return " ".join(question_list)
