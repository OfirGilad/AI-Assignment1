
#from heapq import heappush, heappop,heapify
import csv
import os
from search_manager import SearchManager
import random
import sys
import numpy as np
   
class PuzzleState:
    goal_state = [[0, 1, 2, 3],
                  [4 ,5, 6, 7],
                  [8, 9, 10, 11],
                  [12, 13, 14, 15]]

    def __init__(self, state, parent=None, expansionDelay = 0,expanded_nodes = 0, one_step_error = 0, h=0,manhattan_distance_val=0,linear_conflict_val=0):
        self.state = state
        self.parent = parent
        self.g = sys.maxsize
        self.h = h 
        self.expansion_delay = 0
        #Node's branching factor (number of children)
        self.b = 0
        #The f value of the current node being expanded
        self.f = sys.maxsize
        #Number of expansions between the node's parent's expansion and its own expansion
        self.expansionDelay = expansionDelay
        #Current expansion serial number
        self.expanded_nodes = expanded_nodes
        self.one_step_error = one_step_error
        self.manhattan_distance_val = manhattan_distance_val 
        self.linear_conflict_val = linear_conflict_val
        self.isInOpenList = False
        self.indexInOpenList = -1
        
    def __lt__(self, other):
        return (self.f) < (other.f)

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self.state))

    def get_blank_pos(self):
        for i in range(4):
            for j in range(4):
                if self.state[i][j] == 0:
                    return i, j

    #The parent node's state will not be treated as a successor (branching factor = 1,2,3)
    def generate_successors(self):
       
        successors = []
        row, col = self.get_blank_pos()
        #Notice that for every move, only 1 tile has changed.
        #In terms of sum manhattan distance, 
        #we can simply deduct the previous manhattan distance of the moved tile, 
        #and add its new one back. This reduces naive computation from O(n^2) to O(1)
        if row > 0:
            new_state = [row[:] for row in self.state]
            new_state[row][col], new_state[row - 1][col] = new_state[row - 1][col], new_state[row][col]
            if (self.parent is not None and new_state != self.parent.state) or (self.parent is None):
                goal_row= self.state[row-1][col]  // 4
                new_node = PuzzleState(new_state, self)
                new_node.manhattan_distance_val = self.manhattan_distance_val -  abs(row-1 - goal_row) + abs(row - goal_row)
                if heuristic == 'MD':
                    new_node.h = new_node.manhattan_distance_val
                elif heuristic == 'MD Linear Conflicts':
                    new_node.linear_conflict_val = new_node.linear_conflict() 
                    new_node.h = new_node.linear_conflict_val+new_node.manhattan_distance_val
                successors.append(new_node)
            

        if row < 3:
            new_state = [row[:] for row in self.state]
            new_state[row][col], new_state[row + 1][col] = new_state[row + 1][col], new_state[row][col]
            if (self.parent is not None and new_state != self.parent.state) or (self.parent is None):
                goal_row = self.state[row+1][col]  // 4
                new_node = PuzzleState(new_state, self)
                new_node.manhattan_distance_val = self.manhattan_distance_val - abs(row+1 - goal_row) + abs(row - goal_row)
                if heuristic == 'MD':
                    new_node.h = new_node.manhattan_distance_val
                elif heuristic == 'MD Linear Conflicts':
                    new_node.linear_conflict_val = new_node.linear_conflict() 
                    new_node.h = new_node.linear_conflict_val+new_node.manhattan_distance_val
                successors.append(new_node)

        if col > 0:
            new_state = [row[:] for row in self.state]
            new_state[row][col], new_state[row][col - 1] = new_state[row][col - 1], new_state[row][col]
            if (self.parent is not None and new_state != self.parent.state) or (self.parent is None):
                goal_col =   self.state[row][col-1] % 4
                new_node = PuzzleState(new_state, self)
                new_node.manhattan_distance_val = self.manhattan_distance_val -  abs(col-1 - goal_col) + abs(col - goal_col)
                if heuristic == 'MD':
                    new_node.h = new_node.manhattan_distance_val
                elif heuristic == 'MD Linear Conflicts':
                    new_node.linear_conflict_val = new_node.linear_conflict() 
                    new_node.h = new_node.linear_conflict_val+new_node.manhattan_distance_val
                successors.append(new_node)

        if col < 3:
            new_state = [row[:] for row in self.state]
            new_state[row][col], new_state[row][col + 1] = new_state[row][col + 1], new_state[row][col]
            if (self.parent is not None and new_state != self.parent.state) or (self.parent is None):
                goal_col =  self.state[row][col+1] % 4
                new_node = PuzzleState(new_state, self)
                new_node.manhattan_distance_val = self.manhattan_distance_val - abs(col+1 - goal_col) + abs(col - goal_col)
                if heuristic == 'MD':
                    new_node.h = new_node.manhattan_distance_val
                elif heuristic == 'MD Linear Conflicts':
                    new_node.linear_conflict_val = new_node.linear_conflict() 
                    new_node.h = new_node.linear_conflict_val+new_node.manhattan_distance_val
                successors.append(new_node)
                
        best_successor_h_value = min([successor.h for successor in successors]) 
        return successors , best_successor_h_value

    def manhattan_distance(self):
        distance = 0
        for i in range(4):
            for j in range(4):
                if self.state[i][j] != 0:
                    row = self.state[i][j] // 4
                    col = self.state[i][j] % 4
                    distance += abs(i - row) + abs(j - col)
        return distance
    
    
    
    def linear_conflict(self):
        conflict_count = 0
        for i in range(4):
            for j in range(4):
                value = self.state[i][j]
                #If the current tile is not empty and is not in its goal position
                if value != 0:
                    goal_row = value  // 4
                    goal_col = value  % 4
                    #If the tile's goal is in the same row
                    if i == goal_row:
                        #Current tile = tj
                        #If tk!=0 ,Row(tj)==Row(tk),Col(tj) < Col(tk), GoalRow(tj)==GoalRow(tk) and Val(tj)>Val(tk) ===> Linear Conflict
                            #if tk is not empty, 
                        for k in range(j + 1, 4):
                            test_value = self.state[i][k]
                            if test_value != 0 and test_value // 4 == goal_row and  test_value<value:
                                conflict_count += 1
                    #If the tile's goal is in the same column                
                    if j == goal_col:
                        for k in range(i + 1, 4):
                            test_value = self.state[k][j]
                            if  test_value != 0 and test_value % 4 == goal_col and test_value<value:
                                conflict_count += 1

        return 2 * conflict_count

    

    def total_heuristic(self):
        self.manhattan_distance_val = self.manhattan_distance()
        if heuristic == 'MD':
            return self.manhattan_distance_val
        elif heuristic == 'MD Linear Conflicts':
            self.linear_conflict_val = self.linear_conflict()
            return self.linear_conflict_val + self.manhattan_distance_val
        else:
            raise ValueError(f'Unknown Heuristic: {heuristic}')
        
    
        

    def is_goal_state(self):
        return self.state == self.goal_state

    def print_solution(self):
        if self.parent:
            self.parent.print_solution()
        print(self.move)
####################### End of PuzzleState Class ###################

def aStar(initial_state,weight):
    
    #At the end of the search, res will contain the statistics of each node expansions
    res = [['N','parent','g','h','f','b','hmin','fmax','expansion delay','average expansion delay','velocity','average velocity','h0','one step error','average one step error','state']]
    initial_state.h = initial_state.total_heuristic()
    initial_state.f = weight*initial_state.h
    fmax = initial_state.f
    h0 = initial_state.h
    hmin = h0
    initial_state.g = 0
    
    expanded_nodes = 0
    velocity = 0 
    average_velocity = 0
    average_expansion_delay = 0
    average_one_step_error = 0
    
    print('Initial h = ',h0,flush=True)
    aStarSearchManager = SearchManager(initial_state)
    while aStarSearchManager.numOfNodesInOpenList>0:
        current_state = aStarSearchManager.GetCurrentState()
        #Node with the lowest f in the open list, remove and expand it. 
        expanded_nodes += 1
        if(expanded_nodes%10000 == 0):
            print(f'{expanded_nodes}th expansion : g value = ',current_state.g,'\th value = ',current_state.h,'\thmin = ',hmin,'\tf value = ',current_state.f,'\tfmax = ',fmax,flush=True)
        current_state.expanded_nodes = expanded_nodes
        #To calculate expansion delay + hueristic reduction, we must to have at least 2 nodes
        if expanded_nodes >1:
          current_state.expansionDelay = current_state.expanded_nodes - current_state.parent.expanded_nodes 
          parent_id = current_state.parent.expanded_nodes
        else:
          parent_id = 0
         
        successors , best_successor_h_value = current_state.generate_successors()
        #Calculating branching factor
        current_state.b = len(successors)    
        current_state.one_step_error =  best_successor_h_value + 1 - current_state.h

        average_expansion_delay = ( (expanded_nodes -1) * average_expansion_delay + current_state.expansionDelay) / expanded_nodes
        velocity = (h0 - hmin) / expanded_nodes
        average_velocity = ( (expanded_nodes -1) * average_velocity + velocity) / expanded_nodes 
        average_one_step_error = ( (expanded_nodes -1) * average_one_step_error + current_state.one_step_error) / expanded_nodes 
         
       
        
        #Below are the statistics gathered for the current node.
        statistics = [expanded_nodes,parent_id,current_state.g,current_state.h,current_state.f,current_state.b,hmin,fmax,current_state.expansionDelay,average_expansion_delay,velocity,average_velocity,h0,current_state.one_step_error,average_one_step_error,current_state.state]
        res.append(statistics)
        if current_state.is_goal_state():
          return res
          
        for successor in successors:
            hmin,fmax = aStarSearchManager.SuccessorHandler(current_state,successor,hmin,fmax,weight)
             
    #Open set is empty but goal was never reached                              
    exit(1)

#Generating instances of the Pancake sorting problem.
def generate_data():
    directory = f'/cs_storage/seanmar/Research/Domains/Puzzles/Input'
    file_contents = []
    for filename in os.listdir(directory):
        print(filename)
        inputFileName = os.path.join(directory, filename)
        if os.path.isfile(inputFileName) and '.txt' in inputFileName  :  # Check if the path is a file
            with open(inputFileName, 'r') as f:
                instance = eval(f.read())
                file_contents.append(instance)
    print("Generate inputs")  
    n = 101
    while(n<5001):
        permutation = random.sample(range(0,16,1), 16)
        permutation_matrix = [permutation[i:i+4] for i in range(0, 16, 4)]
        if permutation_matrix not in file_contents:
            file_contents.append(permutation_matrix)
            fileName = f'/cs_storage/seanmar/Research/Domains/Puzzles/Input/{n}.txt'
            with open(fileName, 'w', newline='') as inputFile:
                inputFile.write(str(permutation_matrix))
                n = n +1 
        else: 
            print('already exists',str(permutation_matrix))
 
    # directory = f'/cs_storage/seanmar/Research/Domains/Puzzles/Input'
    # file_contents = []
    # for filename in os.listdir(directory):
    #     inputFileName = os.path.join(directory, filename)
    #     if os.path.isfile(inputFileName) and '.txt' in inputFileName  :  # Check if the path is a file
    #         with open(inputFileName, 'r') as f:
    #             instance = eval(f.read())
    #             file_contents.append(instance)
    # print(file_contents)
    # d = dict()
    # for element in file_contents:
    #     if d.get(str(element)) is not None:
    #         print("Duplicate!!!")
    #         exit(0)
    #     else:
    #         d[str(element)] = file_contents.index(element)
    # print('ALLLL GOOOOD')            


def create_csv_from_result(file_path,result):
    with open(file_path, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for line in result:
            writer.writerow(line)
            


#print('Number of arguments:', len(sys.argv), 'arguments.')
#range_min , range_max = int(sys.argv[1]) , int(sys.argv[2])
#print(range_min,range_max)
#generate_data(num_inputs)
#generate_output(range_min,range_max)

if __name__ == "__main__":
    jobid = int(sys.argv[1])
    if sys.argv[2] == '1.5':
       weight = float(sys.argv[2])
    else:
       weight = int(sys.argv[2])
    
    heuristic = (sys.argv[3])
    print("SLURM_ARRAY_TASK_ID: ",jobid,flush=True)
    print("Weight: ",weight,flush=True)
    print("Heurstic: ",heuristic,flush=True)

    input_file_path=f'/cs_storage/seanmar/Research/Domains/Puzzles/Input/{jobid}.txt'
    print(input_file_path,flush=True)
    #output_file_path=f'/cs_storage/seanmar/Research/Domains/Puzzles/Output/MD_Linear_Conflicts_Heuristic/Weight_{weight}/{jobid}.csv'
    output_file_path=f'/cs_storage/seanmar/Research/Domains/Puzzles/Output/{heuristic} Heuristic/Weight_{weight}/{jobid}.csv'
 
    # Check if the path is a file
    with open(input_file_path, 'r') as f:
            instance = eval(f.read())
            print('Instance is: ',instance,flush=True)
            initial_state = PuzzleState(state=instance)
            res = aStar(initial_state,weight) 
            create_csv_from_result(output_file_path,res)     
