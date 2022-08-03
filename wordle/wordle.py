import random

def main():
    words = []
    try:
        # with automaticly closes the file
        with open("list") as file:
            # [:-1] to remove \n from the lines
            words = [x[:-1] for x in file.readlines()]
    except IOError:
        print("dictionary not found")
        return
    # random module has a function for random item in array
    word_to_guess = random.choice(words)
    # sets are more efficient for contains
    words = set(words)
    max_guesses = 6
    guesses_left = max_guesses
    # loop until the person doesn't have any guesses left
    while guesses_left != 0:
        try:
            guess = input("guess: ")
        # exception will be thrown if Ctrl+c is pressed
        except KeyboardInterrupt:
            print(f"\nThe right answer was: {word_to_guess}")
            return
        if guess in words:
            # python doesn't have the -- operator
            guesses_left -= 1
            colors = colorify(guess, word_to_guess)
            # pythons print is like System.out.println()
            # if you don't want a new line change the end to an empty string
            print(f"  {max_guesses - guesses_left}/{max_guesses}: ", end="")
            for co, gc in zip(colors, guess):
                print(f"{co}{gc}", end="")
            # resets color
            print("\033[39;49m")
            if guess == word_to_guess:
                print("\033[92;49mCongratulations!\033[39;49m")
                return
        else:
            print(f"\033[31;49m{guess}\033[39;49m: is not a valid word!")
    print(f"You are out of guesses. The right answer was: {word_to_guess}")

# YES, you can also write weird, unreadable and bad code in python
def colorify(guess, word):
    guess = list(guess)
    word = list(word)
    color = [None] * len(guess)
    for i in range(len(guess)):
        if guess[i] == word[i]:
            # green escape code
            color[i] = "\033[97;102m"
            word[i] = None
            guess[i] = None
    for i in range(len(guess)):
        if guess[i] is not None:
            try:
                word[word.index(guess[i])] = None
                # yellow or orange
                color[i] = "\033[97;43m"
            except ValueError:
                # black
                color[i] = "\033[97;40m"
    return color

# if the python script was executed directly, then call main()
if __name__ == "__main__":
    main()
