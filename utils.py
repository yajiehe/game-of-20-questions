from pydantic import BaseModel
from typing import List, Callable, Union, Optional, Any


class Agent(BaseModel):
    name: str = "Agent"
    model: str = "gpt-4o-2024-05-13"
    instructions: Union[str, Callable[[dict[Any, Any]], str]] = (
        "You are a helpful agent."
    )


class Response(BaseModel):
    messages: List = []
    agent: Optional[Agent] = None


class bcolors:
    AGENT = "\033[94m"
    HOST = "\033[93m"
    USER = "\033[92m"
    LOG = "\033[95m"
    ENDC = "\033[0m"


class GameResult(BaseModel):
    id: str
    success: bool
    number_of_questions: Optional[int] = None
    chat_history: List[dict]


class GameVariables(BaseModel):
    topic: str
    guessing_agent_temperature: float = 0.8
    host_agent_temperature: float = 0.8
    host_agent_additional_instructions: str = ""
    guessing_agent_additional_instructions: str = ""
