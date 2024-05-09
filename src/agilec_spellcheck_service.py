import requests

def get_response(word):
    URL = "https://agilec.cs.uh.edu/spellcheck?check="     
    return requests.get(f"{URL}{word}").text

def parse(response): 
    if response not in ['true', 'false']:
        raise ValueError("Not true or false")

    return response == 'true' 

def spellcheck(word):
    response = get_response(word)
    return parse(response)
