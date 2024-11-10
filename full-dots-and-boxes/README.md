# Full Dots And Boxes

## How to use

If one wants to play with the agent over a GUI on a
website, follow the instructions below.

### GUI

Run the following command, which starts a websocket connection
and initialises our agent.

```bash
./websocket_player.py agent/ 8080
```

Go to the following [webpage](https://people.cs.kuleuven.be/~wannes.meert/dotsandboxes/dotsandboxes.html)
and fill in `ws://127.0.0.1:8080` as the FIRST agent.

### TOURNAMENT

In case, you wish to play a tournament with the agent in order
to test its capabilities, run the following commands.

The agent can be tested against specific baselines such as
`firstopen`, `random` and a naive `mcts`.

```bash
python3 tournament.py 0 baselines/random 1 agent data/<name_file>.csv
```

## Available files

- `example_dotsandboxes.ipynb`: Notebook to illustrate how to play the Dots and Boxes game in OpenSpiel
- `tournament.py`: Code that is used to play the tournament
- `websocket_player.py`: Code to wrap the agent to play interactively using the web-based interface

## Local installation

We make use of the public version of OpenSpiel.
See the [documentation](https://openspiel.readthedocs.io/en/latest/) for installation options.

If you have a local install of the repository, you can test the Dots and Boxes game with:

```bash
python3 python/examples/dotsandboxes_example.py
```

This will run two random players in Dots and Boxes. You can also play yourself on the keyboard by passing flags:

```bash
python3 python/examples/dotsandboxes_example.py \
    --player0=random --player1=human
```

## FAQ

### Installation cannot find tensorflow

Tensorflow is only compatible with Python 3.8--3.11.

On macOS you can use an older version by running these commands before the install script:

```bash
brew install python@3.10  # if using homebrew
virtualenv -p /usr/local/opt/python@3.10/bin/python3 venv
. ./venv/bin/activate
```

### Tensorflow / PyTorch does not work on Apple Silicon

When using macOS on M1/M2 Apple Silicon, you might need to use the custom packages provided by Apple:

- https://developer.apple.com/metal/pytorch/
- https://developer.apple.com/metal/tensorflow-plugin/

### Module absl not found

Install the required packages (in the virtual environment).

```bash
pip install -r requirements.txt
```

### openspiel or pyspiel not found

If you encounter this error, make sure to activate the virtual environment (see above).

If you installed openspiel from source:

First, check if the `pyspiel` module is available in `build/python`. If it's absent compilation failed. Try compiling again.

Second, make sure the modules can be found by Python by setting the `PYTHONPATH` environment variable:

```bash
export PYTHONPATH=.:./build/python:$PYTHONPATH
```

You can also use `pip install -e`.

If you have install openspiel using pip:

Check that openspiel is installed in the virtual environment you are using.

### Cannot import OpenSpiel: incompatible architecture

Check that your Python version is compiled for the same architecture as your compiled C++ code.
You can check this by running `python3 -c "import platform; print(platform.platform())"` and compare the output to running `arch`.

This can occur on M1/M2 Apple computers when you see:
`ImportError: dlopen ... (mach-o file, but is an incompatible architecture (have 'arm64', need 'x86_64')`.
This is resolved by forcing the architecture (and potentially reinstalling some libraries):
`env /usr/bin/arch -arm64  /bin/zsh --login`.

### Compilation fails on 'Return statement with no value'

Most compilers will allow an empty return statement, but some do not.

```bash
open_spiel/open_spiel/higc/referee_test.cc:229:47: error: return-statement with no value, in function returning ‘int’ [-fpermissive]
  229 |   if (absl::GetFlag(FLAGS_run_only_blocking)) return;
```

You can easily fix this by replacing `return;` with `return 0;` in the source code.

### Tests fail with ValueError: setting an array element with a sequence

If you see one of the following two errors:

```bash
ValueError: setting an array element with a sequence. The requested array has an inhomogeneous shape after 2 dimensions. The detected shape was (10, 3) + inhomogeneous part.
ValueError: The history as tensor in the same infoset are different:
```

This is because Numpy became more strict. You can downgrade numpy using `pip install "numpy==1.21.6"` to
eliminiate the errors (but it will most likely have no effect on the correctness of the project).

### Dots and boxes game not registered in games list

Things to check:

- Did you install an old version of OpenSpiel version?
- Check where the files are located that you are using. The example files should be in the same directory
  as the package you are using. If you have multiple installations these can differ based on your path settings.
  After all import statements, add:

```python
import sys
print(sys.path)  # Check which paths are being search for the OpenSpiel package
print(pyspiel)   # Print the location of the used OpenSpiel package
print(__file__)  # Print the location of the current script being executed
```
