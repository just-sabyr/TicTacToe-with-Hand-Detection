"""
    TicTacToe game on the terminal.
    Initial board setup:
    [1, 2, 3]
    [4, 5, 6]
    [7, 8, 9]
"""

def rowise_or_columnwise_same(board):
    """
    Board must be shaped into 3x3 array before passing to this function.
    """
    winner = rowise_same(board)
    
    # transpose the board (exchange rows with columns) to check columnwise
    transpose = [[board[j][i] for j in range(len(board))] for i in range(len(board[0]))]

    if winner == 0:
        winner = rowise_same(transpose)
    return winner

def rowise_same(board):
    winner = 0
    # check if the values in any row of board is the same

    for row in board:
        if (row.count(row[0]) == len(row)):
            winner = row[0]

    return winner

def diagonalwise_same(board):
    winner = 0
    if board[0][0] == board[1][1] == board[2][2]:
        winner = board[0][0]
    elif board[0][2] == board[1][1] == board[2][0]:
        winner = board[0][2]
    return winner 

def game_winner(board):
    """
    param: board - 3x3 list representing the current board
    return: 0 if no one has one yet, 'x' or 'o' if one has won
    """

    winner = rowise_or_columnwise_same(board)
    if winner == 0:
        winner = diagonalwise_same(board)
    
    return winner

def convert_3x3(board):
    """
    param: board - list 0x9 
    return: board - list 3x3 
    """
    newBoard = [[0 for column in range(3)] for row in range(3)]

    for i in range(2, -1, -1):
        for j in range(2, -1, -1):
            newBoard[i][j] = board.pop()
    return newBoard

def one_dim_to_3x3(index):
    """
    param: index - a value in [1,...9]
    return: row, col
    """
    indexes = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
        ]
    
    for row in range(3):
        for col in range(3):
            if indexes[row][col] == index:
                return row, col
    
def make_move(board, step):
    player = 'o' if step % 2 == 1 else 'x'

    index_choice = int(input(f"{player}'s turn: "))

    row, col = one_dim_to_3x3(index_choice)

    if board[row][col] != 'x' and board[row][col] != 'o':
        board[row][col] = player
        return board
    
    return make_move(board, step)

def print_board(board):
    for row in (board):
        for item in row:
            print(item, end=' | ')
        print('\n')
    print('\n')


def game():
    # Initialize the board
    board = [i for i in range(1, 10)]

    # Convert the board into 3x3
    board = convert_3x3(board)

    # Set the winner to 0 (meaning no one has won yet.)
    winner = 0

    print("Welcome to TicTacToe, input 1 to 10 to place an x or o in the appropriate square.")
    print("****************\n")

    for step in range(9):
        board = make_move(board, step)
        print_board(board)
        winner = game_winner(board)
        if winner != 0:

            print(f"{winner} has won.")
            break

    if winner == 0:
        print('Game has ended a tie.')

if __name__ == '__main__':
    game()