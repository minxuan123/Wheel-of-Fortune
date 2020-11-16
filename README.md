My game is a text-based game which is heavily based on the game show Wheel of Fortune. It is a 3 player game where the ultimate goal is to earn the most amount of money at the end of 3 rounds. 

Players earn money by guessing the correct consonant, and how much they earn per letter depends on the amount they spin on the wheel at the start of their turn. Only the player that solves the puzzle would get to keep the money that he/she earns that round. 

How to play my game:
1. At the start of a turn, a player can choose to spin the wheel, buy a vowel or solve the puzzle
2. If the player spin BANKRUPT or LOSE A TURN, his/her turn will end
3. If the player guess a wrong consonant or buy a wrong letter, his/her turn will also end
4. Money is earned for every correcct letter in the question, according to the value on the wheel
5. Repeat steps 1-4
6. The round ends when one player manages to solve the puzzle
7. The game ends at the end of 3 rounds

My code:
My code consists of 1 function and 3 classes. 

1. function GenerateWL:
    It reads a .txt file containing the list of questions for the game and processes the file into a list, containing lists of questions, each list corresponding to a different category of question.
    
2. class Wheel:
    It has 2 methods, display() and spin(). Method display() prints the wheel while method spin() recreates the action of spinning the wheel, stopping at a random position in the wheel. It returns the display at which the pointer stoopped at and the corresponding value.
    
3. class Player:
    It is a state machine and takes in the player's name when it is initialised. The state machine takes in input and updates each player's winnings accordingly. When the input prompts it, it also updates the scoreboard when a player wins or loses. 
    
4. class Game:
    It is a state machine. It calls the GenerateWL function and store it in a attribute, which acts as a word bank for the game. The class has 5 methods apart from step and get_next_values. 
    
    - Method intro(): It prompts input from the user regarding the number of players and their names and initializes them using the Player class. It then loads an introductory scene explaining the rules of the game. This method is called when the class is initialized. 
    - Method generateqn(): It chooses a random theme and question from the word bank and displays them to the players at the start of each round. 
    - Method duringround(): When it is a player's turn, it prompts the player's input and calls the step function with the player's input. When it is the computer's turn, it will automatically help the computer spin the wheel during its turn or solve the puzzle when all consonants are already revealed. 
    - Method getwinner(): When the game has ended, the method compares the scores of the players and declare the one with the highest score the winner. It also prints the celebratory message. 
    - Method run(): It initiates the state machine and calls the other classes during appropriate times. It keeps track of the number of rounds played and stops the game when 3 rounds have been completed. It also process and inform other methods whether the current round is played by a player or a computer, prompting different outputs. 
    
    Within the get_next_values() method, the state machine takes in input such as prompts for the round to start, to spin the wheel, to buy a vowel or to solve the question, and returns appropriate outputs, according to whether the round is played by a player or a computer. It returns error messages when the input is not expected and facilitates player changes when a player's turn has ended. 

