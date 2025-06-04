#utils.py
# Define the adjacency list for the board positions
adjacency_list = {
    0: [1, 9],
    1: [0, 2, 4],
    2: [1, 14],
    3: [4, 10],
    4: [1, 3, 5, 7],
    5: [4, 13],
    6: [7, 11],
    7: [4, 6, 8],
    8: [7, 12],
    9: [0, 10, 21],
    10: [3, 9, 11, 18],
    11: [6, 10, 15],
    12: [8, 13, 17],
    13: [5, 12, 14, 20],
    14: [2, 13, 23],
    15: [11, 16],
    16: [15, 17, 19],
    17: [12, 16],
    18: [10, 19],
    19: [16, 18, 20, 22],
    20: [13, 19],
    21: [9, 22],
    22: [19, 21, 23],
    23: [14, 22]
}

# Define all possible mills (three in a row)
mills = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [15, 16, 17],
    [18, 19, 20],
    [21, 22, 23],
    [0, 9, 21],
    [3, 10, 18],
    [6, 11, 15],
    [1, 4, 7],
    [16, 19, 22],
    [8, 12, 17],
    [5, 13, 20],
    [2, 14, 23],
    [9, 10, 11],
    [12, 13, 14],
    [19, 16, 15],
    [19, 22, 23],
    [21, 9, 0],
    [18, 10, 3],
    [15, 11, 6],
    [7, 4, 1],
    [22, 19, 16],
    [17, 12, 8],
    [20, 13, 5],
    [23, 14, 2]
]

def is_adjacent(pos1, pos2):
    """Check if two positions are adjacent."""
    return pos2 in adjacency_list[pos1]

def check_mill(board, position):
    """Check if placing a piece at 'position' forms a mill."""
    player = board[position]
    for mill in mills:
        if position in mill and all(board[pos] == player for pos in mill):
            return True
    return False

def count_pieces(board, player):
    """Count the number of pieces a player has on the board."""
    return board.count(player)

def evaluate_board(board, player):
    """Heuristic evaluation of the board for the AI."""
    opponent = 'W' if player == 'B' else 'B'
    player_pieces = count_pieces(board, player)
    opponent_pieces = count_pieces(board, opponent)
    player_mills = sum(1 for mill in mills if all(board[pos] == player for pos in mill))
    opponent_mills = sum(1 for mill in mills if all(board[pos] == opponent for pos in mill))
    return (player_pieces - opponent_pieces) + (player_mills - opponent_mills) * 2

def print_board(board):
    """Print the board to the console."""
    positions = [str(i) if spot == ' ' else spot for i, spot in enumerate(board)]
    board_str = f"""
{positions[0]}----------{positions[1]}----------{positions[2]}
|          |          |
|  {positions[3]}-------{positions[4]}-------{positions[5]}  |
|  |       |       |  |
|  |  {positions[6]}----{positions[7]}----{positions[8]}  |  |
|  |  |         |  |  |
{positions[9]}--{positions[10]}--{positions[11]}       {positions[12]}--{positions[13]}--{positions[14]}
|  |  |         |  |  |
|  |  {positions[15]}----{positions[16]}----{positions[17]}  |  |
|  |       |       |  |
|  {positions[18]}-------{positions[19]}-------{positions[20]}  |
|          |          |
{positions[21]}----------{positions[22]}----------{positions[23]}
"""
    print(board_str)
