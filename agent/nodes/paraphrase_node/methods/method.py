import string


def text_converter(content: str) -> str:
    punctuation = string.punctuation.replace('-', '')
    content = content.lower().translate(str.maketrans(punctuation, ' ' * len(punctuation)))    
    content_list = content.split()    
    return " ".join(content_list)
