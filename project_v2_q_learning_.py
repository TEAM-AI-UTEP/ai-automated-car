#import libraries
import numpy as np
# Bug- Overfeeding - Reduce number of episodes?

## Define Car Stats Class

class CarStats():
  def __init__(self, distance=0,speed=0) -> None:
    self.distance = distance
    self.speed = speed

"""## Define the Environment
"""

################## Read Test File
file_path = input("Enter the path to the maze text file: ")
with open(file_path, 'r') as file:
    maze = []
    for line in file:
        row = [int(x) for x in line.strip().split()]
        maze.append(row)
starting_location = input("Enter x and y coordinates of starting location seperated by one space (Ex: x y):").split()
###################



#define the shape of the environment (i.e., its states)
environment_rows = len(maze)
environment_columns = len(maze[0])

#Create a 3D numpy array to hold the current Q-values for each state and action pair: Q(s, a)

#Automotive Car
q_values = np.zeros((environment_rows, environment_columns, 6))

"""#### Actions
The actions that are available to the AI agent are to move the robot in one of four directions:
* Up
* Right
* Down
* Left

Obviously, the AI agent must learn to avoid driving into the item storage locations (e.g., shelves)!

"""

#define actions
#numeric action codes: 0 = up, 1 = right, 2 = down, 3 = left 4 = slow, 5 = stop, 6 = resume
actions = ['up', 'right', 'down', 'left', 'slow', 'stop','resume']


#Set Rewards

#Our Problem Context - City with four ways and two ways
print('\t\t\tCURRENT MAP\t\t\t')
for row in maze:
    print(" ".join(["{:>5}".format(str(cell)) for cell in row]))

rewards = maze


"""## Train the Model
Our next task is for our AI agent to learn about its environment by implementing a Q-learning model. The learning process will follow these steps:
1. Choose a random, non-terminal state (white square) for the agent to begin this new episode.
2. Choose an action (move *up*, *right*, *down*, or *left*) for the current state. Actions will be chosen using an *epsilon greedy algorithm*. This algorithm will usually choose the most promising action for the AI agent, but it will occasionally choose a less promising option in order to encourage the agent to explore the environment.
3. Perform the chosen action, and transition to the next state (i.e., move to the next location).
4. Receive the reward for moving to the new state, and calculate the temporal difference.
5. Update the Q-value for the previous state and action pair.
6. If the new (current) state is a terminal state, go to #1. Else, go to #2.

This entire process will be repeated across 1000 episodes. This will provide the AI agent sufficient opportunity to learn the shortest paths between the item packaging area and all other locations in the warehouse where the robot is allowed to travel, while simultaneously avoiding crashing into any of the item storage locations!

#### Define Helper Functions
"""

#define a function that determines if the specified location is a terminal state
def is_terminal_state(current_row_index, current_column_index):
  #if the reward for this location is -1, then it is not a terminal state (i.e., it is a 'white square')
  # #changed to list representation
  if rewards[current_row_index][current_column_index] == -1. or rewards[current_row_index][current_column_index] == -5. or rewards[current_row_index][current_column_index] == -10.:
    return False
  else:
    return True

#define a function that will choose a random, non-terminal starting location
def get_starting_location():
  #get a random row and column index
  current_row_index = np.random.randint(environment_rows)
  current_column_index = np.random.randint(environment_columns)
  if rewards[current_row_index ][current_column_index] == -1:
    car_agent.speed = 20
  #continue choosing random row and column indexes until a non-terminal state is identified
  #(i.e., until the chosen state is a 'white square').
  while is_terminal_state(current_row_index, current_column_index):
    current_row_index = np.random.randint(environment_rows)
    current_column_index = np.random.randint(environment_columns)
  return current_row_index, current_column_index

#define an epsilon greedy algorithm that will choose which action to take next (i.e., where to move next)
def get_next_action(current_row_index, current_column_index, epsilon):
  #if a randomly chosen value between 0 and 1 is less than epsilon,
  #then choose the most promising value from the Q-table for this state.
  if np.random.random() < epsilon:
    return np.argmax(q_values[current_row_index, current_column_index])
  else: #choose a random action
    return np.random.randint(6)

#define a function that will get the next location based on the chosen action
def get_next_location(current_row_index, current_column_index, action_index):
  
  new_row_index = current_row_index
  new_column_index = current_column_index
  
  #For any location
  if rewards[current_row_index][current_column_index]:
    if actions[action_index] == 'up' and current_row_index > 0:
      new_row_index -= 1
    elif actions[action_index] == 'right' and current_column_index < environment_columns - 1:
      new_column_index += 1
    elif actions[action_index] == 'down' and current_row_index < environment_rows - 1:
      new_row_index += 1
    elif actions[action_index] == 'left' and current_column_index > 0:
      new_column_index -= 1
  return new_row_index, new_column_index

#define a function that will get the current speed based on the location of the car
def get_speed(current_row_index, current_column_index,action_index):
  if actions[action_index] == 'slow' and rewards[current_row_index][current_column_index] == -5:
    car_agent.speed -= 10
  elif actions[action_index] == 'stop' and rewards[current_row_index][current_column_index] == -10:
    car_agent.speed = 0
  elif actions[action_index] == 'resume' and rewards[current_row_index][current_column_index] == -5:
    car_agent.speed += 10
  return car_agent.speed

#Define a function that will get the shortest path between any location within the warehouse that
#the robot is allowed to travel and the item packaging location.
def get_shortest_path(start_row_index, start_column_index):
  speed_stats = []
  #return immediately if this is an invalid starting location
  if is_terminal_state(start_row_index, start_column_index):
    return []
  else: #if this is a 'legal' starting location
    current_row_index, current_column_index = start_row_index, start_column_index
    shortest_path = []
    shortest_path.append([current_row_index, current_column_index])
    #continue moving along the path until we reach the goal (i.e., the item packaging location)
    while not is_terminal_state(current_row_index, current_column_index):
      #get the best action to take
      action_index = get_next_action(current_row_index, current_column_index, 0.59999)
      current_speed = get_speed(current_row_index, current_column_index,action_index)
      #move to the next location on the path, and add the new location to the list
      current_row_index, current_column_index = get_next_location(current_row_index, current_column_index, action_index)
      speed_stats.append(current_speed)
      shortest_path.append([current_row_index, current_column_index])
      print("Current Location: ",[current_row_index, current_column_index],"Current Action: ",actions[action_index],"Current Speed: ",current_speed)
      # # if len(shortest_path) == 5:
      #   return []
    return shortest_path

"""#### Train the AI Agent using Q-Learning"""

#define training parameters
epsilon = 0.9 #the percentage of time when we should take the best action (instead of a random action)
discount_factor = 0.9 #discount factor for future rewards
learning_rate = 0.7 #the rate at which the AI agent should learn
car_agent = CarStats()

#run through 1000 training episodes
for episode in range(50000):
  #get the starting location for this episode
  row_index, column_index = get_starting_location()

  #continue taking actions (i.e., moving) until we reach a terminal state
  #(i.e., until we reach the item packaging area or crash into an item storage location)
  while not is_terminal_state(row_index, column_index):
    #choose which action to take (i.e., where to move next)
    action_index = get_next_action(row_index, column_index, epsilon)
    # print(actions[action_index])

    #perform the chosen action, and transition to the next state (i.e., move to the next location)
    old_row_index, old_column_index = row_index, column_index #store the old row and column indexes
    row_index, column_index = get_next_location(row_index, column_index, action_index)
    get_speed(old_row_index, old_column_index, action_index)

    #receive the reward for moving to the new state, and calculate the temporal difference
    #changed to list representation
    reward = rewards[row_index][column_index]
    old_q_value = q_values[old_row_index, old_column_index, action_index]
    temporal_difference = reward + (discount_factor * np.max(q_values[row_index, column_index])) - old_q_value

    #update the Q-value for the previous state and action pair
    new_q_value = old_q_value + (learning_rate * temporal_difference)
    q_values[old_row_index, old_column_index, action_index] = new_q_value

print('Training complete!')

"""## Get Shortest Paths
"""
#display a few shortest paths
print(get_shortest_path(int(starting_location[0]), int(starting_location[1])))

"""#### Finally...
It's great that our robot can automatically take the shortest path from any 'legal' location in the warehouse to the item packaging area. **But what about the opposite scenario?**



Run the code cell below to see an example:
"""

#display an example of reversed shortest path
# path = get_shortest_path(5, 2) #go to row 5, column 2
# path.reverse()
# print(path)