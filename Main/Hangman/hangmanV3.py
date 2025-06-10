import random
from Main.Hangman.listOfWords import words
from Main.Hangman.hangman_visual import lives_visual_dict
import string
import sys

difficulty_scale_1 = [3, 4, 5, 6]
difficulty_scale_2 = [7, 8, 9, 10]

def get_word1(words):
    word = random.choice(words)  # randomly chooses something from the list
    while '-' in word or ' ' in word or len(word) not in difficulty_scale_1:
        word = random.choice(words)

    return word.upper()

def get_word2(words):
    word = random.choice(words)  # randomly chooses something from the list
    while '-' in word or ' ' in word or len(word) not in difficulty_scale_2:
        word = random.choice(words)

    return word.upper()

def play():

    input("Welcome to Hangman, press \"Enter\" to play.")

    choices = [1, 2]
    
    level = int(input("enter 1 for easy enter 2 for hard:"))
    
    while level not in choices:
        level = int(input("enter 1 for easy enter 2 for hard:"))
    
    if level == 1:
        word = get_word1(words)
        
    else:
        word = get_word2(words)
        
    word_letters = set(word)  # letters in the word
    alphabet = set(string.ascii_uppercase)
    used_letters = set()  # what the user has guessed

    lives = 7
        
    # getting user input
    while len(word_letters) > 0 and lives > 0:
        # letters used
        # ' '.join(['a', 'b', 'cd']) --> 'a b cd'
        print('\n\n\n\nYou have', lives, 'lives left and you have used these letters: ', ' '.join(used_letters))

        # what current word is (ie W - R D)
        word_list = [letter if letter in used_letters else '-' for letter in word]
        print(lives_visual_dict[lives])
        print('Current word: ', ' '.join(word_list))

        user_letter = input('Guess a letter: ').upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
                print('\nGood job,', user_letter,"was in the word")

            else:
                lives = lives - 1  # takes away a life if wrong
                print('\nYour letter,', user_letter, 'is not in the word.')

        elif user_letter in used_letters:
            print('\nYou have already used that letter. Guess another letter.')

        else:
            print('\nThat is not a valid letter.')

    # gets here when len(word_letters) == 0 OR when lives == 0
    if lives == 0:
        print(lives_visual_dict[lives])
        print('You died, sorry. The word was', word)
    else:
        print('YAY! You guessed the word', word, '!!')

def main2():
    play()
    while True:    
        try_again = input("Try again? (Y/N)").strip().upper()
        if try_again == 'Y' or 'N':
            if try_again == 'N':
                sys.exit()
            elif try_again == 'Y':
                play()
        else:
            while try_again.strip().upper() != 'Y' or 'N':
                try_again = input("Try again? (Y/N)").strip().upper()
            if try_again == 'N':
                sys.exit()
            else:
                play()
                
main2()