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
        #print selected move after printing the game turn and current player
        options = game_state.all_possible_moves()
        selected_move = do_minimax(game_state, self._depth)[0]
        print(selected_move)
        selected_move.execute(game_state)

    def do_minimax(self, node, depth):
        if leaf(node) or depth == 0:
            return evaluate_board(node)
        moves = node.all_possible_moves()
        if node.current_side == WHITE:
            max_pts = -infinity
            for move in moves:
                move.execute(node)
                cur_pts = do_minimax(node, depth -1)
                move.undo(node)
                if cur_pts >= max_pts:
                    max_pts = cur_pts
                    final_move = move
            return [final_move, max_pts]
        elif node.current_side == BLACK:
            min_pts = infinity
            for move in moves:
                move.execute(node)
                cur_pts = do_minimax(node, depth -1)
                move.undo(node)
                if cur_pts <= min_pts:
                    min_pts = cur_pts
                    final_move = move
            return [final_move, min_pts]

    def leaf(self, game_state):
        "Checks if a node is a leaf by checking if it has children nodes"
        if game_state.check_draw() == True or game_state.check_loss() == True:
            return True

    def evaluate_board(self, game_state):
        "Scores a game_state with pieces left on the board, b, returns white - black"
        black = 0
        white = 0
        #obtain list of every piece on the board
        pieces = game_state._board.pieces_iterator()
        for piece in pieces:
            if piece.side() == WHITE:
                white += piece.value
            elif piece.side() == BLACK:
                black += piece.value
        if white == 0:
            # means white lost
            return -infinity
        elif black == 0:
            # means black lost
            return infinity
        else:
            return white - black
            # return 0, a tie
            # return < 0, black is in the lead
            # return > 0, white is in the lead

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

#make the AI players print their selected move after printing the game turn and current player 
class GreedyCompPlayer(Player):
    "Concrete player class that chooses moves that capture the greatest total value of pieces while breaking ties randomly"

    def take_turn(self, game_state):
        options = game_state.all_possible_moves()
        max_captured = 0
        max_moves_dictionary = {}
        ''' dictionary keeps track of the highest points captured by a move and the moves that capture that amount of points
         key = points_captured
         val = moves that capture that amount of points
         dictionary = {
             1 : [moveA, moveD]
             5 : [moveB, moveC]
         }
        '''
        # the for loop runs through all list of posssible moves and updates the counter for max_points_captured 
        # and the dictionary to reflect those moves
        for m in options:
            # get total pts from list of captures
            points_captured = m.evaluate_captures()
            if points_captured > max_captured:
                max_moves_dictionary[points_captured] = [m]
                max_captured = points_captured
            elif points_captured == max_captured:
                max_moves_dictionary[points_captured].append(m)
        # after for loop is done we have the highest max_captured, and so we go into the dictionary to find
        # which moves result in max_captured, we choose a random move from that list
        selected_move = random.choice(max_moves_dictionary[max_captured])
        print(selected_move)
        selected_move.execute(game_state)
