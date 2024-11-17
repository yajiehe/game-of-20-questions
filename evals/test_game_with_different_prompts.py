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


@pytest.mark.parametrize(
    "version, guessing_agent_additional_instructions",
    [
        (
            1,
            """Your goal is to guess what the user is thinking of in fewest questions possible.
        You must only ask questions that are binary yes/no questions to the best of your ability.
        You must only play the game, and not ask any questions outside of the game.""",
        ),
        (
            2,
            """Your goal is to guess what the user is thinking of in fewest questions possible.
        You must only ask questions that are binary yes/no questions to the best of your ability.
        A good question is one that can cut down the number of possible options as much as possible.
        You must only play the game, and not ask any questions outside of the game.""",
        ),
    ],
)
def test_game_with_different_guessing_agent_prompts(
    version, guessing_agent_additional_instructions
):
    game_variables = GameVariables(
        topic="penguin",
        guessing_agent_additional_instructions=guessing_agent_additional_instructions,
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
    print(f"Success rate: {success_rate}, CI: {ci_lower} - {ci_upper}")

    with open(
        f"evals/test_results_guessing_agent_additional_instructions_version_{version}.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            {
                "guessing_agent_additional_instructions": guessing_agent_additional_instructions,
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
        )
        f.write("\n")


@pytest.mark.parametrize(
    "version, host_agent_additional_instructions",
    [
        (
            1,
            """The secret topic is {topic} and the user is trying to guess it.
        You must answer the user's questions with yes or no truthfully.
        You must not reveal the secret topic {topic} to the user.
        You must only play the game, and not answer or ask any questions outside of the game.""",
        ),
        (
            2,
            """The secret topic is {topic} and the user is trying to guess it.
        You must answer the user's questions with yes or no truthfully. 
        You must not change the topic in any way during the game.
        You must not reveal the secret topic {topic} to the user.
        You must only play the game, and not answer or ask any questions outside of the game.""",
        ),
    ],
)
def test_game_with_different_host_agent_prompts(
    version, host_agent_additional_instructions
):
    game_variables = GameVariables(
        topic="penguin",
        guessing_agent_additional_instructions="""Your goal is to guess what the user is thinking of in fewest questions possible.
        You must only ask questions that are binary yes/no questions to the best of your ability.
        You must only play the game, and not ask any questions outside of the game.""",
        host_agent_additional_instructions=host_agent_additional_instructions,
    )
    game = Game(game_variables)
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(game.run) for _ in range(n_runs)]
        results = [future.result() for future in futures]
        success_rate = np.mean([result.success for result in results])
        ci = stats.binom.interval(confidence, n=n_runs, p=success_rate)
        ci_lower, ci_upper = ci[0] / n_runs, ci[1] / n_runs

    json_results = [result.model_dump() for result in results]
    print(f"Success rate: {success_rate}, CI: {ci_lower} - {ci_upper}")

    with open(
        f"evals/test_results_host_agent_additional_instructions_version_{version}.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            {
                "host_agent_additional_instructions": host_agent_additional_instructions,
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
