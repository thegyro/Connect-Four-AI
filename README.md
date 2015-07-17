# Connect-Four-AI
Command Line version for an adversarial Connect Four AI written in Python

#AI falls into a trap
![depth 1 trap](https://github.com/thegyro/Connect-Four-AI/blob/master/screenshots/depth1.png)

The above screenshot explains the limitation of a depth 1 minimax agent (credits - Tushar Nagarajan)

![depth 3 trap](https://github.com/thegyro/Connect-Four-AI/blob/master/screenshots/depth3.png)

You can see the depth 3 alpha beta declaring an early failure without prolonging the game. This was because of poor choice of heuristic function (which in this case, just checked for a win or a loss)
