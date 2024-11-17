# game-of-20-questions

## Setup
```shell
poetry install
```

## Development

format:
```shell
make format
```

lint:
```shell
make lint
```
for playing the game with a single agent on the shell:
```shell
python game_on_shell.py
```

for simple feel of the two agents playing the game:
```shell
python main.py
```

for evaluation of the game with different topics:
```shell
make test_topics
```

for evaluation of the game with different guessing agent temperatures:
```shell
make test_temperatures
```

for evaluation of the game with different prompts:
```shell
make test_prompts
```
