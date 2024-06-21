# Visualized Path Finding
	This program takes an image as an input and processes it to solve maze problems with different algorithms.  
	The image MUST have 1 blue circle(start) and 1 red circle(goal).  
	After processing, If the image is accepted you will be able to run the simulation.

## How to run

You can start program by running the command below in root folder  
`python .\visualizedpathfinding\main.py`

## How to use

The in app helper menu will be visible upon launch. Still you can check keymap below if you need.  

  | KEY   | FUNCTION                                   |
  | ----- | ------------------------------------------ |
  | **H** | Toggle helper menu                         |
  | **J** | Import map (opens a file selection dialog) |
  | **K** | Toggle simulation(play/pause)              |
  | **1** | Select BFS as algorithm                    |
  | **2** | Select GBFS as algorithm                   |
  | **3** | Select A* as algorithm                     |

## Requirements
* **Python > 3.10**  (recommended)
* **Python packages needed**
  * numpy==1.26.4
  * opencv-python
  * pygame