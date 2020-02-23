#
# Copyright 2017 Carsten Friedrich (Carsten.Friedrich@gmail.com). All rights reserved
#
from typing import Dict, List

from tic_tac_toe.Board import Board, GameResult, NAUGHT, CROSS #fix

from poke_env.player.player import Player

import numpy as np


#redefine rewards, win/loss, se, kos?

WIN_VALUE = 1.0  # type: float
DRAW_VALUE = 0.5  # type: float
LOSS_VALUE = 0.0  # type: float

    type_one = (battle.active_pokemon).type_1
    type_two = (battle.active_pokemon).type_2
    opp_type_one = (battle.opponent_active_pokemon).type_1
    opp_type_two = (battle.opponent_active_pokemon).type_2

    state_1 = {'t1': (battle.active_pokemon).type_1, 't2': (battle.active_pokemon).type_2, 'opt1': (battle.opponent_active_pokemon).type_1, 'ot2': (battle.opponent_active_pokemon).type_2} #non commutative

    state_2_t = 's: ' + str((battle.active_pokemon).type_1) + ' ' + str((battle.active_pokemon).type_2) + ', o: ' + str((battle.opponent_active_pokemon).type_1) + ' ' + str((battle.opponent_active_pokemon).type_1)

class TQPlayer(Player):
    """
   Tabular Q Learning player
    """

    def __init__(self, alpha=0.9, gamma=0.95, q_init=0.6): #choose these specifically
        """
        Called when creating a new TQPlayer. Accepts some optional parameters to define its learning behaviour
        :param alpha: The learning rate needs to be larger than 0 and smaller than 1
        :param gamma: The reward discount. Needs to be larger than 0  and should be smaller than 1. Values close to 1
            should work best.
        :param q_init: The initial q values for each move and state.
        """
        self.side = None
        self.q = {}  # type: Dict[int, np.ndarray]
        self.move_history = []  # type: List[(int, int)] #fix
        self.learning_rate = alpha
        self.value_discount = gamma
        self.q_init_val = q_init
        super().__init__()

    def get_q(self, state_2) -> np.ndarray:
        """
        Returns the q values for the state with hash value `board_hash`.
        :param board_hash: The hash value of the board state for which the q values should be returned
        :return: List of q values for the input state hash.
        """

        #
        # We build the Q table in a lazy manner, only adding a state when it is actually used for the first time
        #
        if state_2 in self.q: #fix
            qvals = self.q[state_2] #fix
        else:
            qvals = np.full(20, self.q_init_val) #status move, 18 offensive types, random switch = 20
            self.q[state_2] = qvals #fix

        return qvals

    def is_option(m) -> bool:
        if pokemon.moves #if one of the moves in the list is of the same type as m (define it as type somewhere? how does switch / status work?), eval to true

    def get_move(self, move) -> int: #reference other program, fix
        """
        Return the next move given the board `board` based on the current Q values
        :param board: The current board state
        :return: The next move based on the current Q values for the input state
        """

        state_2 = 's: ' + str((battle.active_pokemon).type_1) + ' ' + str((battle.active_pokemon).type_2) + ', o: ' + str((battle.opponent_active_pokemon).type_1) + ' ' + str((battle.opponent_active_pokemon).type_1)
        qvals = self.get_q(state_2)  # type: np.ndarray
        while True:
            m = np.argmax(qvals)  # type: int

            if move.is_option(m, #probably need some other def?): #redefine this function based on switches
                return m
            else:
                qvals[m] = -1.0

    def move(self, battle):
        # If the player can attack, it will
        if battle.available_moves:
            # Finds the best move among available one

            if (battle.active_pokemon).must_recharge == True:
                return self.choose_random_move(battle)

            else:
                m = self.get_move(battle)

                best_move = max(battle.available_moves, key=lambda move: get_move(move))
                return self.create_order(best_move)

        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)

    def move(self, battle):#use move object from other program
        """
        Makes a move and returns the game result after this move and whether the move ended the game
        :param board: The board to make a move on
        :return: The GameResult after this move, Flag to indicate whether the move finished the game
        """
        m = self.get_move(battle)
        self.move_history.append(('s: ' + str((battle.active_pokemon).type_1) + ' ' + str((battle.active_pokemon).type_2) + ', o: ' + str((battle.opponent_active_pokemon).type_1) + ' ' + str((battle.opponent_active_pokemon).type_1), m))
        _, res, finished = board.move(m, self.side)
        return res, finished

    def final_result(self, result: GameResult): #call correct game result, se, ko values
        """
        Gets called after the game has finished. Will update the current Q function based on the game outcome.
        :param result: The result of the game that has finished.
        """
        if (result == GameResult.NAUGHT_WIN and self.side == NAUGHT) or (
                result == GameResult.CROSS_WIN and self.side == CROSS):
            final_value = WIN_VALUE  # type: float
        elif (result == GameResult.NAUGHT_WIN and self.side == CROSS) or (
                result == GameResult.CROSS_WIN and self.side == NAUGHT):
            final_value = LOSS_VALUE  # type: float
        elif result == GameResult.DRAW:
            final_value = DRAW_VALUE  # type: float
        else:
            raise ValueError("Unexpected game result {}".format(result))

        self.move_history.reverse()
        next_max = -1.0  # type: float

        for h in self.move_history:
            qvals = self.get_q(h[0])
            if next_max < 0:  # First time through the loop
                qvals[h[1]] = final_value
            else:
                qvals[h[1]] = qvals[h[1]] * (
                            1.0 - self.learning_rate) + self.learning_rate * self.value_discount * next_max

            next_max = max(qvals)


#dont need this
    def new_game(self, side):
        """
        Called when a new game is about to start. Store which side we will play and reset our internal game state.
        :param side: Which side this player will play
        """
        self.side = side
        self.move_history = []
