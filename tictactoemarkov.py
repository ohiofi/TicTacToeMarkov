import random




class TicTacToeMarkovChain:
    # Initializes a new instance of the Markov Chain with an empty transition table.
    # Parameters: size (int) - Size of the Tic Tac Toe board.
    # Returns: None.
    def __init__(self, size=3, randomnessPercent=1):
        self.size = size
        self.random_percent = randomness 
        self.transitions = {
            "x--------":{"x--o-----":1},
            "xx-o-----":{"xx-oo----":1},
            "x--ox----":{"x--ox---o":1}
        }
        self.history = []

    # Converts the current state of the game to a string key for indexing the transition table.
    # Parameters: twoDArray (list of lists) - Current state of the Tic Tac Toe board.
    # Returns: String representation of the current state.
    def _gamestate_to_key(self, twoDArray):
        result = ''
        for row in twoDArray:
            for move in row:
                if move == 'X': result += 'x'
                elif move == 'O': result += 'o'
                else: result += '-'
        return result

    # Converts a string key back to a two-dimensional array representing the game state.
    # Parameters: key (str) - String representation of the current state.
    # Returns: Two-dimensional array representing the game state.
    def _key_to_gamestate(self, key):
        legend = {"x":"X","o":"O","-":" "}
        moves = [[legend[key[i + j]] for j in range(self.size)] for i in range(0, len(key), self.size)]
        return moves

    # Generates the next move using the Markov Chain.
    # Parameters: twoDArray (list of lists) - Current state of the Tic Tac Toe board.
    # Returns: Updated state of the Tic Tac Toe board after making a move.
    def get_next_move(self, twoDArray):
        key = self._gamestate_to_key(twoDArray)
        self.history.append(key)
        if key in self.transitions and self.random_percent < random.random()*100:
            twoDArray = self._weighted_move(key, twoDArray)
        else:
            self.transitions[key] = {}
            twoDArray = self._random_move(key, twoDArray)
        newKey = self._gamestate_to_key(twoDArray)
        self.history.append(newKey)
        if newKey not in self.transitions[key]:
            self.transitions[key][newKey] = 1
        return twoDArray

    # Updates the transition table based on the outcome of the game.
    # Parameters: twoDArray (list of lists) - Current state of the Tic Tac Toe board, outcome (str) - Outcome of the game ("win", "lose", "draw").
    # Returns: None.
    def update_transitions(self, twoDArray, outcome):
        if outcome != None:
            print(self.history)
            for i in range(0, len(self.history)-1, 2):
                if outcome == "lose" or outcome == "draw":
                    self.transitions[self.history[i]][self.history[i+1]] *= 2
                else:
                    self.transitions[self.history[i]][self.history[i+1]] *= (0.9 - 0.1*i)
            self.history = []
            print(self.transitions)
        
    # Generates a random move on the board.
    # Parameters: twoDArray (list of lists) - Current state of the Tic Tac Toe board.
    # Returns: Updated state of the Tic Tac Toe board after making a random move.
    def _random_move(self, key, twoDArray):
        # Find empty cells by checking for spaces
        empty_cells = [(i, j) for i in range(len(twoDArray)) for j in range(len(twoDArray[0])) if twoDArray[i][j] == ' ']
        if empty_cells:
            move = random.choice(empty_cells)
            twoDArray[move[0]][move[1]] = 'O'
        return twoDArray
        
    # Selects the move with the highest weight from the transition table.
    # Parameters: key (str) - String representation of the current state, twoDArray (list of lists) - Current state of the Tic Tac Toe board.
    # Returns: Updated state of the Tic Tac Toe board after making a move.
    def _weighted_move(self, key, twoDArray):
        highKey, highValue  = list(self.transitions[key].items())[0]
        for k,v in self.transitions[key].items():
            if v > highValue:
                highKey = k
                highValue = v
        print("high value ",highValue)
        if highValue >= random.random() * self.random_percent:
            return self._key_to_gamestate(highKey)
        else:
            return self._random_move(key, twoDArray)
        
        





class TicTacToeGame:
    # TicTacToeGame.__init__(): Initializes a new instance of the Tic Tac Toe game.
    # Parameters: size (int) - Size of the Tic Tac Toe board.
    # Returns: None.
    def __init__(self, markov_chain, size=3):
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.markov_chain = markov_chain
        self.size = size

    # TicTacToeGame.print_board(): Prints the current state of the Tic Tac Toe board.
    # Parameters: None.
    # Returns: None.
    def print_board(self):
        for i in range(len(self.board)):
            print('|'.join(self.board[i]))
            if i < 2 :
                print('-' * (self.size * 2 - 1))

    # TicTacToeGame.check_winner(): Checks if there is a winner or if the game is a draw.
    # Parameters: None.
    # Returns: String indicating the outcome: "win" if the player wins, "lose" if the player loses, "draw" if the game is a draw, or None if the game is ongoing.
    def check_winner(self):
        # Check rows, columns, and diagonals for a winner
        for i in range(self.size):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return "win" if self.board[i][0] == 'X' else "lose"
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return "win" if self.board[0][i] == 'X' else "lose"
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return "win" if self.board[0][0] == 'X' else "lose"
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return "win" if self.board[0][2] == 'X' else "lose"
        # Check for draw
        if all(cell != ' ' for row in self.board for cell in row):
            return "draw"
        # No winner or draw yet
        return None

    def check_draw(self):
        return all(self.board[i][j] != ' ' for i in range(self.size) for j in range(self.size))

    # TicTacToeGame.player_move(): Prompts the player to make a move and updates the board accordingly.
    # Parameters: None.
    # Returns: None.
    def player_move(self):
        while True:
            try:
                row = int(input("Enter row (1-{}): ".format(self.size))) - 1
                col = int(input("Enter column (1-{}): ".format(self.size))) - 1
                if self.board[row][col] == ' ':
                    self.board[row][col] = 'X'
                    return (row, col)
                else:
                    print("That cell is already taken. Try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a number between 1 and {}.".format(self.size))

    # TicTacToeGame.markov_chain_move(): Generates the next move using the Markov Chain.
    # Parameters: None.
    # Returns: None.
    def markov_chain_move(self):
        current_state = self.board
        next_state = self.markov_chain.get_next_move(current_state)
        if next_state:
            for i in range(self.size):
                for j in range(self.size):
                    if next_state[i][j] != current_state[i][j]:
                        self.board[i][j] = 'O'  # Update the board with the Markov Chain's move
                        return (i, j)

    # Executes the game loop until a winner is determined.
    # Parameters: None.
    # Returns: None.
    def play(self):
        print("Welcome to Tic Tac Toe against Markov Chain!")
        self.print_board()
        game_over = False
        while not game_over:
            # Player move
            player_move = self.player_move()
            self.print_board()
            outcome = self.check_winner()
            print(self.board)
            if outcome:
                if outcome == 'win':
                    print("Congratulations! You won!")
                elif outcome == 'lose':
                    print("You lost. Better luck next time!")
                elif outcome == 'draw':
                    print("It's a draw!")
                game_over = True
            # Update Markov Chain transitions based on the outcome
            self.markov_chain.update_transitions(self.board, outcome)
            if not game_over:
                # Markov Chain move
                markov_move = self.markov_chain_move()
                print("Markov Chain's move:")
                print(markov_move)
                self.print_board()
                outcome = self.check_winner()
                if outcome:
                    if outcome == 'win':
                        print("Congratulations! You won!")
                    elif outcome == 'lose':
                        print("You lost. Better luck next time!")
                    elif outcome == 'draw':
                        print("It's a draw!")
                    game_over = True

                # Update Markov Chain transitions based on the outcome
                self.markov_chain.update_transitions(self.board, outcome)

# Initiates a game with the global Markov Chain
def play_game(markov_chain):
    while True:
        game = TicTacToeGame(markov_chain)
        game.play()
        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again == 'n':
            print("Thank you for playing! Goodbye!")
            break

# Initialize the global Markov Chain
markov_chain = TicTacToeMarkovChain()

# Start the game
play_game(markov_chain)
