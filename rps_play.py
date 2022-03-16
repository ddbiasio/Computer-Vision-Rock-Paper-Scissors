import time
import rps_game
import cv2
import numpy as np

def display_message(frame, message_text):
    if "\n" in message_text:
        starting_y, line_size = 50, 30
        for counter, line in enumerate(message_text.split('\n')):
            new_y = starting_y + counter*line_size
            cv2.putText(frame, line, (50, new_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    else:
        cv2.putText(frame, message_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.imshow('frame', frame)

def play_game():
 
    #initialise the video capture and the model
    vid_cap = cv2.VideoCapture(0)
    model = rps_game.rps_model('/home/siobhan/aicore/code/projects/rps/converted_keras/keras_model.h5')

    #initialise the game
    rps = rps_game.rps()

    time_elapsed = 0
    start_time = None

    while True:
        if rps.game_started:
            time_elapsed = round(time.time() - start_time)

        ret, frame = vid_cap.read()

        if not ret:
            print("The camera device could not be opened")
            break
        else:

            if time_elapsed  >= 6 and rps.game_started:
                if not rps.game_over:
                    # We only need to do this first time we hit this section of the loop
                    # Get the image of the user and read into data array
                    resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
                    image_np = np.array(resized_frame)
                    normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image                    
                    model.data[0] = normalized_image
                    
                    user_choice = model.get_prediction()
                    computer_choice = rps.get_computer_choice()
                    
                    game_result = rps.play(user_choice, computer_choice)

                # Print the results on the screen    
                display_message(frame, game_result)
        
            elif time_elapsed >= 3 and rps.game_started:
                time_interval = str(6 - time_elapsed)
                image_text = "GO!  Capturing image in " + time_interval + "..."
                display_message(frame, image_text)
            
            elif time_elapsed >= 2 and rps.game_started:
                display_message(frame, "SCISSORS")

            elif time_elapsed >= 1 and rps.game_started:
                display_message(frame, "PAPER")
            
            elif time_elapsed >= 0 and rps.game_started:
                display_message(frame, "ROCK")
            else:
                display_message(frame, rps.game_help_text)
            
            #Check pressed key
            pressed_key = cv2.waitKey(1) & 0xFF

            if pressed_key == ord('q'):
                break
            elif pressed_key == ord('s') or pressed_key == ord('b') or pressed_key == ord('f'):
                #start the game and set the game mode
                start_time = time.time()
                time_elapsed = 0
                rps.start_game(chr(pressed_key))
            elif pressed_key == ord('p'):
                start_time = time.time()
                time_elapsed = 0
                rps.reset_game()
                display_message(frame, rps.game_help_text)
            else:
                display_message(frame, "You pressed an invalid key.\n" + rps.game_help_text)

    # After the loop release the cap object
    vid_cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    play_game()