# Full Dots And Boxes

## Available files

- `example_dotsandboxes.ipynb`: Notebook to illustrate how to play the Dots and Boxes game in OpenSpiel
- `tournament.py`: Code that is used to play the tournament
- `websocket_player.py`: Code to wrap the agent to play interactively using the web-based interface

## How to use

If one wants to play with the agent over a GUI on a
website, follow the instructions below.

### website

Run the following command, which starts a websocket connection
and initialises our agent.

```bash
./websocket_player.py agent/ 8080
```

Go to the following [webpage](https://people.cs.kuleuven.be/~wannes.meert/dotsandboxes/dotsandboxes.html)
and fill in `ws://127.0.0.1:8080` as the FIRST agent.

### tournament

In case, you wish to play a tournament with the agent in order
to test its capabilities, run the following commands.

The agent can be tested against specific baselines such as
`firstopen`, `random` and a naive `mcts`.

```bash
python3 tournament.py 0 baselines/random 1 agent data/<name_file>.csv
```

## Local installation

Make sure you have the necessary libraries installed. 
You can use pip to install them from the requirements.txt file.
You also might want to install it a virtual environment if needed.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Normally, you should be able to play the game. You can test by executing
the following command.

```bash
python agent/dotsandboxes_agent.py
```

## Troubleshooting Installation Issues

### openspiel or pyspiel not found

If you encounter this error, make sure to activate the virtual environment (see above).
Check that openspiel is installed in the virtual environment you are using.


