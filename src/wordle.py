from enum import Enum

WORD_SIZE = 5

class Matches(Enum):
    EXACT_MATCH = 'Exact Match'
    PARTIAL_MATCH = 'Part Match'
    NO_MATCH = 'No Match'

class Status(Enum):
    WIN = 'Win'
    LOSE = 'Lose'
    IN_PROGRESS = 'In Progress'
    GAME_OVER = 'Game Over'

class Message(Enum):
    FirstTry = 'Amazing'
    SecondTry = 'Splendid'
    ThirdTry = 'Awesome'
    RemainderTry = 'Yay'

class PlayerResponse(Enum):
    Attempts = 'Attempts' 
    TallyResponse = 'Tally Response' 
    GameStatus = 'Game Status' 
    Message = 'Message'


def validate_length(guess): 
    if len(guess) != WORD_SIZE:
        raise ValueError("Word must be 5 letters")


def tally(target, guess):
    validate_length(guess)

    return [tallyForPosition(position, target, guess) for position in range(5)]

def tallyForPosition( position, target, guess):
    if (target[position] == guess[position]):
        return Matches.EXACT_MATCH
    
    letterAtPosition = guess[position]

    positionMatchesAmount = countPositionalMatches(target, guess, letterAtPosition)

    nonPositionalOccurrencesInTarget = countNumberOfOccurrencesUntilPosition(WORD_SIZE - 1, target, letterAtPosition) - positionMatchesAmount
    numberOfOccurancesInGuessUntilPosition = countNumberOfOccurrencesUntilPosition(position, guess, letterAtPosition)

    if (nonPositionalOccurrencesInTarget >= numberOfOccurancesInGuessUntilPosition):
        return Matches.PARTIAL_MATCH

    return Matches.NO_MATCH


def countPositionalMatches(target, guess, letter):
    return len([ i for i in range(5) if guess[i] == target[i] if guess[i] == letter])


def countNumberOfOccurrencesUntilPosition(position, word, letter):
    wordSubStr = word[0 : position + 1]

    return len([ i for i in range(position + 1) if wordSubStr[i] == letter])

def play(target, guess, attempt, is_spelling_correct=lambda word: True):
    validate_length(guess)

    if not is_spelling_correct(guess):
        raise ValueError("Not a word")

    results = {}

    results[PlayerResponse.Attempts] = attempt + 1

    results[PlayerResponse.TallyResponse] = tally(target, guess)

    results[PlayerResponse.GameStatus] = determineGameStatus(results.get(PlayerResponse.Attempts), results.get(PlayerResponse.TallyResponse))

    results[PlayerResponse.Message] = determineMessage(results.get(PlayerResponse.Attempts), results.get(PlayerResponse.GameStatus), target) 

    return results


def determineGameStatus(attempt, tallyResponse):
    if (tallyResponse == [Matches.EXACT_MATCH] * WORD_SIZE):
        return Status.WIN
    return Status.LOSE if attempt == 6 else Status.IN_PROGRESS


def determineMessage(attempt, gameStatus, target):
    if (gameStatus == Status.LOSE):
        return f"It was {target}, better luck next time" 

    messages = {1: "Amazing", 2: "Splendid", 3: "Awesome", 4: "Yay", 5: "Yay", 6: "Yay"} 
    
    return "" if gameStatus == Status.IN_PROGRESS else messages.get(attempt)
