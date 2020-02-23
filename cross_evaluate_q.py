# -*- coding: utf-8 -*-
import asyncio
import time

from poke_env.player.random_player import RandomPlayer
from tabular_q_player import TabularQPlayer
from poke_env.player.utils import cross_evaluate
from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import LocalhostServerConfiguration
from tabulate import tabulate


async def main():
    start = time.time()

    # We define two player configurations.
    player_1_configuration = PlayerConfiguration("Random Player", None)
    player_2_configuration = PlayerConfiguration("Tabular Q Player", None)

    # We create the corresponding players.
    random_player = RandomPlayer(
        player_configuration=player_1_configuration,
        battle_format="gen7randombattle",
        server_configuration=LocalhostServerConfiguration,
    )
    tabular_q_player = TabularQPlayer(
        player_configuration=player_2_configuration,
        battle_format="gen7randombattle",
        server_configuration=LocalhostServerConfiguration,
    )

    # Now, let's evaluate our player
    cross_evaluation = await cross_evaluate(
        [random_player, tabular_q_player], n_challenges=100
    )

    print(
        "Tabular Q player won %d / 100 battles [this took %f seconds]"
        % (
            cross_evaluation[tabular_q_player.username][random_player.username] * 100,
            time.time() - start,
        )
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
