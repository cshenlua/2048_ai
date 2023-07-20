# 2048_ai

A re-implemtation of [Yanghun Tay](https://www.github.com/yangshun) and [Emmanuel Goh](https://www.github.com/emman27) 's open-sourced base 2048 python program
that supports AI agents, aiming to achieve scores higher than the average human player.

AI agents implemented :

- Greedy Agent
- Minimax Agent
- Expectimax Agent

Heuristics implemented :

- Corner Priority Heuristic
- Monotonicity Heuristic
- Smoothness Heuristic
- Empty-Space Heuristic

## **AI Agents :**

### - _Greedy Agent_ :

- Modeled a player's intuition of wanting to obtain the highest possible score for each action.

### - _Minimax Agent_ :

- Based on the popular adversarial search algorithm "Minimax", the agent acts as the "Max" player and the randomly generated tiles represent the "Min" player.

### - _Expectimax Search Agent_ :

- Expectimax utilizes a "Max" player and "chance" nodes. The "chance" nodes replace the Min player from the Minimax Search Agent and evaluating the state in a different way.

## **Heuristics :**

### - _Corner Priority Heuristic_ :

- Estimates how close the largest-valued tile is to a corner on the board. Distance is measured using the "Manhattan" distance approach similar to its implementation in A\* search. The goal of the heuristic is to have the largest valued tile in any of the four corners of the board.

### - _Monotonicity Heuristic_ :

- Aims to have all the values on the tiles to be in ascending or descending order going upwards/downwards or right/left. This increases the likelihood of tile merges.

### - _Smoothness Heuristic_ :

- Prioritizes the lowest absolute difference between the values of tiles adjacent to one another.

### - _Empty-Space Heuristic_ :

- Aims to maximize the number of empty tiles after performing an action. The agent is awarded a higher evaluation based on the number of empty tiles in the resulting action. With more empty tiles on the board, the longer the game can be prolonged.

## **Running the program :**

<br>

### **NOTE :** You will need to install the `tkinter` package (Python interface to Tcl/Tk GUI toolkit) prior to running the program. This is achieved with the command :

<br>

```
pip install tk
```

<br>

### **Run :**

```
$ python3 puzzle.py
```

## **Demo screenshots :**

e.g. Expectimax Agent paired with the empty-tile heuristic :
![2048](/assets/2048.png)

![terminal_output](/assets/2048_terminal_output.png)
