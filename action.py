from enum import Enum

from poke_env.environment.battle import Battle
from poke_env.environment.move import Move
from poke_env.environment.pokemon import Pokemon
from poke_env.environment.move_category import MoveCategory

class ActionUtil:
    def move_to_num(move: Move) -> int:
        if (move.category).value == 3:
            return 19
        else:
            return (move.type).value

    def is_legal(move: int) -> bool: #getting passed num version of action from tab q
        options = battle.available_moves

        for i in options:
            if num_to_str(options[i]) == move: #favors slot 1
                return True
        else:
            return False

    def num_to_move(move: int) -> Move:
        options = battle.available_moves

        for i in options:
            if num_to_str(options[i]) == move:
                return options[i]
