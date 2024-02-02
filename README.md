# Introduction to Artificial Intelligence - Programming Assignment 1

## Detailed installation instructions:

In order to run the code create a Python environment as follows: \
`Python3.10` \
`numpy==1.26.3`

And to run the project:
1. open the [main.py](main.py) script.
2. Update the `data_filepath` parameter with the path to the input txt file.
3. Run the `main` function.

## About the Heuristic function we used:

In order to calculate the heuristic value we did the following steps:
1. We created a list of all the points of interest which were:
   1. The agent current location.
   2. The locations of all the packages waiting to appear on the graph.
   3. The locations of all the packages placed on the graph.
   4. All the delivery locations of the packages picked up by the agent (Not including other agents picked packages).
2. We created a new graph and connected only the points of interest, by edges with weights according to the shortest path
   between each 2 points using dijkstra.
3. We calculated the minimum spanning tree of the new graph.
4. We set the heuristic value as the cost of the minimum spanning tree of the new graph.

## The rationale behind selecting this Heuristic function:

The optimal path for our agent to take is the path that will start from the agent current location and pass through:
1. All the packages in "waiting" status after their time of appearance, and their delivery locations before the due time.
2. All the packages in "placed" status, and their delivery locations before the due time.
3. All the delivery locations of the packages picked by the agent.

Therefore, we add all these locations into our points of interest list, knowing that if we will find the optimal path, 
we will reach the simulator goal.

We notice the following things:
1. Since we know that the number of packages and their due times are finite,
   by using the A Star algorithm, with update of the packages statuses  on each tested state,
   we are guaranteed to find a path without entering an infinity loop.
2. Since on each state, our heuristic value is the cost of the minimum spanning tree, which is the cost of the path
   that goes between all the points of interest without traversing the same edge more than once, we know that our 
   heuristic function is admissible (Since the solution path will have go through all the edges at least once, 
   and sometimes twice in some of the edges).
 
And by combining this information we get that we are guaranteed to find the optimal path to reach our goal.
