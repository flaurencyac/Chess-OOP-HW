import random
import sys

class Player:
    "Abstract player class"

    def __init__(self, side=None) -> None:
        self.side = side

    def take_turn(self, game_state):
        raise NotImplementedError()

    @staticmethod
    def create_player(player_type):
        "Factory method for creating players"
        if player_type == "human":
            return HumanPlayer()
        elif player_type == "random":
            return RandomCompPlayer()
        elif player_type == "greedy":
            return GreedyCompPlayer()
        elif player_type[:7] == 'minimax':
            minimax_player = MinimaxPlayer()
            minimax_player.set_depth(int(player_type[-1]))
            return minimax_player
        else:
            return None


class MinimaxPlayer(Player):

    def __init__(self, *args, **kwargs):
        super(*args, **kwargs).__init__(*args, **kwargs)
        self._depth = None

    def set_depth(self, depth):
        self._depth = depth

    def take_turn(self, game_state):
        options = game_state.all_possible_moves()
        #selected_move.execute(game_state)
        '''heuristic: points based on piece
        checkers: peassant = 1, king = 2, sum any pieces captured
        chess: pawn = 1, bishops = 3, knights = 3, rooks = 5, queens = 9, kings 100
        make AI players generic and print their selected moove after printing the game turn and current player
        '''
        pass
        sys.exit(0)


class HumanPlayer(Player):
    "Concrete player class that prompts for moves via the command line"

    def take_turn(self, game_state):
        b = game_state.board
        while True:
            chosen_piece = input("Select a piece to move\n")
            chosen_piece = b.get_space(chosen_piece).piece
            if chosen_piece is None:
                print("no piece at that location")
                continue
            if chosen_piece.side != self.side:
                print("that is not your piece")
                continue
            options = chosen_piece.enumerate_moves()
            if len(options) == 0 or options[0] not in game_state.all_possible_moves():

                print("that piece cannot move")
                continue

            self._prompt_for_move(options).execute(game_state)
            return

    def _prompt_for_move(self, options):
        while True:
            for idx, op in enumerate(options):
                print(f"{idx}: {op}")
            chosen_move = input(
                "Select a move by entering the corresponding index\n")
            try:
                chosen_move = options[int(chosen_move)]
                return chosen_move
            except ValueError:
                print("not a valid option")


class RandomCompPlayer(Player):
    "Concrete player class that picks random moves"

    def take_turn(self, game_state):
        options = game_state.all_possible_moves()
        m = random.choice(options)
        print(m)
        m.execute(game_state)


class GreedyCompPlayer(Player):
    "Concrete player class that chooses moves that capture the greatest total value of pieces while breaking ties randomly"

    def take_turn(self, game_state):
        options = game_state.all_possible_moves()
        max_value = 0
        potential_moves = []
        for m in options:
            # get total pts from list of captures
            points = m.evaluate_captures()
            if points > max_value:
                potential_moves = [m]
                max_value = points
            elif points == max_value:
                potential_moves.append(m)

        selected_move = random.choice(potential_moves)
        print(selected_move)
        selected_move.execute(game_state)
