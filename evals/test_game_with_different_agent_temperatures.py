import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import numpy as np
import pytest
from scipy import stats

from game import Game
from utils import GameVariables

n_runs = 10
confidence = 0.95


@pytest.mark.parametrize("guessing_agent_temperature", [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
def test_game_with_different_guessing_agent_temperatures(guessing_agent_temperature):
    game_variables = GameVariables(
        guessing_agent_temperature=guessing_agent_temperature,
        guessing_agent_additional_instructions="""Your goal is to guess what the user is thinking of in fewest questions possible.
        You must only ask questions that are binary yes/no questions to the best of your ability.
        You must only play the game, and not ask any questions outside of the game.""",
        host_agent_additional_instructions="""The secret topic is {topic} and the user is trying to guess it.
        You must answer the user's questions with yes or no truthfully.
        You must not reveal the secret topic {topic} to the user.
        You must only play the game, and not answer or ask any questions outside of the game.""",
    )
    game = Game(game_variables)
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(game.run) for _ in range(n_runs)]
        results = [future.result() for future in futures]
        success_rate = np.mean([result.success for result in results])
        mean_number_of_questions = np.mean(
            [result.number_of_questions for result in results if result.success is True]
        )
        ci = stats.binom.interval(confidence, n=n_runs, p=success_rate)
        ci_lower, ci_upper = ci[0] / n_runs, ci[1] / n_runs

    json_results = [result.model_dump() for result in results]
    print(
        f"Success rate: {success_rate} for guessing agent temperature {guessing_agent_temperature}, CI: {ci_lower} - {ci_upper}"
    )

    with open(
        f"evals/test_results_guessing_agent_temperature_{guessing_agent_temperature}.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            {
                "guessing_agent_temperature": guessing_agent_temperature,
                "n_runs": n_runs,
                "confidence": confidence,
                "success_rate": success_rate,
                "ci_lower": ci_lower,
                "ci_upper": ci_upper,
                "mean_number_of_questions": mean_number_of_questions,
                "game_variables": game_variables.model_dump(),
                "game_results": json_results,
            },
            f,
            indent=2,
        )
        f.write("\n")


@pytest.mark.parametrize("host_agent_temperature", [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
def test_game_with_different_host_agent_temperatures(host_agent_temperature):
    game_variables = GameVariables(
        host_agent_temperature=host_agent_temperature,
        guessing_agent_additional_instructions="""Your goal is to guess what the user is thinking of in fewest questions possible.
        You must only ask questions that are binary yes/no questions to the best of your ability.
        You must only play the game, and not ask any questions outside of the game.""",
        host_agent_additional_instructions="""The secret topic is {topic} and the user is trying to guess it.
        You must answer the user's questions with yes or no truthfully.
        You must not reveal the secret topic {topic} to the user.
        You must only play the game, and not answer or ask any questions outside of the game.""",
    )
    game = Game(game_variables)
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(game.run) for _ in range(n_runs)]
        results = [future.result() for future in futures]
        success_rate = np.mean([result.success for result in results])
        ci = stats.binom.interval(confidence, n=n_runs, p=success_rate)
        ci_lower, ci_upper = ci[0] / n_runs, ci[1] / n_runs

    json_results = [result.model_dump() for result in results]
    print(
        f"Success rate: {success_rate} for host agent temperature {host_agent_temperature}, CI: {ci_lower} - {ci_upper}"
    )

    with open(
        f"evals/test_results_host_agent_temperature_{host_agent_temperature}.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            {
                "host_agent_temperature": host_agent_temperature,
                "n_runs": n_runs,
                "confidence": confidence,
                "success_rate": success_rate,
                "ci_lower": ci_lower,
                "ci_upper": ci_upper,
                "game_variables": game_variables.model_dump(),
                "game_results": json_results,
            },
            f,
        )
        f.write("\n")
