# Poker Hand Simulator

The Poker Hand Simulator is a desktop application developed with PyQt5 that allows users to simulate dealing poker hands. It supports running batches of simulations to calculate the probability of various hand ranks, including Royal Flush, Straight Flush, Four of a Kind, and others. The application provides a graphical user interface (GUI) for easy interaction, including options to reset counts, run batch simulations, and view the last hand of each rank.

## Features

- **Run Batch Simulation**: Simulate multiple hands at once to see how often each poker hand rank occurs.
- **View Hand Ranks**: Select a specific hand rank to see the last hand dealt for that category.
- **Reset Counts**: Reset the simulation counts and start over at any time.
- **Card Display**: View the cards of the most recently dealt hand or the last hand of a selected rank.

## Dependencies

This application requires Python and the following Python packages:
- PyQt5
- Pillow (PIL Fork)
- Collections
- Random

## Setup and Installation

To run the Poker Hand Simulator, you need to have Python installed on your system. If you haven't installed Python yet, download and install it from [python.org](https://www.python.org/).

Next, you need to install PyQt5. You can install PyQt5 and Pillow using pip. Run the following command in your terminal:

```
pip install PyQt5 Pillow
```


## Running the Application

Once you have Python and the necessary packages installed, you can run the Poker Hand Simulator by executing the script from the command line:

```
python poker_simulator.py
```


Replace `poker_simulator.py` with the path to the script if you're not in the directory where the script is located.

## How to Use

After starting the application, you can:

1. Select the batch size for simulations from the dropdown.
2. Click **Run Batch Simulation** to simulate the selected number of hands.
3. Use the **Hand Rank** dropdown to select a specific poker hand rank and click **Start Simulation** to simulate until that hand rank is achieved.
4. View the last hand for a specific rank by selecting it in the **View Last Hand for Rank** dropdown and clicking the corresponding button.
5. Reset all counters and hand information by clicking **Reset Counts**.
