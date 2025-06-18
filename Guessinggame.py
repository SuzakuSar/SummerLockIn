#intro
import sys
def guessing_game(): 
    start = ""
    start = input("Welcome to the guessing game! Press enter to play.")

#choosing difficulty

    level_choices = [1,2]
    level = float(input("Enter \"1\" for normal difficulty, or \"2\" for hard difficulty:"))

    
    if level not in level_choices:
        level = float(input("Choose 1 or 2."))
        if level not in level_choices:
            level = float(input("Stop it."))
            while level not in level_choices:
                if level not in level_choices:
                    level = float(input("Sotp"))
    Guess = ""
        
#attempts
    
    num_of_attempts = 0
    attempts = set()

#random numbers

    import random
    normal_level = random.randint(0,21)
    hard_level = random.randint(0,31)
    normal_range = range(0,21)
    hard_range = range(0,31)

#hard difficulty level
        
    if level == 2:
        print("Guess a number from 0 to 30:")
        while Guess != hard_level:
            try:
                Guess = int(input())
            except ValueError:
                print("Try typing in a number:")
                continue
            if Guess == hard_level:        
                num_of_attempts = num_of_attempts + 1
                attempts.add(Guess)
                print("\nNice you got it! The number was: " + str(hard_level)+ ". It took you " + str(num_of_attempts) + " attempts.")
                print("Your attempts were: " + str(attempts))
                attempts.clear()
                pass
            else:
                if Guess not in hard_range: 
                    print("That's not an option dummy.")
                elif Guess > hard_level:
                    print("lower:")
                    attempts.add(Guess)
                    num_of_attempts = num_of_attempts + 1
                elif Guess < hard_level:
                    print("Higher:")
                    attempts.add(Guess)
                    num_of_attempts = num_of_attempts + 1
                else:
                    break

#normal difficulty level           
        
    elif level == 1:
        print("Guess a number from 0 to 20:")
        while Guess != normal_level:
            try:
                Guess = int(input())
            except ValueError:
                print("Try typing in a number:")
                continue
            if Guess == normal_level:        
                attempts.add(Guess)
                num_of_attempts = num_of_attempts + 1
                print("\nNice you got it! The number was: " + str(normal_level) + ". It took you " + str(num_of_attempts) + " attempts.")
                print("Your attempts were: " + str(attempts))
                attempts.clear
                pass
            else:
                if Guess not in normal_range:
                    print("That's not an option you dummy.")
                elif Guess > normal_level:
                    print("lower:")
                    attempts.add(Guess)
                    num_of_attempts = num_of_attempts + 1
                elif Guess < normal_level:
                    print("Higher:")
                    attempts.add(Guess)
                    num_of_attempts = num_of_attempts + 1
                else:
                    break     
    else:
        pass

#try again

def main():
    guessing_game()
    while True:    
        try_again = input("Try again? (Y/N)").strip().upper()
        if try_again == 'Y' or 'N':
            if try_again == 'N':
                sys.exit()
            elif try_again == 'Y':
                guessing_game()
        else:
            while try_again.strip().upper() != 'Y' or 'N':
                try_again = input("Try again? (Y/N)").strip().upper()
            if try_again == 'N':
                sys.exit()
            else:
                guessing_game()
                
main()
