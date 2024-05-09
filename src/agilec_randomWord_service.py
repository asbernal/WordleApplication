import requests
import random


def get_randomWords():
    URL = "https://agilec.cs.uh.edu/words"     
    return requests.get(f"{URL}").text

def parse(response): 
    if response not in ['FAVOR\nSMART\nGUIDE\nTESTS\nGRADE\nBRAIN\nSPAIN\nSPINE\nGRAIN\nBOARD\n']:
        raise ValueError("Not correct words of list")
    
    return response.split()

def pick_randomWord():

    response = get_randomWords()

    parseResponse = parse(response)

    return random.choice(parseResponse)
