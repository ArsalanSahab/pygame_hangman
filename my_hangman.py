
#### Important Imports ####

import pygame as pg
import random



#### Pygame initialising (Windows , etc) ####


# Initialise Pygame

pg.init()

# Window Height and Width

win_height = 500
win_width = 700

# Initialise the window

window = pg.display.set_mode((win_width,win_height))


##### Global Variables #####


# Colours


BLACK = (0,0, 0)
WHITE = (255,255,255)
RED = (255,0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHT_BLUE = (102,255,255)


# Settings Fonts


button_font = pg.font.SysFont("arial",20)
guess_btn_font = pg.font.SysFont("monospace",24)
lost_font = pg.font.SysFont("arial",50)

# Initialising variables and lists to store words , buttons and etc

words = ''
buttons = []
guesses = []

game_pics = pg.image.load('img/hangman0.png'),pg.image.load('img/hangman1.png'),pg.image.load('img/hangman2.png'),pg.image.load('img/hangman3.png'),pg.image.load('img/hangman4.png'),pg.image.load('img/hangman5.png'),pg.image.load('img/hangman6.png')

body_parts = 0




##### Drawing the game window again #####

def game_window():

    #import globals vars

    global guesses, game_pics,body_parts

    # Fill window with a colour

    window.fill(GREEN)

    # Drawing buttons

    for i in range(len(buttons)) :

        if buttons[i][4] :

            # draw Circle Button 1

            pg.draw.circle(window, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])

            # draw Circle button 2
            pg.draw.circle(window, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2)

            # draw a lable on the window
            label = button_font.render(chr(buttons[i][5]), 1, BLACK)
            window.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))


    ## Call space area and fill with guesses and create rectangles

    space_area = space_filler(words, guesses)
    label_1 = guess_btn_font.render(space_area, 1, BLACK)
    rect = label_1.get_rect()
    length = rect[2]


    # Draw rectangle spaces

    window.blit(label_1, (win_width / 2 - length / 2, 400))




    # Load hangman

    pic = game_pics[body_parts]
    window.blit(pic, (win_width / 2 - pic.get_width() / 2 + 20, 150))

    # Update display

    pg.display.update()


#### Function to get the random word ####


def get_random_word():


    # Open the words file

    file = open('my_words.txt')

    file_reader = file.readlines()

    random_word = random.randrange(0, len(file_reader) - 1)

    return file_reader[i][:-1]




#### Create function to check if guessed word in correct ####


def word_checker(user_guess):



    ## import globals

    global words

    if user_guess.lower() not in words.lower():

        return True
    return False







#### Function to fill spacesand fill with guessed words ####

def space_filler(words,guesses=[]) :



    space = ''

    guess_word = guesses

    for x in range(len(words)) :

        if words[x] != ' ' :

            space += '_ '

            for i in range(len(guesses)):

                if words[x].upper() == guesses[i]:
                    space = space[:-2]
                    space += words[x].upper() + ' '
        elif words[x] == ' ':
            space += ' '
        return space




#### Define a function which does actions when button pressed , button == A-Z ####


def button_pressed(x_cord,y_cord) :


    for i in range(len(buttons)) :

        if x_cord < buttons[i][1] + 20 and x_cord > buttons[i][1] - 20:

            if y_cord < buttons[i][2] + 20 and y_cord > buttons[i][2] - 20:

                return buttons[i][5]
    return None




#### Define function when player loses ####

def game_lost(winner=False) :


    # import global

    global body_parts


    losing_string = 'You Lost, press any key to play again...'
    winnner_string = 'WINNER!, press any key to play again...'


    # Re-run game

    game_window()
    pg.time.delay(1000)
    window.fill(GREEN)



        # Print text corresponding text

    if winner == True:
        label = lost_font.render(winnner_string, 1, BLACK)
    else:
        label = lost_font.render(losing_string, 1, BLACK)


        # Variable to show what the word was

    word_string = lost_font.render(words.upper(), 1, BLACK)
    wordWas = lost_font.render('The phrase was: ', 1, BLACK)

    window.blit(word_string, (win_width / 2 - word_string.get_width() / 2, 295))
    window.blit(wordWas, (win_width / 2 - wordWas.get_width() / 2, 245))
    window.blit(label, (win_width / 2 - label.get_width() / 2, 140))
    pg.display.update()
    again = True


    while again:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                again = False

    reset_game()



#### Funcion to reset everything ####

def reset_game() :

    global body_parts
    global guesses
    global buttons
    global words


    for i in range(len(buttons)):
        buttons[i][4] = True

    body_parts = 0
    guessed = []
    word = get_random_word()



##### MAIN GAME_FLOW #####



increase = round(win_width / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([LIGHT_BLUE, x, y, 20, True, 65 + i])
    # buttons.append([color, x_pos, y_pos, radius, visible, char])

words = get_random_word()
playing = True


#### While playing is true draw the game and call events ####


while playing:
    game_window()
    pg.time.delay(10)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            inPlay = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                inPlay = False
        if event.type == pg.MOUSEBUTTONDOWN:
            clickPos = pg.mouse.get_pos()
            letter = button_pressed(clickPos[0], clickPos[1])
            if letter != None:
                guesses.append(chr(letter))
                buttons[letter - 65][4] = False
                if word_checker(chr(letter)):
                    if body_parts != 5:
                        body_parts += 1
                    else:
                        game_lost()
                else:
                    print(space_filler(words, guesses))
                    if space_filler(words, guesses).count('_') == 0:
                        game_lost(True)

pg.quit()










