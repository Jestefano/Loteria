import numpy as np
import pandas as pd
from Game import Game

def one_simulation(rng, game, num_cards):
    winners = []
    cards = np.arange(num_cards)
    rng.shuffle(cards)
    idx = 0
    while (not winners):
        winners = game.mark(cards[idx])
        idx += 1

    num_cards_until_win = idx
    first_mid = game.get_first_mid()

    return (winners, num_cards_until_win, first_mid)
    
def simulations_given_game(rng, game, num_simulations, num_cards):
    winners_cum = []
    num_cards_until_win_cum = []
    first_mid_cum = []
    for _ in range(num_simulations):
        (winners,num_cards_until_win,first_mid) = one_simulation(rng, game, num_cards)
        winners_cum.append(winners)
        num_cards_until_win_cum.append(num_cards_until_win)
        first_mid_cum.append(first_mid)
        game.restart()
    return (winners_cum, num_cards_until_win_cum, first_mid_cum)

def simulation(num_games, num_simulations, rng = np.random.RandomState(42), \
    num_players = 3, num_squares = 16, num_cards = 54):
    results = pd.DataFrame()
    for i in range(num_games):
        game = Game(rng, num_players, num_squares, num_cards)
        (winners_cum, num_cards_until_win_cum, first_mid_cum) = \
            simulations_given_game(rng, game, num_simulations, num_cards)
        temp_results = pd.DataFrame({'num_game':[i for _ in range(num_simulations)],
        'winners':winners_cum,'num_cards_until_end':num_cards_until_win_cum,
        'first_mid':first_mid_cum})
        results = pd.concat([results,temp_results],axis = 0)
    return results


def main():
    df = simulation(num_games = 1, num_simulations = 50_000, num_players = 100)
    df.to_csv('data/simulation_{}.csv'.format(100),index=False)

main()