import re
import uuid
from collections import defaultdict
from typing import Any, Callable, List, Optional, Union

from agent_client import AgentClient
from utils import Agent, GameResult, GameVariables, bcolors


class Game:
    def __init__(self, game_variables: GameVariables):
        self.run_id = str(uuid.uuid4())
        self.client = AgentClient()
        self.game_variables = game_variables

    def host_agent_instructions(self) -> str:
        topic = self.game_variables.topic
        additional_instructions = (
            self.game_variables.host_agent_additional_instructions.format(topic=topic)
        )
        host_agent_prompt = """You are playing a game of 20 questions as the host agent.
        {additional_instructions}
        """
        return host_agent_prompt.format(additional_instructions=additional_instructions)

    def guessing_agent_instructions(self) -> str:
        additional_instructions = (
            self.game_variables.guessing_agent_additional_instructions
        )
        guessing_agent_prompt = """You are playing a game of 20 questions as the guessing agent.
        {additional_instructions}
        """
        return guessing_agent_prompt.format(
            additional_instructions=additional_instructions
        )

    def run(self) -> GameResult:
        host_agent = Agent(
            name="Host Agent", instructions=self.host_agent_instructions()
        )
        guessing_agent = Agent(
            name="Guessing Agent",
            instructions=self.guessing_agent_instructions(),
        )
        chat_history: List[dict] = []
        try:
            while True:
                host_agent_response = self.client.run(
                    host_agent,
                    chat_history=chat_history,
                    temperature=self.game_variables.host_agent_temperature,
                    json_response=False,
                )
                print(
                    bcolors.HOST
                    + f"Host Agent: {host_agent_response.messages[-1]['content']}"
                    + bcolors.ENDC
                )
                chat_history.extend(host_agent_response.messages)

                guessing_agent_response = self.client.run(
                    guessing_agent,
                    chat_history=chat_history,
                    temperature=self.game_variables.guessing_agent_temperature,
                    json_response=False,
                )
                print(
                    bcolors.AGENT
                    + f"Guessing Agent: {guessing_agent_response.messages[-1]['content']}"
                    + bcolors.ENDC
                )

                chat_history.extend(guessing_agent_response.messages)

                last_guessing_agent_response = guessing_agent_response.messages[-1][
                    "content"
                ].lower()
                number_of_questions = len(
                    [
                        message
                        for message in chat_history
                        if message["role"] == guessing_agent.name
                    ]
                )
                if re.search(
                    r"\b" + re.escape(self.game_variables.topic) + r"\b",
                    last_guessing_agent_response,
                ):
                    print(
                        bcolors.LOG
                        + f"Guessing Agent guessed the secret topic in {number_of_questions} questions!"
                        + bcolors.ENDC
                    )
                    success = True
                    break
                if number_of_questions > 20:
                    print(
                        bcolors.LOG
                        + "Game over, too many questions asked."
                        + bcolors.ENDC
                    )
                    success = False
                    break
            host_agent_response = self.client.run(
                host_agent,
                chat_history=chat_history,
                temperature=self.game_variables.host_agent_temperature,
                json_response=False,
            )
            print(
                bcolors.HOST
                + f"Host Agent: {host_agent_response.messages[-1]['content']}"
                + bcolors.ENDC
            )
            chat_history.extend(host_agent_response.messages)
        except KeyboardInterrupt:
            print(bcolors.LOG + "Stopping game." + bcolors.ENDC)
            success = False
        return GameResult(
            id=self.run_id,
            success=success,
            number_of_questions=number_of_questions,
            chat_history=chat_history,
        )
