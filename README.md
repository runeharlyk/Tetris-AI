# Tetris-AI using DQN

<!-- Insert gif of AI playing -->

<!-- ## TL-DR -->

<!-- Write intro to tetris and the working of DQN -->

## About the project

This project utilizes deep reinforcement learning to master the game of Tetris. The game engine makes use of the NumPy library for efficient numerical computations and the AI agent is implemented using PyTorch. Our project aims to showcase how Deep Q-Networks (DQN) can be applied to classic games, demonstrating both the learning capability of neural networks and the strategic depth of Tetris.

<!-- Describe how to the AI works -->

## Features

**Deep Q-Network Implementation**: Utilizes a DQN for learning optimal play strategies.

**Customizable Hyperparameters**: Allows tweaking learning rate, discount factor, etc.

**Real-time Learning Plotting**: Watch the AI learn and improve over time.

## Heuristics

To efficiently train and run the neural network the game state is reduced to a few heuristics:

* Number of full rows
* Max height of the columns
* Number of bridges (a bridge is an empty cell beneath a full cell in the column above).
* Bumpiness (sum of absolute difference between column height)

## Getting started

### Prerequisites

The project uses Python 3.11.x which can be down from the [official website](https://www.python.org/downloads/release/python-3117/).

### Installation

1. Clone the repo

    ```sh
    git clone https://github.com/runeharlyk/Tetris-AI.git
    cd Tetris-AI
    ```

1. Setup [virtual environment](https://docs.python.org/3/library/venv.html) (Optional)

    ```sh
    python -m venv TetrisEnv
    ```

1. Install the dependencies

    ```sh
    pip install -r requirements.txt
    ```

## Usage

To train a model, run their training script eg.

```sh
python train_DQLAgent.py
```

To test, without modifying, the models run their test script eg.

```sh
python test_DQNAgent.py
```

## Roadmap

- [x] Generate states, without duplicates
- [ ] python decorator for logging function calls
- [x] Number of sims per second printed every second
- [ ] Rolling average
- [ ] Graph for model reward prediction
- [ ] Model weight visualization

See [issues](https://github.com/runeharlyk/Tetris-AI/issues) for more details

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions to the project are welcome! If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Authors

- Clara
- Lucas
- Rune

<!-- ## Acknowledgments -->
