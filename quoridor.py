# Author: Devon Miller
# Date: July 2022
# Description: two player game quoridor using object oriented programing with flask ui

import copy

class QuoridorGame:
    def __init__(self):
        """initialize board turn fences position and game state"""

        self._board = self.initialiseGrid()
        self._game_state = "unfinished"
        self._player_1_fences = 10
        self._player_2_fences = 10
        self._turn = "player_1"
        self._player_1_position = [0, 8]                     
        self._player_2_position = [16, 8]
                             

    def initialiseGrid(self):
        """initialize board, only called by init method
        i = an empty spacea a fence may ocupy
        O = an empty space a pawn may move into
        + donotes the edges of a playable space"""

        empty_row = ["O"] * 17 
        for i in range(17):
            if i % 2 != 0:
                empty_row[i] = "i"
        base_row1 = copy.deepcopy(empty_row)
        base_row1[8] = "player_1"
        base_row2 = copy.deepcopy(empty_row)
        base_row2[8] = "player_2"
        wall_row = ["i", "+", "i", "+", "i", "+", "i", "+", "i", "+", "i", "+", "i", "+", "i", "+", "i"] 
        grid = [base_row1, wall_row,  empty_row, wall_row,  empty_row, wall_row,  empty_row, wall_row,
        empty_row, wall_row,  empty_row, wall_row,  empty_row, wall_row,  empty_row, wall_row, base_row2] 
        return grid


    def add_fence(self, x, y, direction):
        """called when player adds fence, does initial validation and calls method to check
        fairplay rule, see rules for details"""

        if (self._turn == "player_1" and self._player_1_fences == 0) or \
            (self._turn == "player_2" and self._player_2_fences == 0):
            return "False0"
        x = (x-1) * 2
        y = (y-1) * 2
        if direction == "Verticle":
            y -= 1
        else:
            x-= 1
        if x > 15 or x < 1 or y > 16 or y < 0:
            return "False12"
        if self.check_fairplay(x, y):
            return "False1"
        if self._board[x][y] != "i":
            return "False2"
        return self.place_fence(x, y, direction)
            

    def check_fairplay(self, x, y):
        """checks fairplay rule returns method which returns true if move not allowed"""

        temp_board = copy.deepcopy(self._board)
        row = copy.deepcopy(temp_board[x])
        row[y] = "fence"
        temp_board[x] = row
        if self._turn == "player_1":
            cur = self._player_2_position
            return self.fairplay(cur[0], cur[1], 0, temp_board)
        else:
            cur = self._player_1_position
            return self.fairplay(cur[0], cur[1], 16, temp_board)
        

    def fairplay(self, x, y, target, board):
        """checks fiarplay rule returns true if rule broken and move not allowed"""

        board[x][y] = "blue"
        moves = [[x>0, x-2, y, x-1, y], [x<16, x+2, y, x+1, y], [y>0, x, y-2, x, y-1], [y<16, x, y+2, x, y+1]]
        for move in moves:
            if move[0]:
                if board[move[1]][move[2]] == "O" and board[move[3]][move[4]] == "i":
                    row = copy.deepcopy(board[move[1]])
                    row[move[2]] = "blue"
                    board[move[1]] = row
                    self.fairplay(move[1], move[2], target, board)
        if "blue" in board[target]:  # move is valid
            return False
        return True


    def place_fence(self, x, y, direction):
        """places fence after all validation done in prior methods"""

        row = copy.deepcopy(self._board[x])
        if direction == "Horizontal":
            row[y] = "H"
        else:                 
            row[y] = "V"
        self._board[x] = row
        if self._turn == "player_1":
            self._player_1_fences -= 1
            self._turn = "player_2"
        else:
            self._player_2_fences -= 1
            self._turn = "player_1"
        return True

        
    def movePawn(self, x, y):
        """called when player moves their pawn does initial validation and determines 
        type of move, normal, diagonal or jump"""

        turn = self._turn
        x = (x - 1) * 2
        y = (y - 1) * 2
        if (x > 16 or x < 0) or (y > 16 or y < 0):  # in bounds
            return "False00"
        if self._board[x][y] != "O":
            return "FalseAA"
        current_space = self._player_2_position
        if turn == "player_1":
            current_space = self._player_1_position
        cur_x = current_space[0]
        cur_y = current_space[1]
        if (self._player_1_position[0] == self._player_2_position[0] and \
            (self._player_1_position[1] - 2 == self._player_2_position[1] or \
            self._player_1_position[1] + 2 == self._player_2_position[1])) or \
                (self._player_1_position[1] == self._player_2_position[1] and \
                (self._player_1_position[0] - 2 == self._player_2_position[0] or \
                self._player_1_position[0] + 2 == self._player_2_position[0])):
            return self.move_diagonal_or_jump(x, y, current_space)        # pawns touching
        if (cur_x - 2 != x and cur_x + 2 != x and cur_x != x) or \
                (cur_y - 2 != y and cur_y + 2 != y and cur_y != y) or \
                (self._board[x][y] != "O"):
                return "False1"
        return self.validate_normal(x, y, current_space)


    def validate_normal(self, x, y, current_space):
        """performs validation for normal move"""

        cur_x = current_space[0]
        cur_y = current_space[1]
        if cur_x > x:
            direction = 0  # up
        elif cur_x < x:
            direction = 1  # down
        elif cur_y > y:
            direction = 2  # left
        else:
            direction = 3  # right
        validate = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
        move = validate[direction]
        if self._board[move[0]][move[1]] != "i":
            return False
        self.make_move(x, y, current_space)


    def move_diagonal_or_jump(self, x, y, current_space):
        """performs initial validation of jump or diagonal and determines if move
        is jump or diagonal"""
        cur_x = current_space[0]
        cur_y = current_space[1]
        if (cur_x - 4 == x or cur_x + 4 == x and cur_y == y) or \
            (cur_y - 4 == y or cur_y + 4 == y and cur_x == y):
            return self.validate_jump(x, y, current_space)
        if (cur_x - 2 == x or cur_x + 2 == x and cur_y == y) or \
            (cur_y - 2 == y or cur_y + 2 == y and cur_x == y):
            return self.make_move(x, y, current_space)     #not diagonal or jump
        if (cur_x - 2 == x or cur_x + 2 == x) and (cur_y-2 == y or cur_y+2 == y):
            return self.validate_diagonal(x, y, current_space)
        return False


    def validate_diagonal(self, x, y, current_space):
        """validate diagonal moves returns false if not valid"""

        cur_x = current_space[0]
        cur_y = current_space[1]
        moves = [[cur_x-1, cur_y], [cur_x+1, cur_y], [cur_x, cur_y+1], [cur_x, cur_y-1]]
        for move in moves:
            try:
                if self._board[move[0]][move[1]] != "i":
                    return make_move(x, y, current_space)
            except:
                continue
        return "FalseCC"


    def validate_jump(self, x, y, current_space):
        """performs validation on jumps, returns false if invalid"""

        cur_x = current_space[0]
        cur_y = current_space[1]
        if cur_x > x:
            direction = 0      #up
        elif cur_x < x:
            direction = 1       #down
        elif cur_y > y:
            direction = 2        #left
        else:
            direction = 3        #right
        validate = [[x+1, x+2, x+3, y, y, y], [x-1, x-2, x-3, y, y, y], [x, x, x, y+1, y+2, y+3], [x, x, x, y-1, y-2, y-3]]
        move = validate[direction]
        if self._board[move[0]][move[3]] != "i" or self._board[move[2]][move[5]] != "i":
            return (self._board, self._board[move[0]][move[3]], self._board[move[2]][move[5]] )
        if self._board[move[1]][move[4]] == "O":
            return "FalseEE"
        self.make_move(x, y, current_space)
    

    def make_move(self, x, y, current_space):
        """move is valid and board updated"""

        row = copy.deepcopy(self._board[x])
        row[y] = self._turn
        self._board[x] = row
        self._board[current_space[0]][current_space[1]] = "O"
        if self._turn == "player_1":
            self._player_1_position = (x, y)
            self._turn = "player_2"
        else:
            self._player_2_position = (x, y)
            self._turn = "player_1"
        return True


    def return_game_state(self):
        """returns game state"""

        return self._game_state


    def check_winner(self):
        """checks if game has been won"""

        if self._turn == "player_2":
            for x in range(17):
                if self._board[16][x] == "player_1":
                    self._game_state = "Won"
                    return True
        else:
             for x in range(17):
                if self._board[0][x] == "player_2":
                    self._game_state = "Won"
                    return True
        return False


    def return_board(self):
        """returns board for display"""

        return self._board

    def return_turn(self):
        """returns turn for display"""

        return self._turn

    def return_fences(self):
        """returns fences to be displayed"""

        return (self._player_1_fences, self._player_2_fences)