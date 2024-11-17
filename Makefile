format:
	poetry run black .

lint:
	poetry run black . --check

test_topics:
	poetry run pytest -s evals/test_game_with_different_topics.py

test_temperatures:
	poetry run pytest -s evals/test_game_with_different_agent_temperatures.py

test_prompts:
	poetry run pytest -s evals/test_game_with_different_prompts.py
