#!/usr/bin/env python3
# encoding: utf-8
"""
tournament.py

Code to play a round robin tournament between dots-and-boxes agents.

Created by Pieter Robberechts, Wannes Meert.
Copyright (c) 2022 KU Leuven. All rights reserved.
"""
import importlib.util
import itertools
import logging
import os
import sys
from pathlib import Path
import errno
import os
import signal
import functools
import copy
import cProfile
import pstats

import click
import pandas as pd
import numpy as np
from tqdm import tqdm

import pyspiel
from open_spiel.python.algorithms.evaluate_bots import evaluate_bots

logger = logging.getLogger('be.kuleuven.cs.dtai.dotsandboxes.tournament')


def evaluate_bots(state, bots, rng):
    """Plays bots against each other, returns terminal utility for each bot.

    Patched from open_spiel/python/algorithms/evaluate_bots.py to pass a copy
    of the game state to the agents.
    """
    for bot in bots:
        bot.restart_at(copy.deepcopy(state))
    while not state.is_terminal():
        if state.is_chance_node():
            outcomes, probs = zip(*state.chance_outcomes())
            action = rng.choice(outcomes, p=probs)
            for bot in bots:
                bot.inform_action(copy.deepcopy(state), pyspiel.PlayerId.CHANCE, action)
            state.apply_action(action)
        elif state.is_simultaneous_node():
            joint_actions = [
                bot.step(copy.deepcopy(state))
                if state.legal_actions(player_id) else pyspiel.INVALID_ACTION
                for player_id, bot in enumerate(bots)
            ]
            state.apply_actions(joint_actions)
        else:
            current_player = state.current_player()
            action = bots[current_player].step(copy.deepcopy(state))
            for i, bot in enumerate(bots):
                if i != current_player:
                    bot.inform_action(copy.deepcopy(state), current_player, action)
            state.apply_action(action)
    return state.returns()


def load_agent(path, player_id):
    """Initialize an agent from a 'dotsandboxes_agent.py' file.
    """
    module_dir = os.path.dirname(os.path.abspath(path))
    sys.path.insert(1, module_dir)
    spec = importlib.util.spec_from_file_location("dotsandboxes_agent", path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo.get_agent_for_tournament(player_id)


def load_agent_from_dir(agent_id, path):
    """Scrapes a directory for an dots-and-boxes agent.

    This function searches all subdirectories for an 'dotsandboxes_agent.py' file and
    calls the ``get_agent_for_tournament`` method to create an instance of
    a player 1 and player 2 agent. If multiple matching files are found,
    a random one will be used.
    """
    print(path)
    print(agent_id)
    print(next(Path(path).glob('**/dotsandboxes_agent.py')))
    agent_path = next(Path(path).glob('**/dotsandboxes_agent.py'))
    try:
        return {
            'id':  agent_id,
            'agent_p1': load_agent(agent_path, 0),
            'agent_p2': load_agent(agent_path, 1),
        }
    except Exception as e:
        logger.exception("Failed to load %s" % agent_id)

class TimeoutError(Exception):
    pass

def timeout(seconds=1., error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(signal.ITIMER_REAL, seconds) 
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapper

    return decorator


def play_match(game, agent1, agent2, seed=1234, rounds=100, timeout_ms=200):
    """Play a set of games between two agents.
    """
    # Set timers for each agent
    for agent in (agent1, agent2):
        for player in ('agent_p1', 'agent_p2'):
            agent[player].step = timeout(seconds=timeout_ms/1000, error_message=f"Timeout for agent {agent['id']}")(agent[player].step)
    # Play tournament
    rng = np.random.RandomState(seed)
    results = []
    for _ in tqdm(range(rounds)):
        # Alternate between the two agents as p1 and p2
        for (p1, p2) in [(agent1, agent2), (agent2, agent1)]:
            try:
                returns = evaluate_bots(
                        game.new_initial_state(),
                        [p1['agent_p1'], p2['agent_p2']],
                        rng)
                error = None
            except Exception as ex:
                logger.exception("Failed to play between %s and %s" % (agent1['id'], agent2['id']))
                template = "An exception of type {0} occurred. Message: {1}"
                error = template.format(type(ex).__name__, ex)
                returns = [None, None]
            finally:
                results.append({
                    "agent_p1": p1['id'],
                    "agent_p2": p2['id'],
                    "return_p1": returns[0],
                    "return_p2": returns[1],
                    "error": error
                })
    return results


@click.command()
@click.argument('agent1_id', type=str)
@click.argument('agent1_dir', type=click.Path(exists=True))
@click.argument('agent2_id', type=str)
@click.argument('agent2_dir', type=click.Path(exists=True))
@click.argument('output', type=click.Path(exists=False))
@click.option('--rounds', default=250, help='Number of rounds to play.')
@click.option('--num_rows', default=7, help='Number of rows.')
@click.option('--num_cols', default=7, help='Number of cols.')
@click.option('--timeout', default=200, help='Max time (in ms) to reply')
@click.option('--seed', default=1234, help='Random seed')
def cli(agent1_id, agent1_dir, agent2_id, agent2_dir, output, rounds, timeout, num_rows, num_cols, seed):
    """Play a set of games between two agents."""
    logging.basicConfig(level=logging.INFO)

    # Create the game
    dotsandboxes_game_string = (
        "dots_and_boxes(num_rows={},"
        "num_cols={})").format(num_rows, num_cols)
    logger.info("Creating game: {}".format(dotsandboxes_game_string))
    game = pyspiel.load_game(dotsandboxes_game_string)
    # Load the agents
    logger.info("Loading the agents")
    agent1 = load_agent_from_dir(agent1_id, agent1_dir)
    agent2 = load_agent_from_dir(agent2_id, agent2_dir)
    # Play the tournament
    logger.info("Playing {} matches between {} and {}".format(rounds, agent1_id,  agent2_id))
    with cProfile.Profile() as profile: 

        results = play_match(game, agent1, agent2, seed, rounds, timeout)
    # Process the results
    logger.info("Processing the results")
    results = pd.DataFrame(results)
    results.to_csv(output, index=False)
    logger.info("Done. Results saved to {}".format(output))


    res = pstats.Stats(profile)
    res.sort_stats(pstats.SortKey.TIME)
    res.dump_stats(f"data/profiler/{agent1_id}vs{agent2_id}.prof")

if __name__ == '__main__':
    sys.exit(cli())

