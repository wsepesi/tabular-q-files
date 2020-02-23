import numpy as np

from poke_env.player.player import Player
from action import ActionUtil

from typing import Dict, List

WIN_VALUE = 1.0
LOSS_VALUE = 0.0

class TabularQPlayer(Player):

    def __init__(self, alpha = .9, gamma = .95, q_init = .6): #generic numbers, update w/ reason
        self.q = {}  # type: Dict[str, np.ndarray]
        self.move_history = []  # type: List[(str, int)]
        self.learning_rate = alpha
        self.value_discount = gamma
        self.q_init_val = q_init
        super().__init__()

    def get_q(self, state: str) -> np.ndarray:
        if state in self.q:
            qvals = self.q[state]

        else:
            qvals = self.full(19, self.q_init_val)
            self.q[state] = qvals

        return qvals

    def game_state(battle): #finds game state abstraction represented by self and opponent types (24,509 states possible)
        temp_state_s = [(battle.active_pokemon).type_1, (battle.active_pokemon).type_2]
        s_sort = temp_state_s.sort()
        s_string = ' '.join([str(elem) for elem in s_sort])

        temp_state_o = [(battle.opponent_active_pokemon).type_1, (battle.opponent_active_pokemon).type_2]
        o_sort = temp_state_o.sort()
        o_string = ' '.join([str(elem) for elem in o_sort])

        total_state = s_string + ', ' + o_string

        return total_state

    def get_move(self, battle) -> int:

        state = game_state(battle)
        qvals = self.get_q(state)
        while True:
            m = np.argmax(qvals)
            if ActionUtil.is_legal(m):
                return m
            else:
                qvals[m] = -1.0 #this works, but maybe causes problems - late fix

    def final_result(self, battle):
        if battle.won == True:
            final_value = WIN_VALUE
        elif battle.lost == True:
            final_value = LOSS_VALUE
        else:
            return

        self.move_history.reverse()
        next.max = -1.0

        for h in self.move_history: #doesn't reward se / penalize kos - late fix, would be a change to final_value
            qvals = self.get_q(h[0])
            if next_max < 0:
                qvals[h[1]] = final_value
            else:
                qvals[h[1]] = qvals[h[1]] * (
                            1.0 - self.learning_rate) + self.learning_rate * self.value_discount * next_max

            next_max = max(qvals)

        self.move_history = []

    def choose_move(self, battle):
        if battle.available_moves:

            if (battle.active_pokemon).must_recharge == True:
                return self.choose_random_move(battle)

            else:
                best_move_num = self.get_move(state) #convert 1D back to move type
                best_move = ActionUtil.num_to_move(best_move_num)
                return self.create_order(best_move)

        else:
            print('uh oh')
            return self.choose_random_move(battle)

        m = self.get_move(battle)
        self.move_history.append((game_state(battle), m))
        self.final_result(battle)
