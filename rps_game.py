import cv2
from keras.models import load_model
import numpy as np
import time

class rps_model:
    """
    The rps_model class returns a prediction from the trained model

    ...

    Attributes
    ----------
    model : model
        A keras model trained with images in 4 classes: Rock, Paper, Scissors, Nothing

    data : np.ndarray
        An image of the user presenting their choice for the game, captured from camera

    Methods
    -------
    get_prediction(image)
        Makes a prediction from the model based on the user image
    """
    def __init__(self, model) -> None:

        """
        Parameters
        ----------
        model : model
            A keras model trained with images in 4 classes: Rock, Paper, Scissors, Nothing      
        """

        self.model = load_model(model)
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    def get_prediction(self) -> str:

        """
        Makes a predicition of the user's choice
        Returns 'nothing' if it cannot be determined

        Parameters
        ----------
        image : np.ndarray
            An image captured from the video input
        """
        prediction = self.model.predict(self.data)

        if prediction[0][0] > 0.85:
            return 'rock'
        elif prediction[0][1] > 0.85:
            return 'paper'
        elif prediction[0][2] > 0.85:
            return 'scissors'
        else:
            return 'nothing'

class scores:
    """
    A class to hold the user and computer scores during gameplay

    Attributes
    ----------
    user_score : int
        The user's score
    computer_score:
        The computer's score

    Methods
    -------
    update_score(winner)
        Increments the indicated players score by 1
    reset_score
        Resets both player scores to 0
    """

    def __init__(self):

        """
        Initialises both player scores to 0
        """

        self.user_score = 0
        self.computer_score = 0

    def update_score(self, winner: str) -> None:
        """
        Increments the indicated players (winner) score by 1

        Parameters
        ----------
        winner : str
            The winner of the round (user or computer)
        """

        if winner =="user":
            self.user_score += 1
        elif winner == "computer":
            self.computer_score += 1
    
    def reset_score(self) -> None:

        """
        Resets both player scores to 0
        """

        self.user_score = 0
        self.computer_score = 0

class rps:
    """
    A class to implement the Rock Paper Scissord game

    Attributes
    ----------
    scores : rps_game.scores
        Maintains the scores for the user and computer

    outcome : str
        A text based description of the gae result e.g. Scissors cut Paper

    

    Methods
    -------
    """

    def __init__(self):
        self.scores = scores()
        self.game_mode = ""
        self.game_started = False
        self.game_over = False
        self.match_over = False
        self.game_result = ""
        self.match_result = ""
        self.game_help_text = ("Select game mode or 'q' to quit."
            + "\nSingle round (s)"
            + "\nFirst to 3 wins (f)"
            + "\nBest of 3 wins (b)")

    def start_game(self, game_mode):
        self.game_mode = game_mode
        self.game_started = True

    def __compare_choices(self, user_choice, computer_choice):

        if user_choice == computer_choice:
            winner = "draw"
            result_msg = "The result is a draw"
        elif user_choice == 'rock':
            if computer_choice == 'scissors':
                winner = "user"
                result_msg = "Rock sharpens scissors: you win"
            elif computer_choice == 'paper':     
                winner = "computer"
                result_msg = "Paper wraps rock: computer wins"
            else: 
                winner = "none"
                result_msg = "The computer's selection could not be processed"
        elif user_choice == 'scissors':
            if computer_choice == 'paper':   
                winner = "user"
                result_msg = "Scissors cut paper: you win"
            elif computer_choice == 'rock':  
                winner = "computer"
                result_msg = "Rock sharpens scissors: computer wins"
            else:
                winner = "none"
                result_msg = "The computer's selection could not be processed"
        elif user_choice == 'paper':
            if computer_choice == 'scissors':    
                winner = "computer"
                result_msg = "Scissors cut paper: computer wins"
            elif computer_choice == 'rock':   
                winner = "user"
                result_msg = "Rock sharpens scissors: user wins" 
            else: 
                winner = "none"               
                result_msg = "The computer's selection could not be processed"
        else:
            winner = "none"
            result_msg = "Your selection could not be processed"
        return winner, result_msg

    def build_results_text(self, user_choice, computer_choice, match_winner, result_msg):
        results_text = (f"You: {user_choice}"
                f"\nComputer: {computer_choice}"
                f"\nResult:  {result_msg}"
                f"\nUser score: {self.scores.user_score}"
                f"\nComputer score: {self.scores.computer_score}")
        
        if self.match_over:
            results_text = (f"{results_text}"
                            f"\nThe overall winner is: {match_winner}")

        results_text = (f"{results_text}"
                            f"\nPress 'p' to play again or 'q' to quit")
        return results_text

    def get_computer_choice(self):
        import random   
        rps_list = ['rock', 'paper', 'scissors']
        return random.choice(rps_list)  
          
    def get_match_result(self):

        if self.game_mode ==  "f":
            # Check if a user has reached 3 and declare them the winner
            if self.scores.computer_score == 3:
                self.match_over = True
                return "computer"
            elif self.scores.user_score == 3:
                self.match_over = True
                return "user"

        elif self.game_mode == "b":
            # Check  if 3 games have been played and who has most wins
            if self.scores.user_score + self.scores.computer_score == 3:
                if self.scores.user_score > self.scores.computer_score:
                    self.match_over = True
                    return "user"
                else:
                    self.match_over = True
                    return "computer"
            
        else:
            # single match match winner = game winner
            self.match_over = True
    
    def play(self, user_choice, computer_choice):
        
        game_winner, result_msg = self.__compare_choices(user_choice, computer_choice)

        self.scores.update_score(game_winner)

        match_winner = self.get_match_result()
        if match_winner == None:
            match_winner = game_winner

        self.game_over = True
 
        # results_text = self.__build_results_text(user_choice, computer_choice, match_winner, result_msg)
        results_text = self.build_results_text(user_choice, computer_choice, match_winner, result_msg)
        
        return results_text

    def reset_game(self):

        #restarts match or game
        self.game_over = False
        if self.game_mode in ('b', 'f') and not self.match_over:
            self.game_started = True
        else:
            self.game_started = False
            self.scores.reset_score()
            self.game_mode = ""
            self.match_over = False
