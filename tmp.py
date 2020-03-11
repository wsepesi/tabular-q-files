# -*- coding: utf-8 -*-
import asyncio
import time

from poke_env.player.player import Player
from poke_env.player.random_player import RandomPlayer
from poke_env.player.utils import cross_evaluate
from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import LocalhostServerConfiguration

#defines full max damage player to be tested against
class TrueMaxPlayer(Player):
    def choose_move(self, battle):
        # If the player can attack, it will
        if battle.available_moves:

            # Finds the best move among available one

            if (battle.active_pokemon).must_recharge == True:
                return self.choose_random_move(battle)

            else:

                def stab(move):
                    if (battle.active_pokemon).type_1 == move.type or (battle.active_pokemon).type_2 == move.type:
                        return 1.5

                    else:
                        return 1

                #effectiveness / stab / max base power
                best_move = max(battle.available_moves, key=lambda move: (stab(move))*int(move.base_power)*int((move.type).damage_multiplier((battle.opponent_active_pokemon).type_1, (battle.opponent_active_pokemon).type_2)))
                return self.create_order(best_move)

        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)

class SuperEffectivePlayer(Player):
    def choose_move(self, battle):
        # If the player can attack, it will
        if battle.available_moves:
            # Finds the best move among available one

            if (battle.active_pokemon).must_recharge == True:
                return self.choose_random_move(battle)

            else:
                best_move = max(battle.available_moves, key=lambda move: int(move.base_power)*int((move.type).damage_multiplier((battle.opponent_active_pokemon).type_1, (battle.opponent_active_pokemon).type_2)))
                return self.create_order(best_move)

        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)

class MaxDamagePlayer(Player):
    def choose_move(self, battle):
        # If the player can attack, it will
        if battle.available_moves:
            # Finds the best move among available ones
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            return self.create_order(best_move)

        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)

async def main():
    start = time.time()

    # We define two player configurations.
    player_1_configuration = PlayerConfiguration("Super Effective Player", None)
    player_2_configuration = PlayerConfiguration("True Max Player", None)

    # We create the corresponding players.
    super_effective_player = SuperEffectivePlayer(
        player_configuration=player_1_configuration,
        battle_format="gen7randombattle",
        server_configuration=LocalhostServerConfiguration,
    )
    true_max_player = TrueMaxPlayer(
        player_configuration=player_2_configuration,
        battle_format="gen7randombattle",
        server_configuration=LocalhostServerConfiguration,
    )

    # Now, let's evaluate our player
    cross_evaluation = await cross_evaluate(
        [super_effective_player, true_max_player], n_challenges=5000
    )

    print(
        "True Max Player won %d / 5000 battles [this took %f seconds]"
        % (
            cross_evaluation[true_max_player.username][super_effective_player.username] * 5000,
            time.time() - start,
        )
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
