"""Simple two-player Tic-tac-toe command-line game."""

BOARD_SIZE = 3
EMPTY_CELL = " "


def create_board():
    """Create an empty game board."""
    return [[EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def display_board(board):
    """Display the current board."""
    print()
    for index, row in enumerate(board):
        print(f" {row[0]} | {row[1]} | {row[2]} ")
        if index < BOARD_SIZE - 1:
            print("---+---+---")
    print()


def is_valid_move(board, row, col):
    """Check whether a move is valid."""
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == EMPTY_CELL


def check_winner(board, player):
    """Check whether a player has won."""
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(BOARD_SIZE):
        if all(board[row][col] == player for row in range(BOARD_SIZE)):
            return True

    if all(board[index][index] == player for index in range(BOARD_SIZE)):
        return True

    if all(board[index][BOARD_SIZE - 1 - index] == player for index in range(BOARD_SIZE)):
        return True

    return False


def is_board_full(board):
    """Check whether the board is full."""
    return all(cell != EMPTY_CELL for row in board for cell in row)


def get_move(board, player):
    """Get a valid move from the player."""
    while True:
        move = input(f"Player {player}, enter row and column, for example 1 2: ")

        try:
            row_text, col_text = move.split()
            row = int(row_text) - 1
            col = int(col_text) - 1
        except ValueError:
            print("Invalid input. Please enter two numbers, for example 1 2.")
            continue

        if is_valid_move(board, row, col):
            return row, col

        print("Invalid move. Please choose an empty cell between 1 and 3.")


def play_game():
    """Run the game."""
    board = create_board()
    current_player = "X"

    print("Welcome to Tic-tac-toe!")
    print("Player X starts first.")
    print("Enter row and column numbers from 1 to 3.")

    while True:
        display_board(board)
        row, col = get_move(board, current_player)
        board[row][col] = current_player

        if check_winner(board, current_player):
            display_board(board)
            print(f"Player {current_player} wins!")
            break

        if is_board_full(board):
            display_board(board)
            print("The game is a draw!")
            break

        current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
    play_game()