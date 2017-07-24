from tictac import *

def main():
    game = Game()
    while True:
        game.print_board()
        if len(game.current_board) > 0:
            print("Current board: " + Utils.format_board_number(game.current_board[0]))
        player =  game.get_current_player()
        player.parse(input("Player " + str(player.number) + ", your move? "))

if __name__ == "__main__":
    main()

