import numpy as np

from player_test import Player
from poke_env.player.utils import cross_evaluate
from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import LocalhostServerConfiguration

from action import ActionUtil

from enum import Enum

from typing import Dict, List

#defines basic training values
WIN_VALUE = 1.0
LOSS_VALUE = 0.0

#creates tabular q class
class TabularQPlayer(Player):

    #generates q table as states occur for the first time and update array, if state exists returns existing q values
    def get_q(self, state: str) -> np.ndarray:

        if state in self.q:
            qvals = self.q[state]

        else:
            qvals = np.full(19, self.q_init_val)
            self.q[state] = qvals

        return qvals

    #finds (very) simple game state abstraction as defending type vs opposing type, actions represented by move type (future work can make this a more accurate representation of state/action)
    def game_state(self, battle): #24,509 states possible
        s_type_1 = (battle.active_pokemon).type_1
        s_type_1_n = s_type_1.name

        o_type_1 = (battle.opponent_active_pokemon).type_1
        o_type_1_n = o_type_1.name

        s_type_2 = (battle.active_pokemon).type_2
        if s_type_2:
            s_type_2_n = s_type_2.name
            s_sort = str(s_type_1_n) + ' ' + str(s_type_2_n)
        else:
            s_sort = str(s_type_1_n)

        o_type_2 = (battle.opponent_active_pokemon).type_2
        if o_type_2:
            o_type_2_n = o_type_2.name
            o_sort = str(o_type_1_n) + ' ' + str(o_type_2_n)

        else:
            o_sort = str(o_type_1_n)

        #note: likely a better way to accomplish this, goal was to pull types and then make them commutative (fire water same as water fire) and alphabetization accomplished this
        total_state = s_sort + ', ' + o_sort

        return total_state

    #calls q table for current state to return best legal action
    def get_move(self, battle) -> int:
        state = self.game_state(battle)
        qvals = self.get_q(state)
        while True: #loops legality check
            m = np.argmax(qvals)
            if ActionUtil.is_legal(battle, m):
                return m #returns move if legal
            else:
                qvals[m] = qvals[m] - 1.0 #if not legal, discounts move for state but not so much that it will never be called if another pokemon has a different set of moves

    #called from other file when game is complete
    def train(self, p2_rate):
        rate = int(p2_rate)
        if rate == 1:
            final_value = WIN_VALUE
        elif rate == 0:
            final_value = LOSS_VALUE
        else:
            print('win rate error')

        #calls and reverses move history to assign descending reward
        h = self.move_history
        self.move_history.reverse()
        next_max = -1.0

        for h in self.move_history: #assign rewards with discount value defined in player class (future work should implement reward at points within the game instead of end result only)
            qvals = self.get_q(h[0])
            if next_max < 0:
                qvals[h[1]] = final_value
            else:
                qvals[h[1]] = qvals[h[1]] * (
                            1.0 - self.learning_rate) + self.learning_rate * self.value_discount * next_max

            next_max = max(qvals)

        self.move_history = []

    #(mostly) regular choose move function from poke-env
    def choose_move(self, battle):
        if battle.available_moves:
            if (battle.active_pokemon).must_recharge == True: #slaking error workaround (think this is bugged for code as a whole bc i got the same problem with the max damage player)
                return self.choose_random_move(battle)
            elif len(battle.available_moves) == 1: #struggle workaround (issue with my state representation)
                return self.choose_random_move(battle)
            elif str(battle.active_pokemon) == 'Kecleon (pokemon object)': #protean workaround (issue with my state representation)
                return self.choose_random_move(battle)
            else:
                best_move_num = self.get_move(battle)
                best_move = ActionUtil.num_to_move(battle, best_move_num) #get move returns number from q table corresponding to type enumeration, this converts to real move


        else:
            return self.choose_random_move(battle)

        #updates move history
        m = self.get_move(battle)
        self.move_history.append((self.game_state(battle), m))
        return self.create_order(best_move)
