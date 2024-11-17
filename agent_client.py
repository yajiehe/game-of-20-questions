from openai import OpenAI
from typing import List
import os
from dotenv import load_dotenv
from utils import Agent, Response

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class AgentClient:
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
        )

    def run(
        self,
        agent: Agent,
        chat_history: List = [],
        temperature: float = 0.8,
        json_response: bool = False,
    ) -> Response:
        clean_chat_history = [
            (
                {"role": "assistant", "content": message["content"]}
                if message["role"] == agent.name
                else {"role": "user", "content": message["content"]}
            )
            for message in chat_history
        ]
        messages = [
            {"role": "system", "content": agent.instructions}
        ] + clean_chat_history
        if json_response:
            response = self.client.chat.completions.create(
                model=agent.model,
                response_format={"type": "json_object"},
                messages=messages,
                temperature=temperature,
            )
        else:
            response = self.client.chat.completions.create(
                model=agent.model,
                messages=messages,
                temperature=temperature,
            )

        response_utterance = response.choices[0].message.content
        return Response(
            messages=[{"role": agent.name, "content": response_utterance}],
            agent=agent,
        )
