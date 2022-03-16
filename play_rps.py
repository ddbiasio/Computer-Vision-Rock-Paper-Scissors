import cv2
from keras.models import load_model
import numpy as np
import time

#initialise variables which control the flow of the game
computer_wins = 0
user_wins = 0
game_over = False
match_over = False
game_mode = ""
    
def who_won(user_choice, computer_choice):
    global computer_wins
    global user_wins

    if user_choice == computer_choice:
        return "The result is a draw"
    elif user_choice == 'rock':
        if computer_choice == 'scissors':
            user_wins = user_wins + 1
            return "Rock sharpens scissors: you win"
        elif computer_choice == 'paper':
            computer_wins = computer_wins + 1
            return "Paper wraps rock: computer wins"
        else:
            return "The computer's selection could not be processed"
    elif user_choice == 'scissors':
        if computer_choice == 'paper':
            user_wins = user_wins + 1
            return "Scissors cut paper=: you win"
        elif computer_choice == 'rock':
            computer_wins = computer_wins + 1
            return "Rock sharpens scissors: computer wins"
        else:
            return "The computer's selection could not be processed"
    elif user_choice == 'paper':
        if computer_choice == 'scissors':
            computer_wins = computer_wins + 1
            return "Scissors cut paper=: computer wins"
        elif computer_choice == 'rock':
            user_wins = user_wins + 1
            return "Rock sharpens scissors: you win"
        else:
            return "The computer's selection could not be processed"
    else:
        return "Your selection could not be processed"

def get_computer_choice():
    import random   
    rps_list = ['rock', 'paper', 'scissors']
    return random.choice(rps_list)  

def get_user_choice(prediction_data):
    if prediction_data[0][0] > 0.85:
        return 'rock'
    elif prediction_data[0][1] > 0.85:
        return 'paper'
    elif prediction_data[0][2] > 0.85:
        return 'scissors'
    else:
        return 'nothing'

def compare_the_choices(user_choice, computer_choice):

    global computer_wins
    global user_wins
    global match_over
    global game_mode

    winner = who_won(user_choice, computer_choice)

    if game_mode == "f":
        # Check if a user has reached 3 and declare them the winner
        if computer_wins == 3:
            match_over = True
            overall_winner = 'Computer'
        elif user_wins == 3:
            overall_winner = 'You'
            match_over = True
        results_text = ("You: " + user_choice
                                + "\nComputer: " + computer_choice
                                + "\nResult: " + winner
                                + "\nYour score: " + str(user_wins) 
                                + "\nComputer score: " + str(computer_wins))
        if match_over:
            results_text = (results_text
                                        + "\nThe overall winner is: " + overall_winner)
        results_text = (results_text
                                + "\nPress 'p' to play again, 'r' to reset, or 'q' to quit")
    elif game_mode == "b":
        # Check  if 3 games have been played and who has most wins
        results_text = ("You: " + user_choice
                                + "\nComputer: " + computer_choice
                                + "\nYour score: " + str(user_wins) 
                                + "\nComputer score: " + str(computer_wins)
                                + "\nResult: " + winner)
        if user_wins + computer_wins == 3:
            if user_wins > computer_wins:
                overall_winner = 'You'
                match_over = True
            else:
                match_over = True
                overall_winner = 'Computer'
        
        if match_over:
            results_text = (results_text
                                        + "\nThe overall winner is: " + overall_winner)
        results_text = (results_text
                                + "\nPress 'p' to play again or 'q' to quit")
    else:
        # single match display winner
        results_text = ("You: " + user_choice
                        + "\nComputer: " + computer_choice
                        + "\nResult: " + winner
                        + "\nPress 'p' to play again or 'q' to quit")

    return results_text

def play_rps():

    global game_over
    global game_mode
    global match_over
    global computer_wins
    global user_wins
 
    start_time = time.time()
    game_started = False
    time_elapsed = 0

    #initialise the model, video capture and data array for the image
    model = load_model('/home/siobhan/aicore/code/projects/rps/converted_keras/keras_model.h5')
    cap = cv2.VideoCapture(0)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    while True:
        if game_started:
            time_elapsed = round(time.time() - start_time)

        ret, frame = cap.read()
        if not ret:
            print("The camera device could not be opened")
            break
        else:
 
            if time_elapsed  >= 6 and game_started:
                if not game_over:
                    # We only need to do this first time we hit this section of the loop
                    # Get the image of the user and read into data array
                    resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
                    image_np = np.array(resized_frame)
                    normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
                    data[0] = normalized_image

                    prediction = model.predict(data)
                    user_choice = get_user_choice(prediction)
                    computer_choice = get_computer_choice() 

                    results_text = compare_the_choices(user_choice, computer_choice)
                    game_over = True

                # Print the results on the screen    
                starting_y, line_size = 50, 30
                for counter, line in enumerate(results_text.split('\n')):
                    new_y = starting_y + counter*line_size
                    cv2.putText(frame, line, (50, new_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            elif time_elapsed >= 3 and game_started:
                time_interval = str(6 - time_elapsed)
                image_text = "GO!  Capturing image in " + time_interval + "..."
                cv2.putText(frame, image_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            elif time_elapsed >= 2 and game_started:
                cv2.putText(frame, "SCISSORS", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            elif time_elapsed >= 1 and game_started:
                cv2.putText(frame, "PAPER", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            elif time_elapsed >= 0 and game_started:
                cv2.putText(frame, "ROCK", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            else:
                help_text = ("Select game mode or 'q' to quit."
                            + "\nSingle round (s)"
                            + "\nFirst to 3 wins (f)"
                            + "\nBest of 3 wins (b)")
                starting_y, line_size = 50, 30
                for counter, line in enumerate(help_text.split('\n')):
                    new_y = starting_y + counter*line_size
                    cv2.putText(frame, line, (50, new_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            cv2.imshow('frame', frame)
 
            #Check pressed key
            pressed_key = cv2.waitKey(1) & 0xFF

            if pressed_key == ord('q'):
                break
            elif pressed_key == ord('s') or pressed_key == ord('b') or pressed_key == ord('f'):
                #start the game and set the game mode
                game_started = True
                start_time = time.time()
                time_elapsed = 0
                game_over = False
                match_over = False
                game_mode = chr(pressed_key)
                computer_wins = 0
                user_wins = 0
            elif pressed_key == ord('p'):
                #restarts match or game
                time_elapsed = 0
                game_over = False
                if game_mode in ('b', 'f') and not match_over:
                    start_time = time.time()
                    game_started = True
                else:
                    game_started = False
                    start_time = 0
                    game_mode = ""
                    match_over = False
                    computer_wins = 0
                    user_wins = 0

    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

play_rps()
