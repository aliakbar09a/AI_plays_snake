# AI plays snake game
Neural Network Trained using Genetic Algorithm which acts as the brain for the snake.

The snake looks in the 8 direction for food, body part and the boundary which acts as the 24 input for the Neural Network.

<img src= "/samples/generation6.gif"> <img src= "/samples/generation23.gif">

## Getting Started
### Requirements
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
