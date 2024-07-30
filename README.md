# Tic-Tac-Toe-with-Hand-Detection

This project is a tictactoe game with hand detection.
## Demo Video

<iframe width="560" height="315" src="https://youtu.be/cPGkEDbw9gU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Project Structure

- `hand_detection.py`: Main Script to play Tic-Tac-Toe.
- `cli_game.py`: Tic-Tac-Toe game in the terminal with only keyboard inputs.
- `blue_won.png`, `red_won.png`, `tie.png`: Photos that I use to display the result of the match (can be replaced with any photo of shape 1600, 800).
- `potisions_boxes.py`: Contains a utility function that to get box locations for all the frames.
- `README.md`: This readme file.
- `requirements.txt`: A list of required libraries to use this project.

## Requirements

- Python 3.x
- OpenCV 4.x
- Mediapipe 0.10.x
- Matplotlib 3.x
- other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/just-sabyr/TicTacToe-with-Hand-Detection.git
    cd TicTacToe-with-Hand-Detection
    ```
2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate # on windows, use `.venv\Scripts\activate`
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Running the project

With Hand Detection:
```bash
python hand_detection.py
```
    
Only Command Line game:
```bash
python cli_game.py
```
