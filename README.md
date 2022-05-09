# Computer-Vision-Rock-Paper-Scissors
In this lab, you will create an interactive Rock-Paper-Scissors game, in which the user can play with the computer using the camera.
# Milestone 1
Used https://teachablemachine.withgoogle.com/train to create an image model for Rock Paper Scissos with 4 classes (Rock, Paper, Scissors), each with about 400-500 pictures and downloaded

# Milestone 2
Created the environment: 
   conda create --name rps python=3.8
   conda activate rps
Installed the required packages: opencv-python, tensorflow, and ipykernel:
   conda install pip
   pip install opencv-python
   pip install ~/Downloads/tensorflow-2.7.0-cp38-cp38-linux_x86_64.whl
   pip install ipykernel
Attempted to run the model but got an error: The TensorFlow library was compiled to use AVX instructions, but these aren't available on your machine.
I downloaded a pre-complied version from https://github.com/lakshayg/tensorflow-build to overcome this issue and installed this in the enviroment and was able to run the model successfully

# Milestone 3

The simulation program in rps_simulation.ipynb simulates the Rock Paper Scissors game, accepting a one character input r (rock), p (paper) or s (scissors) from the user
The computer choice is generated as a random selection from a list containing the 3 options
The computer and user choice are compared and a message is output informing the user of the winner
The output also includes the 'reason' behind the result e.g. Rock sharpens Scissors

# Milestone 4
Created the game in a Jupyter notebook rps_computer_vision.ipynb
This combines the logic in the simulation, with capturing the image input from the user instead of text
I initially used input / print statements to capture user input or output results so I could see the inner workings
I then changed this to use the put_text method to display output and wait_key to capture input
I had an issue with wait_key in that it seemed very slow to respond to any key stroked after the first user input
To overcome this I used a variable pressed_key to store the key pressed and used this in the evaluation, rather than use wait_key each time.  This is because when waitkey is run each time iand each time reads the keyboard buffer, so the second branch executed only if the software receives the key in a later branch straight after it receives any of the keys in previous branches.
I initally implemented a single round game, initiated by the user pressing 'p', and allowing them to exit by pressing 'q'
Once I had this working I enhanced the game with the following features:
* Count down to the image capture, displaying text Rock Paper Scissors Go in 1 second intervals to simulate the real life game, followed by a 3 second count down informing the user the image is being captured
* Multi play options:
    * Single game - user enters s and plays 1 round
    * First to 3 - user enters f, and the game plays until one player reaches a score of 3
    * Best of 3 - user enters b, the game play rounds until one winner has a score of 2 and 3 valid games have been played (excludes draws or when the model cannot predict the user input)
After each game the results and scores are displayed on the frame.  An issue I encountered here was the new line string sequence is not recognised when using puttext.  I overcame this by searching the message text for '\n' and then creating a loop where the y co-ordinate was incremented for each line of the message and each line printed in each execution of the loop

Once I had this implementation I then created the game as a class, with additional classes for the model and the user scores (really just to practice writing and using classes!).
The classes are defined in rps_game and the utilised in rpl_play.py


