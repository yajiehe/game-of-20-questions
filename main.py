from game import Game
from utils import GameVariables

if __name__ == "__main__":
    game_variables = GameVariables(
        topic="pear",
        guessing_agent_temperature=0.8,
        host_agent_temperature=0.8,
        guessing_agent_additional_instructions="""Your goal is to guess what the user is thinking of in fewest questions possible.
        You must only ask questions that are binary yes/no questions to the best of your ability.
        You must only play the game, and not ask any questions outside of the game.""",
        host_agent_additional_instructions="""The secret topic is {topic} and the user is trying to guess it.
        You must answer the user's questions with yes or no truthfully.
        You must not reveal the secret topic {topic} to the user.
        You must only play the game, and not answer or ask any questions outside of the game.""",
    )
    game = Game(game_variables)
    result = game.run()
    print(f"Game ID: {result.id}")
    print(f"Game success: {result.success}")
    print(f"Number of questions: {result.number_of_questions}")
    print(f"Chat history: {result.chat_history}")
