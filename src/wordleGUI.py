import pygame
import sys
from wordle import *
from pygame import *
from agilec_randomWord_service import *
from agilec_spellcheck_service import *
from guessButton import *

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wordle')
FONT = pygame.font.Font(None, 56)

FPS = 60
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (106, 170, 100)
YELLOW = (201, 180, 88)
GRAY = (120, 124, 126)
DARK_MODE_BLACK = (18, 18, 18)
USED_LETTER_COLOR= (50, 50, 50)

guessed_letters = {'correct': set(), 'present': set(), 'absent': set()} 
MAX_LETTERS = 5
MAX_GUESSES = 6

class Button:
    def __init__(self, x_pos, y_pos, width, height, color, text = '', text_color = (0, 0, 0), font_size = 30):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.color = color

        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.font = pygame.font.Font(None, self.font_size)
        self.action = None

        self.is_animating = False
        self.animation_time = 0
        self.original_color = color
        self.click_color = USED_LETTER_COLOR

    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x_pos, self.y_pos, self.width, self.height))

        if self.text != '':
            text = self.font.render(self.text, True, self.text_color)
            text_rect = text.get_rect(center=(self.x_pos + self.width / 2, self.y_pos + self.height / 2))
            screen.blit(text, text_rect)
    
    def update(self, delta_time):
        if self.is_animating:
            self.animation_time -= delta_time
            if self.animation_time <= 0:
                self.is_animating = False
                self.color = self.original_color
            else:
                self.color = self.click_color

    def animate_click(self):
        self.is_animating = True
        self.animation_time = 180
    
    
    def is_clicked(self, mouse_pos, event):
        if (self.x_pos < mouse_pos[0] < self.x_pos + self.width) and (self.y_pos < mouse_pos[1] < self.y_pos + self.height) and event.type == MOUSEBUTTONDOWN:
            return True
        return False
    

class Wordle_Gui:

    def __init__(self):

        self.target = pick_randomWord()
        self.savedPreviousTallys = []
        self.savedPreviousGuesses = []
        self.current_guess = ""
        self.attemptCount = 0
        self.guessResult = {}

        self.guess_button = Button(492, 700, 80, 60, USED_LETTER_COLOR, "GUESS", WHITE, 30)
        self.restart_button = Button (250, 450, 120, 70, GRAY, "Restart", WHITE, 45)

        self.gameOver = False
        self.resetGame()

    def resetGame(self):
        global guessed_letters
        guessed_letters = {'correct': set(), 'present': set(), 'absent': set()}
        self.target = pick_randomWord()
        self.savedPreviousTallys = []
        self.savedPreviousGuesses = []
        self.current_guess = ""
        self.attemptCount = 0
        self.guessResult = {}
        self.gameOver = False


    def isTheGameOver(self):
        return self.guessResult.get(PlayerResponse.GameStatus) != Status.IN_PROGRESS

    def handle_guess_action(self):
        self.guess_button.animate_click()
        if len(self.current_guess) == MAX_LETTERS:
            self.handleEventKeydown_userSubmitGuess()

    def handle_restart_action(self):
        self.restart_button.animate_click()
        self.resetBoard()

    def handle_mouse_click(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.restart_button.is_clicked(mouse_pos, event) and self.gameOver:
            self.handle_restart_action()
        else:
            self.handle_guess_action()  

    def handlePyGameEventType(self, event):
        if event.type == QUIT:
            self.quitTheGame()

        elif event.type == MOUSEBUTTONDOWN:
            self.handle_mouse_click(event)

        elif event.type == KEYDOWN:
            self.handleEventKeydown_KeyType(event)

    def handleEventKeydown_KeyType(self, event):
        if event.key == K_RETURN and len(self.current_guess) == MAX_LETTERS:
            self.handleEventKeydown_userSubmitGuess()

        else:
            self.handleEventKeydown_Backspace_Alpha(event)


    def handleEventKeydown_Backspace_Alpha(self, event):

        if event.key == K_BACKSPACE and len(self.current_guess) > 0:

            self.current_guess = self.current_guess[:-1]
            self.update_guess_button_state()
        else:
            self.handleEventKeydown_UserInput_Alpha(event)


    def quitTheGame(self):
        pygame.quit
        sys.exit()


    def handleEventKeydown_userSubmitGuess(self):
        if spellcheck(self.current_guess):
            self.guessResult = play(self.target, self.current_guess, self.attemptCount)
            self.savedPreviousGuesses.append(self.current_guess)
            self.savedPreviousTallys.append(self.guessResult.get(PlayerResponse.TallyResponse))
            self.updateGuessedLetters()

            if self.isTheGameOver():
                self.gameOver = True

            self.resetGuess()
        else:
            print("Not a word")


    def resetGuess(self):
        self.attemptCount += 1
        self.current_guess = ""
        self.guess_button.color = USED_LETTER_COLOR


    def updateGuessedLetters(self):
        for i, letter in enumerate(self.current_guess):
            if letter == self.target[i]:  
                guessed_letters['correct'].add(letter)

            elif letter in self.target:
                guessed_letters['present'].add(letter)

            else:
                guessed_letters['absent'].add(letter)


    def handleEventKeydown_UserInput_Alpha(self, event):

        if event.unicode.isalpha() and len(self.current_guess) < MAX_LETTERS:
            self.current_guess += event.unicode.upper()
            self.update_guess_button_state()

        elif event.unicode.isalpha() and len(self.current_guess) == MAX_LETTERS:
            self.update_guess_button_state()


    def draw_letter_boxes(self):
        box_size = 60  
        box_margin = 20  
        start_x = (SCREEN_WIDTH - (MAX_LETTERS * (box_size + box_margin) - box_margin)) // 2
        start_y = 60

        for i in range(MAX_GUESSES):
            for j in range(MAX_LETTERS):
                box_x = start_x + j * (box_size + box_margin)
                box_y = start_y + i * (box_size + box_margin)
                pygame.draw.rect(SCREEN, GRAY, (box_x, box_y, box_size, box_size), 3)
    

    def draw_guesses(self):
        box_size = 60  
        box_margin = 20  
        start_x = (SCREEN_WIDTH - (MAX_LETTERS * (box_size + box_margin) - box_margin)) // 2  
        start_y = 60  
        
        for i, previousGuess in enumerate(self.savedPreviousGuesses):
            tally = self.savedPreviousTallys[i]
            for j, letter in enumerate(previousGuess):
                letter_color = BLACK  

                if tally[j] == Matches.EXACT_MATCH:
                    box_color = GREEN
                elif tally[j] == Matches.PARTIAL_MATCH:
                    box_color = YELLOW
                else:
                    box_color = GRAY

                letter_color = WHITE  

                letter_x = start_x + j * (box_size + box_margin)
                letter_y = start_y + i * (box_size + box_margin)
                
                pygame.draw.rect(SCREEN, box_color, (letter_x, letter_y, box_size, box_size))
                
                text = FONT.render(letter, True, letter_color)
                text_rect = text.get_rect(center=(letter_x + box_size / 2, letter_y + box_size / 2))
                SCREEN.blit(text, text_rect)


    def draw_keyboard(self, guessed_letters):
        key_width = 50  
        key_height = 60  
        key_margin = 5  
        start_keyboard_x = 20  
        start_keyboard_y = SCREEN_HEIGHT - 230  

        keyboard_rows = [
            " QWERTYUIOP",
            "  ASDFGHJKL ",
            "     ZXCVBNM  "
        ]

        color_map = {
            'correct': GREEN,
            'present': YELLOW,
            'absent': USED_LETTER_COLOR
        }

        for row_idx, row in enumerate(keyboard_rows):
            for key_idx, key in enumerate(row.strip()):
                key_x = start_keyboard_x + key_idx * (key_width + key_margin) + (len(row) - len(row.strip())) * key_width / 4
                key_y = start_keyboard_y + row_idx * (key_height + key_margin)

                key_color = GRAY  
                for state, keys in guessed_letters.items():
                    if key in keys:
                        key_color = color_map[state]
                        break

                pygame.draw.rect(SCREEN, key_color, (key_x, key_y, key_width, key_height))
                letter_text = FONT.render(key, True, WHITE)
                SCREEN.blit(letter_text, (key_x + (key_width - letter_text.get_width()) / 2, key_y + (key_height - letter_text.get_height()) / 2))


    def draw_current_guess(self):
        box_size = 60
        box_margin = 20
        start_x = (SCREEN_WIDTH - (MAX_LETTERS * (box_size + box_margin) - box_margin)) // 2
        current_guess_y = 60 + len(self.savedPreviousGuesses) * (box_size + box_margin) 
        
        for j, letter in enumerate(self.current_guess):
            letter_x = start_x + j * (box_size + box_margin)
            
            text = FONT.render(letter, True, WHITE)
            text_rect = text.get_rect(center=(letter_x + box_size / 2, current_guess_y + box_size / 2))
            SCREEN.blit(text, text_rect)


    def displayEndOfGameMessage(self):
        SCREEN.fill(DARK_MODE_BLACK) 

        message = self.guessResult.get(PlayerResponse.Message)

        font_size = 100
        text = pygame.font.Font(None, font_size).render(message, True, WHITE)

        while text.get_width() > SCREEN_WIDTH - 40: 
            font_size -= 1
            text = pygame.font.Font(None, font_size).render(message, True, WHITE)

        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(text, text_rect)

        self.restart_button.draw(SCREEN)


        pygame.display.update()
        

    def resetBoard(self):
        self.resetGame()
        self.gameOver = False

    def draw_components(self):
        self.draw_letter_boxes()
        self.draw_guesses()
        self.draw_current_guess()
        self.guess_button.draw(SCREEN)


    def update_guess_button_state(self):
        if len(self.current_guess) == MAX_LETTERS:
            self.guess_button.color = GRAY
        else:
            self.guess_button.color = USED_LETTER_COLOR


def main():
    global  guessed_letters

    game = Wordle_Gui()

    last_time = pygame.time.get_ticks()

    while True:
        SCREEN.fill(DARK_MODE_BLACK)
        current_time = pygame.time.get_ticks()
        delta_time = current_time - last_time
        last_time = current_time

        for event in pygame.event.get():
            game.handlePyGameEventType(event)
            
           
        game.guess_button.update(delta_time)

        if not game.gameOver:
            game.draw_components() 
            game.draw_keyboard(guessed_letters)
            
        else:
            game.displayEndOfGameMessage()

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
