#import libraries
import numpy as np
import time
## Define Car Stats Class

class CarStats():
  def __init__(self, distance=0,speed=0) -> None:
    self.distance = distance
    self.speed = speed
  
  def reset_speed(self):
    self.speed = 0
  
  def get_speed(self, index):
    if index == -1:
      car_agent.speed = 20
    elif index == -5:
      car_agent.speed = car_agent.speed/2
    elif index == -10:
      car_agent.speed = car_agent.speed/2
    elif index == -2:
      car_agent.speed = 0
    elif index == -11:
      car_agent.speed +=5
    elif index == -15:
      car_agent.speed = car_agent.speed*2


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
reward_choice = input("Enter reward function choice: \n1 for constant reward (aka reward value at index of reward grid)\n 2 for reward function to get to location without stops: ")
###################



#define the shape of the environment (i.e., its states)
environment_rows = len(maze)
environment_columns = len(maze[0])

#Create a 3D numpy array to hold the current Q-values for each state and action pair: Q(s, a)

#Automotive Car
q_values = np.zeros((environment_rows, environment_columns, 4))


#define actions
#numeric action codes: 0 = up, 1 = right, 2 = down, 3 = left 4 = slow, 5 = stop, 6 = resume
actions = ['up', 'right', 'down', 'left']

#Set Rewards

#Our Problem Context - City with four ways and two ways
print('\t\t\tCURRENT MAP\t\t\t')
for row in maze:
    print(" ".join(["{:>5}".format(str(cell)) for cell in row]))

rewards = maze


"""## Train the Model
Our next task is for our AI agent to learn about its environment by implementing a Q-learning model. The learning process will follow these steps:
1. Choose a random, non-terminal state (white square) for the agent to begin this new episode.
2. Choose an action (move *up*, *right*, *down*, or *left*) for the current state. Actions will be chosen using an *epsilon greedy algorithm*. 
This algorithm will usually choose the most promising action for the AI agent, but it will occasionally choose a less promising option in order to encourage the agent to explore the environment.
3. Perform the chosen action, and transition to the next state (i.e., move to the next location).
4. Receive the reward for moving to the new state, and calculate the temporal difference.
5. Update the Q-value for the previous state and action pair.
6. If the new (current) state is a terminal state, go to #1. Else, go to #2.
"""

#define a function that determines if the specified location is a terminal state
def is_terminal_state(current_row_index, current_column_index):
  #if the reward for this location is -1, then it is not a terminal state (i.e., it is a 'white square')
  # #changed to list representation
  if rewards[current_row_index][current_column_index] == -1. or rewards[current_row_index][current_column_index] == -5. or rewards[current_row_index][current_column_index] == -10.:
    return False
  elif rewards[current_row_index][current_column_index] == -2 or rewards[current_row_index][current_column_index] == -15. or rewards[current_row_index][current_column_index] == -11.:
    return False
  else:
    # print('Destination Arrived',current_row_index, current_column_index, rewards[current_row_index][current_column_index])
    return True

#define a function that will choose a random, non-terminal starting location
def get_starting_location():
  #get a random row and column index
  current_row_index = np.random.randint(environment_rows)
  current_column_index = np.random.randint(environment_columns)
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
    return np.random.randint(4)

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

#Define a function that will get the shortest path between any location within the warehouse that
#the robot is allowed to travel and the item packaging location.
def get_shortest_path(start_row_index, start_column_index):
  speed_stats = []
  car_agent.reset_speed()
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
      action_index = get_next_action(current_row_index, current_column_index, 1.)
      car_agent.get_speed(rewards[current_row_index][current_column_index])
      #move to the next location on the path, and add the new location to the list
      current_row_index, current_column_index = get_next_location(current_row_index, current_column_index, action_index)
      speed_stats.append(car_agent.speed)
      shortest_path.append([current_row_index, current_column_index])
      car_agent.distance = car_agent.distance + 60
      print("Current Location: ",[current_row_index, current_column_index],"Current Action: ",actions[action_index],"Current Speed: ",car_agent.speed, "m/s", "Current Distance: ", car_agent.distance, " units")
      # if len(shortest_path) == 10:
      #   return []
    return shortest_path

# function that returns the reward value based on environment
def reward_function(location_reward_index):    
    # Calculate speed
    # Calculate reward
    reward = location_reward_index
        
    # Penalize for each step taken speed slowing or resuming
    lose = 0
    # Adjust reward based on speed
    if location_reward_index == -5:
      lose = 5
    elif location_reward_index == -10:
      lose = 10
    elif location_reward_index == -2:
      lose = 2
    elif location_reward_index == -11:
      lose = 11
    elif location_reward_index == -15:
      lose = 15
    
    
    return reward - lose
"""#### Train the AI Agent using Q-Learning"""

#define training parameters
epsilon = 0.9 #the percentage of time when we should take the best action (instead of a random action)
discount_factor = 0.9 #discount factor for future rewards
learning_rate = 0.9 #the rate at which the AI agent should learn
car_agent = CarStats()
start_time = time.time()
#run through XXX000 training episodes
for episode in range(10000):
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
    
    #receive the reward for moving to the new state, and calculate the temporal difference
    #changed to list representation

    if int(reward_choice) == 1:
       reward = rewards[row_index][column_index]
    if int(reward_choice) == 2:
      reward = reward_function(rewards[row_index][column_index])


    old_q_value = q_values[old_row_index, old_column_index, action_index]
    temporal_difference = reward + (discount_factor * np.max(q_values[row_index, column_index])) - old_q_value

    #update the Q-value for the previous state and action pair
    new_q_value = old_q_value + (learning_rate * temporal_difference)
    q_values[old_row_index, old_column_index, action_index] = new_q_value

print('Training complete!')
end_time = time.time()

total_time = end_time - start_time
print("Time: ", total_time*1000, "ms")

"""## Get Shortest Paths
"""
#display a few shortest path

print(get_shortest_path(int(starting_location[0]), int(starting_location[1])))
