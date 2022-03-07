def who_won(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "The result is a draw"
    elif user_choice == 'rock':
        if computer_choice == 'scissors':
            return "Rock sharpens scissors: you win"
        elif computer_choice == 'paper':
            return "Paper wraps rock: computer wins"
        else:
            return "The computer's selection could not be processed"
    elif user_choice == 'scissors':
        if computer_choice == 'paper':
            return "Scissors cut paper=: you win"
        elif computer_choice == 'rock':
            return "Rock sharpens scissors: computer wins"
        else:
            return "The computer's selection could not be processed"
    elif user_choice == 'paper':
        if computer_choice == 'scissors':
            return "Scissors cut paper=: computer wins"
        elif computer_choice == 'rock':
            return "Rock sharpens scissors: you win"
        else:
            return "The computer's selection could not be processed"
    else:
        return "Your selection could not be processed"

def get_computer_choice(choice_list):
    import random   
    return random.choice(choice_list)  

def get_user_choice(prediction_data):
    if prediction_data[0][0] > 0.85:
        return 'rock'
    elif prediction_data[0][1] > 0.85:
        return 'paper'
    elif prediction_data[0][2] > 0.85:
        return 'scissors'
    else:
        return 'nothing'

def play_rps():
    import cv2
    from keras.models import load_model
    import numpy as np
    import time

    rps_list = ['rock', 'paper', 'scissors']
    computer_choice = get_computer_choice(rps_list)

    model = load_model('/home/siobhan/aicore/code/projects/rps/converted_keras/keras_model.h5')
    cap = cv2.VideoCapture(0)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    while True:
        ret, frame = cap.read()
        resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
        image_np = np.array(resized_frame)
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
        data[0] = normalized_image
        prediction = model.predict(data)
        cv2.imshow('frame', frame)
        # Press q to close the window

        user_choice = get_user_choice(prediction)

        print("You chose", user_choice)
        print("The computer chose", computer_choice)
        print(who_won(user_choice, computer_choice))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

play_rps()
