# -*- coding: utf-8 -*-
import asyncio
import time

from poke_env.player.random_player import RandomPlayer
from player_test import Player
from tabular_q_player_test import TabularQPlayer
from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import LocalhostServerConfiguration
from poke_env.environment.battle import Battle

from tabulate import tabulate

from poke_env.player.player import Player
from poke_env.utils import to_id_str
from typing import Dict
from typing import List
from typing import Optional

import asyncio

#manages cross evaluation of tab q and other agent (set rn to random), I ran an edited version of this on jupyter to create a graph of win rates over time
async def cross_evaluate(
    players: List[Player], n_challenges: int
) -> Dict[str, Dict[str, Optional[float]]]:
    results = {p_1.username: {p_2.username: None for p_2 in players} for p_1 in players}
    for i, p_1 in enumerate(players):
        for j, p_2 in enumerate(players):
            if j <= i:
                continue
            await asyncio.gather(
                p_1.send_challenges(
                    opponent=to_id_str(p_2.username),
                    n_challenges=n_challenges,
                    to_wait=p_2.logged_in,
                ),
                p_2.accept_challenges(
                    opponent=to_id_str(p_1.username), n_challenges=n_challenges
                ),
            )
            results[p_1.username][p_2.username] = p_1.win_rate  # pyre-ignore
            results[p_2.username][p_1.username] = p_2.win_rate  # pyre-ignore

            battles = p_2._battles
            for value in battles:
                aValue = value

            value = battles[str(aValue)]

            #training workaround, only trains after 1 game and doesnt work with concurrent games
            TabularQPlayer.train(p_2, p_2.win_rate)

            p_1.reset_battles()
            p_2.reset_battles()
    return results  # pyre-ignore

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

    #defines training protocols
    spars = 10
    battles = 100
    n_challenges = 1

    q_wins = []
    game_count = []

    for s in range(spars):
        print('spar ' + str(s))

        battle_wins = 0

        for b in range(battles):
            cross_evaluation = await cross_evaluate(
                [random_player, tabular_q_player], n_challenges
            )

            battle_win_rate = cross_evaluation[tabular_q_player.username][random_player.username]

            battle_wins = battle_wins + battle_win_rate

        #information for matplotlib graphing on jupyter
        q_wins.append(((battle_wins)/(battles))*100.0)
        game_count.append((s+1)*battles)

    print('done')
    print(q_wins)
    print(game_count)
    print(time.time() - start)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
