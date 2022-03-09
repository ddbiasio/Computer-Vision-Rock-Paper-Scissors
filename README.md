# Computer-Vision-Rock-Paper-Scissors
In this lab, you will create an interactive Rock-Paper-Scissors game, in which the user can play with the computer using the camera.
# Environment
Virtual environment with Python 3.9 and Tensorflow and OpenCV
Some initial difficulties running the model with this error: The TensorFlow library was compiled to use AVX instructions, but these aren't available on your machine.
I downloaded a pre-complied version from https://github.com/lakshayg/tensorflow-build to ocercome this issue and added this to my virtual environment
# Simulation Program
The simulation program in rps_simulation.ipynb simulates the Rock Paper Scissors game, accepting a one character input r (rock), p (paper) or s (scissors) from the user
The computer choice is generated as a random selection from a list containing the 3 options
The computer and user choice are compared and a message is output informing the user of the winner
