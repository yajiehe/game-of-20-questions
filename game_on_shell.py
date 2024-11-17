from utils import bcolors
from openai import OpenAI
from typing import List, Optional
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class OpenAIClient:
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
        )
        self.model = "gpt-4o-2024-05-13"

    def generate(
        self,
        messages: List,
        temperature: Optional[float] = 0.8,
    ) -> str | None:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content


client = OpenAIClient()

system_prompt = """You are playing a game of 20 questions with the user. 
You must only play the game, and not answer or ask any questions outside of the game. 
You start by asking whether the user would like to guess or be asked questions."""


def main():
    start_trigger = "Hello!"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": start_trigger},
    ]
    response = client.generate(messages)
    print(bcolors.AGENT + f"Agent: {response}" + bcolors.ENDC)
    messages.extend([{"role": "assistant", "content": response}])
    try:
        while True:
            print(bcolors.USER + "User:" + bcolors.ENDC, end=" ")
            user_input = input()
            messages.extend(
                [
                    {"role": "user", "content": user_input},
                ]
            )
            response = client.generate(messages)

            messages.extend([{"role": "assistant", "content": response}])

            print(bcolors.AGENT + f"Agent: {response}" + bcolors.ENDC)

    except KeyboardInterrupt:
        print("*** Stopping ***")


if __name__ == "__main__":
    main()
