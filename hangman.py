from hangman_helper import *


def update_word_pattern(word, pattern, letter):
    """The function update the pattern of the word"""
    update_pattern = ""
    for i in range(len(word)):
        if word[i] == letter:
            update_pattern += letter
        else:
            update_pattern += pattern[i]
    return update_pattern


def gen_full_pattern(word, pattern):
    """The function fill the pattern when the guess is right"""
    for i in word:
        letter = i
        pattern = update_word_pattern(word, pattern,
                                     letter)
    return pattern


def run_single_game(word_list, score):
    """The most important function in code.
    The function get the initial word list and score and the game starts.
    A player need to choose what he want to insert a word, a letter or get a hint.
    Based on player's choice the function print different messages"""
    word = get_random_word(word_list)
    wrong_guess_lst = []
    points = score
    pattern = '_' * len(word)
    msg = "The game is started!"
    while not is_game_over(points, pattern):
        display_state(pattern, wrong_guess_lst, points, msg)
        value = get_input()
        if value[0] == LETTER:
            pattern, points, msg = choice_is_letter(value[1], wrong_guess_lst, pattern, word, points, msg)

        if value[0] == WORD:
            pattern, points, msg = choice_is_word(value[1], pattern, points, word, msg)

        if value[0] == HINT:
            points, msg = choice_is_hint(pattern, wrong_guess_lst, word_list, points, msg)

    if points > 0:
        msg = "You win!"
    else:
        msg = "You loosed! The right word was: " + word + '.'
    display_state(pattern, wrong_guess_lst, points, msg)
    return points


def choice_is_letter(letter, wrong_guess_lst, pattern, word, points, msg):
    """The function which makes different operation if a player
     chooses to write a letter"""
    if letter_wrong(letter) is False:
        msg = 'The letter is invalid'
    elif letter in wrong_guess_lst or letter in pattern:
        msg = 'This letter has already been selected'
    elif letter in word:
        points -= 1
        msg = 'The guess correct'
        pattern = update_word_pattern(word, pattern, letter)
        points = points + word.count(letter) * (word.count(letter) + 1) // 2
    else:
        points -= 1
        if points >= 0:
            msg = "Let's try again"
            wrong_guess_lst.append(letter)
    return pattern, points, msg


def choice_is_word(inserted_word, pattern, points, word, msg):
    """The function which makes different operation if a player
     chooses to write a word"""
    if word_wrong(inserted_word) is False:
        msg = 'The word is invalid'
    elif inserted_word == word:
        points -= 1
        points = count_points(inserted_word, pattern, points)
        pattern = gen_full_pattern(inserted_word, pattern)
    elif inserted_word != word:
        msg = "Unfortunately the word is not right"
        points = points - 1
    return pattern, points, msg


def choice_is_hint(pattern, wrong_guess_lst, word_list, points, msg):
    """The function which makes different operation if a player
     chooses a hint"""
    points -= 1
    msg = ''
    filtered_right_words = []
    right_words = filter_words_list(word_list, pattern,
                                    wrong_guess_lst)
    len_of_right_words = len(right_words)
    if len_of_right_words > HINT_LENGTH:
        for i in range(HINT_LENGTH):
            position_in_list = i * len_of_right_words // HINT_LENGTH
            filtered_right_words.append(right_words[position_in_list])
    else:
        filtered_right_words = right_words
    show_suggestions(filtered_right_words)
    return points, msg


def count_points(value, pattern, points):
    """Auxiliary function which helps to count points when
    a player enter the whole word, but he already guessed some of the letters"""
    right_letter = 0
    for i in value:
        if i not in pattern:
            right_letter += 1
    points = points + right_letter * (right_letter + 1) // 2
    return points


def is_game_over(points, pattern):
    """Terms of the end of the game"""
    return points == 0 or pattern.find('_') == -1


def letter_wrong(value):
    """Auxiliary function which check if the letter is validity"""
    return len(value) == 1 and value.isalpha() and value.islower()


def word_wrong(value):
    """Auxiliary function which checks if the word is valid."""
    return value.isalpha() and value.islower()


def filter_words_list(words, pattern, wrong_guess_lst):
    """Auxiliary function which return list of words
    which could be match as a hint"""
    right_words = list()
    wrong_words_list = list()
    for i in words:
        if len(i) == len(pattern):
            right_words.append(i)
    for j in range(len(right_words)-1):
        for k in right_words[j]:
            if k in wrong_guess_lst:
                wrong_words_list.append(right_words[j])
                break
    for word in wrong_words_list:
        if word in right_words:
            right_words.remove(word)
    for word in right_words[:]:
        for index, letter in enumerate(pattern):
            if letter != '_' and pattern[index] != word[index]:
                right_words.remove(word)
                break
    right_words = compare_place_of_letter(right_words, pattern)
    return right_words


def compare_place_of_letter(words, pattern):
    list_of_right_words = []
    for word in words:
        for char in pattern:
            if char != "_":
                places_in_word = get_places_of_char(word, char)
                places_in_pattern = get_places_of_char(pattern, char)
                if places_in_pattern == places_in_word:
                    list_of_right_words.append(word)
    return list_of_right_words


def get_places_of_char(word, char):
    index_of_chars = []
    for i in range(len(word)):
        if word[i] == char:
            index_of_chars.append(i)
    return index_of_chars


def main():
    """The main function which called to run_single_game and ask
    if you want to play again or not"""
    counter_games = 1
    word_list = load_words()
    game_score = POINTS_INITIAL
    do_play_game = True
    while do_play_game is True:
        game_score = run_single_game(word_list, game_score)
        msg_game = ('Your current points: ' + str(
            game_score) + '. You played already: ' + str(
            counter_games) + ' games' + '. Do you want to play again?')
        if game_score == 0:
            game_score = POINTS_INITIAL
        do_play_game = play_again(msg_game)
        counter_games += 1


if __name__ == '__main__':
    main()
