import functions as f
playing = True
EMPTY = "   "

"""this module contains all the user_interface handling"""


def run() -> None:
    """runs the entirety of the game"""
    rows = int(input())  # ask for row
    columns = int(input())  # ask for col
    game = f.GameBoard(rows, columns)  # creating a GameBoard object
    game.initialize_board()  # creating an empty board based on specified fields
    beginning_state = input()  # asking user for how they want the board to be

    if beginning_state == "CONTENTS":
        contents = _set_board_up(rows)
        game.place_contents(contents)  # setting up the requested game_board
        game.tick(0)  # detect match in the beginning
    print_board(game.get_board())  # print the initial board

    # entering the game loop:
    col = 0
    while playing:
        next_step = input()

        if next_step == "":
            state = game.tick(col)
            if state == 13:
                print_board(game.get_board())
                print("GAME OVER")
                break
            else:
                pass

        elif next_step[0] == "F":
            # [F 1 X Y Z] --> [1 X Y Z]
            next_step = next_step.split()[1:]
            state = game.place_faller(next_step)
            if state == 13:
                print("GAME OVER")
                break
            elif state == 101:
                col = col
            else:
                col = state


        elif next_step == "R":
            game.rotate()  

        elif next_step == "<":
            col = game.move_faller_left()

        elif next_step == ">":
            col = game.move_faller_right()

        elif next_step == "Q":
            break

        else:
            pass

        print_board(game.get_board())


def _set_board_up(rows: int) -> list[list]:
    """asks for input according to the num of rows in the board, returns 2D list content in stack form
        last one is on the bottom"""
    row_pieces = []
    for i in range(rows):
        row_pieces.append(input())
    row_pieces = [list(i) for i in row_pieces]
    return row_pieces


def print_board(board: "[[]]") -> None:
    """prints the board"""
    for i in range(2, len(board[0])):
        sequence = "|"
        for j in range(len(board)):
            sequence += (board[j][i])
        print(sequence + "|")

    print(" " + ("---" * len(board)) + " ")  # printing the floor of the game


if __name__ == "__main__":
    run()
