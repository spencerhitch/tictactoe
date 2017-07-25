import time, re

class Game:
    def __init__(self):
        self.current_pos = None
        self.boards = [[MiniBoard(i, j) for i in range(3)] for j in range(3)]
        self.players = []
        self.add_player()
        self.add_player()
        self.current_player = 1
        self.current_board = []

    def add_player(self):
        if len(self.players) < 2:
            player = Player(self)
            self.players.append(player)
        else:
            print("Maximum number of players is 2")

    def is_current_board(self, mini):
        return len(self.current_board) == 0 or self.current_board[0] == mini.number

    def get_current_player(self):
        return self.players[self.current_player - 1]

    def set_next_player(self):
        self.current_player = self.current_player % 2 + 1

    def move(self, coord, player_number):
        change_set = self.find_coord(coord)
        mini = self.boards[change_set["board"][1]][change_set["board"][0]]
        if not self.is_current_board(mini):
            Utils.print_rule("Your next move must be on board " + 
                str(self.current_board[0]))
        elif mini.is_won():
            Utils.print_rule("This board is already won, play anywhere else!")
        else:
            y = change_set["cell"][1]
            x = change_set["cell"][0]
            next_board = mini.move(x, y, player_number)
            next_y = next_board[1]
            next_x = next_board[0]
            if not mini.is_won() and not self.boards[next_y][next_x].is_won():
                self.current_board = [next_board]
            else:
                self.check_winning_win(change_set["board"])
                self.current_board = []
            self.set_next_player()

    def check_winning_win(self, coord):
        x = coord[0]
        y = coord[1]
        candidate = self.boards[y][x].winner
        for i in range(-1,2):
            for j in range(-1,2):
                coord0 = y + i
                coord1 = x + j
                coord0_next = (y + 2*i) % 3
                coord1_next = (x + 2*j) % 3
                if (not (coord0 == y and coord1 == x) and
                    coord0 < 3 and 
                    coord1 < 3 and
                    self.boards[coord0][coord1].winner == candidate and 
                    self.boards[coord0_next][coord1_next].winner == candidate):
                    print("Player " + candidate + " has won the game!")
                    exit()


    def find_coord(self, coord):
        board_y = int(coord[1]) // 3
        cell_y = int(coord[1]) % 3
        x = ord(coord[0]) - 65
        board_x = x // 3
        cell_x = x % 3
        return {"board":(board_x,board_y),"cell":(cell_x,cell_y)}

    def print_board(self):
        print("")
        for i in range(3):
            rows = [[],[],[]]
            for j in range(3):
                for k in range(3):
                    row = self.boards[i][j].board[k]
                    rows[k].append(' │ '.join(map(Utils.print_format, row)))
            for j in range(3):
                print(str(i*3 + j) + " " + str(" ║ ".join(rows[j])))
                if j == 2:
                    print(' ═══════════╬═══════════╬══════════')
                else:
                    print(' ───┼───┼───╫───┼───┼───╫───┼───┼───')

        print('  A   B   C   D   E   F   G   H   I ')
        print("")

class MiniBoard:
    def __init__(self, x, y):
        self.board = [[0 for n in range(3)] for n in range(3)]
        self.winner = 0
        self.number = (x,y)

    def is_won(self):
        return self.winner != 0 

    def move(self, x, y, player_number):
        self.board[y][x] = player_number
        self.winner = self.check_winning_move(x,y)
        if self.winner > 0:
            print("Player " + 
                    str(self.winner) +
                    " has won Board " +
                    Utils.format_board_number(self.number))
        return (x,y)

    def check_winning_move(self, x, y):
        candidate = self.board[y][x]
        for i in range(-1,2):
            for j in range(-1,2):
                coord0 = y + i
                coord1 = x + j
                coord0_next = (y + 2*i) % 3
                coord1_next = (x + 2*j) % 3
                if (not (coord0 == y and coord1 == x) and
                    coord0 < 3 and 
                    coord1 < 3 and
                    self.board[coord0][coord1] == candidate and 
                    self.board[coord0_next][coord1_next] == candidate):
                    return candidate
        return 0

class Player:
    def __init__(self, game):
       self.game = game
       self.number = len(game.players) + 1

    def parse(self, coord):
        parsed = coord.split(",")
        if (len(parsed) != 2
            or not re.match(r"[A-I]",parsed[0])
            or not re.match(r"[0-8]",parsed[1])):
            Utils.print_rule("Valid coordinates consist of A-H and 0-8 seperated by a comma")
            return
        self.game.move(parsed, self.number)

class Utils:
    @staticmethod
    def print_rule(s):
        print("\n################# RULE ##################")
        print(s)
        print("##########################################\n")
        time.sleep(4)

    @staticmethod
    def print_format(item):
        if item == 0:
            return ' '
        if item == 1:
            return 'X'
        if item == 2:
            return 'O'

    @staticmethod
    def format_board_number(coord):
        x = coord[0] * 3 + 65
        y = coord[1] * 3
        print_x = chr(x) + "-"  + chr(x + 2)
        print_y = str(y) + "-" + str(y + 2)
        return print_x + ", " + print_y

