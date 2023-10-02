import streamlit as st
import random


def outcome(user_selection):
    """
    This function is responsible for the game. It will first create all
    variable (i.e., user_/computer_points, computer_selections) for use
    in the function. It will then generate the computer selection and
    work through the logic of who wins.

    The function returns three values before exiting:
      * The message to print for the user RE: who won
      * A binary representing the user's win/loss
      * A binary representing the computer's win/loss
    """

    # set points to zero for the instance
    user_point = 0
    computer_point = 0

    # these are the computer's options
    computer_selections = {
        1: 'rock',
        2: 'paper',
        3: 'scissors'
    }
    
    # this makes a random selection for the computer
    computer_selection = computer_selections[random.randint(1, 3)]
    
    # now, we determine the outcome and increment scores
    if user_selection == computer_selection:
        outcome_message = "It's a tie."
    else:
        if user_selection == 1: # user selected rock
            if computer_selection == 'paper':
                outcome_message = "I chose paper. You lose."
                computer_point = 1

            else:
                outcome_message = "I chose scissors. You win!"
                user_point = 1
        elif user_selection == 2: # user selected paper
            if computer_selection == 'rock':
                outcome_message = "I chose rock. You win!"
                user_point = 1
            else:
                outcome_message = "I chose scissors. You lose."
                computer_point = 1
        else: # user selected scissors
            if computer_selection == 'paper':
                outcome_message = "I chose paper. You win!"
                user_point = 1
            else:
                outcome_message = "I chose rock. You lose."
                computer_point = 1

    return outcome_message, user_point, computer_point


def get_scores():
    """
    Fetches the latest scores from scores.txt
    """
    with open('score.txt', 'r') as file:
        return file.readlines()

def record_scores(scores):
    """
    Writes the latest scores to scores.txt.
    """
    with open('score.txt', 'w') as file:
        file.write(scores)

def reset_game():
    """
    Right now, this resets score.txt to 0-0.
    """
    with open('score.txt', 'w') as file:
        file.write("0\n0")


# +------------+
# |  HEADINGS  |
# +------------+

st.title("Margot & Andi's Rock, Paper, Scissors Game")

# +------------+
# | SCOREBOARD |
# +------------+

try:
    current_score = get_scores()
    user_score = int(current_score[1])
    computer_score = int(current_score[2])
    st.subheader(f"You: {user_score} | Computer: {computer_score}")

    if "You win" in current_score[0]:
        st.info(current_score[0], icon="👍")
    else:
        st.error(current_score[0], icon="👎")

except IndexError:
    # set the scores to 0 by default
    user_score = 0
    computer_score = 0
    # write two lines to score.txt
    updated_scores = f"{user_score}\n{computer_score}"
    record_scores(updated_scores)
    # show the score to the user
    st.subheader(f"You: {user_score} | Computer: {computer_score}")

st.divider()

# +------------+
# |  GAMEPLAY  |
# +------------+

st.write("Select an option to play:")

# the user can select from three buttons
user_options = ['rock', 'paper', 'scissors']

for index, user_option in enumerate(user_options):
    # make the buttons dynamically
    button = st.button(user_option, key=user_option)
    
    if button:
        # get the outcome
        results = outcome(index + 1)
        message_to_user = results[0]

        # get the current store if it exists
        current_score = get_scores()

        # calculate the new scores
        try:
            new_user_score = int(current_score[1]) + results[1]
            new_computer_score = int(current_score[2]) + results[2]
        except IndexError:
            new_user_score = int(current_score[0]) + results[1]
            new_computer_score = int(current_score[1]) + results[2]
        updated_scores = f"{results[0]}\n{new_user_score}\n{new_computer_score}"
        
        # write the message and scores to score.txt
        record_scores(updated_scores)

        # update the session state
        st.rerun()