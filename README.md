# AI plays snake game
Neural Network Trained using Genetic Algorithm which acts as the brain for the snake.

The snake looks in the 8 direction for food, body part and the boundary which acts as the 24 input for the Neural Network.

<img src= "/samples/generation5.gif"> <img src= "/samples/generation23.gif">

## Getting Started
### Prerequisites
To install the dependencies, run on terminal :
```
python3 -m pip -r requirements.txt
```

### Project Structure
```
├── Arena.py            # class that helps in setting the boundary and parameters of the arena
├── brain.py            # class that deals with the neural network
├── colors.py           # consists of colors used in the whole project
├── game.py             # lets the saved snakes to run in 
├── samples
│   ├── generation23.gif    
│   └── generation6.gif
├── input.py            # parametes to apply genetic algorithm on your own
├── README.md
├── requirements.txt    # python dependencies required
├── saved
│   └── top_snakes.pickle   # saved list of objects of snake class for each generation
└── snake.py            # class snake that handles all properties of snake
```
## Testing
To test the Genetic Algorithm, alter the parameters inside the ```input.py```, then run the following command specifying the path to save the optimised result as a pickle file (a list is stored, containing the best snake from each generation):
```
python3 Genetic_algo.py --output saved/test.pickle 
```
## Playing 
To run the snakes saved previously, run the following commands specifying the path to the saved file :
```
python3 game.py --input saved/test.pickle
```
## Acknowledgement
- Inspired by the video of Code-Bullet. Link : https://www.youtube.com/watch?v=3bhP7zulFfY
- Game Visual inspired by YuriyGuts. Link : https://github.com/YuriyGuts/snake-ai-reinforcement
