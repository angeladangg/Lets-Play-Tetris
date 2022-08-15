"""this module contains the mechanics/ model of the game in a GameBoard class """
EMPTY = "   "
playing = None


class GameBoard:
    def __init__(self, rows: int, columns: int):
        self._board = []
        self._rows = rows + 2
        self._columns = columns


    def get_board(self) -> list[list]:
        """allow access to board"""
        return self._board

    def get_num_rows(self) -> int:
        """return num of VISIBLE rows"""
        return self._rows-2

    def get_num_cols(self) -> int:
        """allow access to num of cols"""
        return self._columns

    def place_contents(self, contents: list[list]) -> None:
        """replaces original board with transformed pre-game board"""
        transformed = []
        for i in range(len(contents[0]) - 1, -1, -1):
            temp = [' ', ' ']
            for j in range(len(contents)):
                temp.append(contents[j][i])
            transformed.append(temp)

        self._board = transformed[::-1]  # flipping the board, left is right and right is left

        # ADDING WHITE SPACE TO EVERYTHING:
        for i in range(self._columns):
            for j in range(self._rows):
                self._board[i][j] = f" {self._board[i][j]} "

        self.shove_down()


    def initialize_board(self) -> None:
        """creates game board with rows and cols. plus 2 to rows because of faller object mechanics"""
        for col in range(self._columns):
            self._board.append([])
            for row in range(self._rows):
                self._board[-1].append(EMPTY)


    def drop(self, col: int) -> bool:
        """This method is called for every passage of time. Drops the faller down by 1 everytime the method is called.
            once faller at the bottom or on top of a jewel, state turns into almost frozen. If almost frozen, freeze."""
        # FINDING THE HEAD OF THE FALLER IN THE BOARD:
        for i in range(len(self._board[col])):
            if self._board[col][i][0] == "[":
                row_head = i  # this is the head of my faller
                try:
                    if self._board[col][row_head + 3] == EMPTY:
                        #  if the space below faller is empty, move down
                        self._board[col][row_head + 3] = self._board[col][row_head + 2]
                        self._board[col][row_head + 2] = self._board[col][row_head + 1]
                        self._board[col][row_head + 1] = self._board[col][row_head]
                        self._board[col][row_head] = EMPTY
                        if row_head + 3 == len(self._board[col]) - 1 or self._board[col][row_head + 4] != EMPTY:
                            # if faller reached the end or faller on top of another jewel, turn into ready to freeze
                            self._board[col][row_head+1] = f"|{self._board[col][row_head+1][1]}|"
                            self._board[col][row_head + 2] = f"|{self._board[col][row_head + 2][1]}|"
                            self._board[col][row_head + 3] = f"|{self._board[col][row_head + 3][1]}|"
                            self._board[col][row_head] = EMPTY
                            return False

                    elif self._board[col][row_head + 4] != EMPTY:
                        self._board[col][row_head] = f"|{self._board[col][row_head][1]}|"
                        self._board[col][row_head + 1] = f"|{self._board[col][row_head + 1][1]}|"
                        self._board[col][row_head + 2] = f"|{self._board[col][row_head + 2][1]}|"

                except IndexError:
                    self._board[col][row_head + 1] = f"|{self._board[col][row_head + 1][1]}|"
                    self._board[col][row_head + 2] = f"|{self._board[col][row_head + 2][1]}|"
                    self._board[col][row_head + 3] = f"|{self._board[col][row_head + 3][1]}|"
                    self._board[col][row_head - 1] = EMPTY

                    return False
                break  # once found the head, stop searching


            elif self._board[col][i].startswith("|"):
                row_head = i
                self._freeze(col, row_head)
                return True
                break

            elif self._board[col][i].startswith(" ") and self._board[col][i] != EMPTY:
                return True
                break


    def rotate(self) -> None:
        """Rotates the faller when it's falling or when it hasn't been frozen"""
        col = None
        row_head = None
        # RIGHT HERE I'M FINDING THE FALLER IN THE BOARD:
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                if self._board[i][j].startswith("[") or self._board[i][j].startswith("|"):
                    row_head = j  # this is the head of my faller
                    col = i
                    break  # once head is found, stop searching
        # SINCE THE BUTT IS 2 SPACES AWAY FROM THE HEAD, I ADDED 2
        row_butt = row_head + 2
        # ROTATING EVERYTHING IN FALLER DOWN BY 1 INDEX
        temp = self._board[col][row_butt]
        self._board[col][row_butt] = self._board[col][row_head+1]
        self._board[col][row_head+1] = self._board[col][row_head]
        self._board[col][row_head] = temp


    def place_faller(self, faller: list) -> int:  # faller is a class object
        """This places the faller on the board with the bottom peeking out.
            If another faller exist, creating faller won't take effect. If column is full, return 13 to end game."""
        col = int(faller[0]) - 1
        # searching for another faller:
        another_fall_exists = False
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                if self._board[i][j].startswith("[") or self._board[i][j].startswith("|"):
                    another_fall_exists = True
        if another_fall_exists:
            return 101
        # if there's 3 empty space for the faller
        elif len(set(self._board[col][0:3])) == 1:
            self._board[col][0] = f"[{faller[1]}]"
            self._board[col][1] = f"[{faller[2]}]"
            self._board[col][2] = f"[{faller[3]}]"
            return col

        else:
            return 13  # 13 means death of the game

    def move_faller_left(self) -> int:
        """Finds the location of the faller and identifies its top piece.
            Moves the faller to the left within the column range. Returns the col num of new col"""
        col = None
        row_head = None
        # RIGHT HERE I'M FINDING THE FALLER IN THE BOARD:
        found = False
        for i in range(len(self._board)):
            if found:
                break
            for j in range(len(self._board[0])):
                if self._board[i][j].startswith("[") or self._board[i][j].startswith("|"):
                    row_head = j  # this is the head of my faller
                    col = i
                    found = True
                    break
        if col == 0:  # if we're at the left most of the column, return the column number immediately
            return col
        else:
            if self._board[col - 1][row_head:row_head + 3].count(EMPTY) == 3:  # if 3 rows in column to the left is empty
                if (row_head + 2) != len(self._board[col]) - 1:  # if row butt isn't at the bottom of the col
                    if self._board[col - 1][row_head + 3] == EMPTY:
                        self._board[col - 1][row_head] = f'[{self._board[col][row_head][1]}]'
                        self._board[col - 1][row_head + 1] = f'[{self._board[col][row_head + 1][1]}]'
                        self._board[col - 1][row_head + 2] = f'[{self._board[col][row_head + 2][1]}]'
                        # emptying out original spots
                        self._board[col][row_head] = EMPTY
                        self._board[col][row_head + 1] = EMPTY
                        self._board[col][row_head + 2] = EMPTY
                        return col - 1

                    else:  # if the left has space but bottom has other jewels, turn back to landed
                        self._board[col - 1][row_head] = f"|{self._board[col][row_head][1]}|"
                        self._board[col - 1][row_head + 1] = f"|{self._board[col][row_head + 1][1]}|"
                        self._board[col - 1][row_head + 2] = f"|{self._board[col][row_head + 2][1]}|"
                        # emptying out original spots
                        self._board[col][row_head] = EMPTY
                        self._board[col][row_head + 1] = EMPTY
                        self._board[col][row_head + 2] = EMPTY
                        return col - 1
                else:
                    self._board[col - 1][row_head] = f"|{self._board[col][row_head][1]}|"
                    self._board[col - 1][row_head+1] = f"|{self._board[col][row_head+1][1]}|"
                    self._board[col - 1][row_head+2] = f"|{self._board[col][row_head+2][1]}|"
                    # emptying out the original faller spots after the migration
                    self._board[col][row_head] = EMPTY
                    self._board[col][row_head+1] = EMPTY
                    self._board[col][row_head+2] = EMPTY
                    return col-1

            else:
                return col
            
    def move_faller_right(self) -> int:
        """Moves the faller to the right within the column range. Returns the column num of new column"""
        col = None
        row_head = None
        found = False
        # I'M FINDING THE FALLER IN THE BOARD:
        for i in range(len(self._board)):
            if found:
                break
            for j in range(len(self._board[0])):
                if self._board[i][j].startswith("[") or self._board[i][j].startswith("|"):
                    row_head = j  # this is the head of my faller
                    col = i
                    found = True
                    break
        if col == len(self._board)-1:
            return col
        # if self._board[col] != self._board[-1]:  # if the column we're looking at isn't the right most one
        else:
            if self._board[col + 1][row_head:row_head + 3].count(EMPTY) == 3:  # if column to the right is empty
                if (row_head+2) != len(self._board[col])-1:  # if row butt isn't all the way at the bottom
                    if self._board[col+1][row_head+3] == EMPTY:
                        self._board[col + 1][row_head] = f'[{self._board[col][row_head][1]}]'
                        self._board[col + 1][row_head + 1] = f'[{self._board[col][row_head + 1][1]}]'
                        self._board[col + 1][row_head + 2] = f'[{self._board[col][row_head + 2][1]}]'
                        self._board[col][row_head] = EMPTY
                        self._board[col][row_head + 1] = EMPTY
                        self._board[col][row_head + 2] = EMPTY
                        return col + 1
                    else:
                        self._board[col + 1][row_head] = f'|{self._board[col][row_head][1]}|'
                        self._board[col + 1][row_head + 1] = f'|{self._board[col][row_head + 1][1]}|'
                        self._board[col + 1][row_head + 2] = f'|{self._board[col][row_head + 2][1]}|'
                        # emptying out the original faller spots
                        self._board[col][row_head] = EMPTY
                        self._board[col][row_head + 1] = EMPTY
                        self._board[col][row_head + 2] = EMPTY
                        return col + 1

                else:
                    self._board[col + 1][row_head] = f'|{self._board[col][row_head][1]}|'
                    self._board[col + 1][row_head + 1] = f'|{self._board[col][row_head+1][1]}|'
                    self._board[col + 1][row_head + 2] = f'|{self._board[col][row_head+2][1]}|'
                    # emptying out the original faller spots
                    self._board[col][row_head] = EMPTY
                    self._board[col][row_head + 1] = EMPTY
                    self._board[col][row_head + 2] = EMPTY
                    return col+1
            else:
                return col


    def match_vertical(self) -> None:
        """finding 3 or more match of jewels vertically and turning them into frozen state"""
        for col in range(len(self._board)):
            for row in range(len(self._board[col])-2):  # bound-checking
                if self._board[col][row] != EMPTY:
                    if self._board[col][row][1] == self._board[col][row+1][1] and self._board[col][row][1] == self._board[col][row+2][1]:
                        self._board[col][row] = f'*{self._board[col][row][1]}*'
                        self._board[col][row+1] = f'*{self._board[col][row+1][1]}*'
                        self._board[col][row+2] = f'*{self._board[col][row+2][1]}*'



    def match_horizontal(self) -> None:
        """finding 3 or more match of jewels horizontally and turning them into frozen state"""
        for col in range(len(self._board)-2):  # bound_checking. this won't go out of bound
            for row in range(len(self._board[col])):
                if self._board[col][row] != EMPTY:  # we don't want to match the "empty jewels"
                    if self._board[col][row][1] == self._board[col+1][row][1] and self._board[col][row][1] == self._board[col+2][row][1]:
                        self._board[col][row] = f'*{self._board[col][row][1]}*'
                        self._board[col+1][row] = f'*{self._board[col+1][row][1]}*'
                        self._board[col+2][row] = f'*{self._board[col+2][row][1]}*'

    def match_diagonal_left(self) -> None:
        """identifying 3 or more matches diagonally from top left to bottom right"""
        """
        [[* *, E , E],
        [ E , * *, E],
        [ E , E , * *]]
    
        """
        for col in range(len(self._board)-2):
            for row in range(len(self._board[col])-2):
                if self._board[col][row] != EMPTY:
                    if self._board[col][row][1] == self._board[col + 1][row+1][1] and self._board[col][row][1] == self._board[col + 2][row+2][1]:
                        self._board[col][row] = f"*{self._board[col][row][1]}*"
                        self._board[col+1][row+1] = f"*{self._board[col][row][1]}*"
                        self._board[col+2][row+2] = f"*{self._board[col][row][1]}*"


    def match_diagonal_right(self) -> None:
        """identifying 3 or more matches diagonally from bottom left to top right"""
        """
        [[ "" , "" , **],
         [ "", **, "" ],
         [ **, "" , "" ]]
        """
        for col in range(len(self._board) - 2):  # leave 2 spaces for col to check +1 and +2
            for row in range(len(self._board[col]) - 1, 1, -1):  # starting at the bottom, so iterating backwards
                if self._board[col][row] != EMPTY:  # don't want empty jewel matches
                    if self._board[col][row][1] == self._board[col+1][row-1][1] and self._board[col][row][1] == self._board[col+2][row-2][1]:
                        self._board[col][row] = f"*{self._board[col][row][1]}*"
                        self._board[col+1][row-1] = f"*{self._board[col + 1][row-1][1]}*"
                        self._board[col+2][row-2] = f"*{self._board[col + 2][row-2][1]}*"


    def _freeze(self, col, head) -> bool:
        """This is inside the drop() method. Takes the parameter of where the faller is and where it's head is.
           Triggered passage of time is requested and turning state from landed to frozen"""
        self._board[col][head] = f" {self._board[col][head][1]} "
        self._board[col][head+1] = f" {self._board[col][head+1][1]} "
        self._board[col][head+2] = f" {self._board[col][head+2][1]} "

    def _match(self) -> None:
        """Checks for all possible matches."""
        self.match_vertical()
        self.match_horizontal()
        self.match_diagonal_right()
        self.match_diagonal_left()


    def theres_a_match(self) -> bool:
        """checks if there are any matches"""
        for col in range(len(self._board)):  # leave 2 spaces for col to check +1 and +2
            for row in range(len(self._board[col])):
                if self._board[col][row][0] == "*":
                    return True
        return False

    def is_game_over(self) -> bool:
        """checking if the columns are full. If so, end the game"""
        for col in range(len(self._board)):
            for row in range(len(self._board[0:3])):
                if self._board[col][row] != EMPTY:
                    return True
        return False

    def tick(self, col: int) -> int:
        """this always triggers when checking for match, dropping, freezing , all the functionalities"""
        ready_to_match = self.drop(col)

        # only shove everything down once you've cleared after matches
        if self.clear():
            self.shove_down()
        # if there are frozen jewels, start matching
        if ready_to_match:
            self._match()
            # if there's no match and column full, game over
            if not self.theres_a_match():
                if self.is_game_over():
                    return 13
                else:
                    return 6
        else:
            return 6


    def clear(self) -> bool:
        """clears all the matches by turning them into EMPTY"""
        matched = False
        for col in range(len(self._board)):
            for row in range(len(self._board[1])):
                if self._board[col][row].startswith("*"):
                    self._board[col][row] = EMPTY
                    matched = True
        return matched

    def shove_down(self) -> None:
        """When there's blank spaces in between the elements in the col, shove everything to the bottom"""
        for col in self._board:
            while EMPTY in col:
                col.remove(EMPTY)
        for col in self._board:
            while len(col) < self._rows:
                col.insert(0, EMPTY)


if __name__ == "__main__":
    pass


