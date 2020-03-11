from enum import Enum

from poke_env.environment.battle import Battle
from poke_env.environment.move import Move
from poke_env.environment.pokemon import Pokemon
from poke_env.environment.move_category import MoveCategory

#extra functions that i didnt want to throw all into the main class
class ActionUtil:
    #converts move to type enumeration (1-18 as defined by poke-env, 19 is status)
    def move_to_num(move: Move) -> int:
        print('move to num started')
        cat = move.category
        val = cat.value

        if val == 3:
            return 18

        else:
            n = int((move.type).value) - 1
            return n

    #checks legality (but favors legal moves in higher numbered slots)
    def is_legal(battle, move: int) -> bool:
        options = battle.available_moves

        for i in options:

            cat = i.category
            val = cat.value

            if val == 3:
                num = 18

            else:
                num = int((i.type).value) - 1

            if num == move:
                return True

        else:
            return False

    #converts enumeration back to actual move
    def num_to_move(battle, move: int) -> Move: 
        options = battle.available_moves

        for i in options:

            cat = i.category
            val = cat.value

            if val == 3:
                num = 18

            else:
                num = int((i.type).value) - 1

            if num == move:
                return i
