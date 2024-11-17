# game-of-20-questions

## Notes during development
### Started with a single agent
I first tried to implement the game with a single agent that could act as either the host or the guessing agent to try out the inherent capabilities of the LLM at this game.
This shell agent would take on the role of the host or the guessing agent based on the user's input.
It had a simple prompt:
```
You are playing a game of 20 questions with the user. 
You must only play the game, and not answer or ask any questions outside of the game.
You start by asking whether the user would like to guess or be asked questions.
```
I found that it was already quite capable of playing the game with a human user without additional instructions of the game.

### Added host and guessing agents
I then added two agents, one that would act as the host and one that would act as the guessing agent.
The prompts were very simple:
- The host agent prompt: "You are playing a game of 20 questions as the host agent. You are thinking of a secret topic {topic} and the user is trying to guess it. You must answer the user's questions with yes or no truthfully. You must not reveal the secret topic {topic} to the user. You must only play the game, and not answer or ask any questions outside of the game."
- The guessing agent prompt: "You are playing a game of 20 questions as the guessing agent. Your goal is to guess what the user is thinking of in fewest questions possible. You must only ask questions that are binary yes/no questions to the best of your ability. You must only play the game, and not ask any questions outside of the game."

I noticed two issues:
1. The host agent prompt need to say "The secret topic is {topic}" rather than "You are thinking of a secret topic {topic}" because I noticed that while the original prompt works for very tangible objects like a car or a chair, it doesn't work as well for broader concepts like "books". In those cases, the host agent would self-define a more specific word under the topic.
(see examples/example_for_vague_host_prompt_when_topic_is_astraunat.png)
2. There needs to be a way to determine the success of the game and finish the game, otherwise the game would go on indefinitely.

### Added success condition
I added a simple evaluation mechanism that would check if the guessing agent's last message contains the secret topic. If it does, the game is successful.
Additionally, if the guessing agent runs out of questions, the game is unsuccessful.

### Added evaluation
Added some simple evaluation scripts to test the game with different topics, agent temperatures, and prompts.

The key feature of the tests are that they run the game multiple times `n_runs` with the same parameters and report the mean of the number of questions asked and the success rate with confidence intervals.

There is scope to test the variables of the game with combinations of different values.

### Future work
- Test the game with more complex prompts. e.g. adding more instructions to the guessing agent to ask more complex questions. Or add more ambiguity in the way the host answers the questions to test the guessing agent's ability to deal with uncertainty.
- Test the game with different agent architectures. e.g. adding another guessing agent that calculate the probability of the secret topic based on the questions asked and inform the question of the guessing agent with the most probable outcome.
- Test the game with different models.
- As the game becomes more complex, the success condition might need to change. e.g. might need to add a judge agent to evaluate the quality/fairness of the game.