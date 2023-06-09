#!/usr/bin/env python3
import sys

# Define the function for computing shortest path in multistage graphs
def shortest_path_multistage(levels, node_quantities, transition_costs):
    # Compute the total number of nodes in the graph
    n = sum(node_quantities)
    # Initialize the DP table with large values
    dp = [[sys.maxsize for _ in range(node_quantities[k])] for k in range(levels)]
    # Initialize the directions table to keep track of optimal directions
    directions = [[0 for j in range(node_quantities[k])] for k in range(levels)]
    # Set the costs of the nodes in the last level to 0
    for j in range(node_quantities[levels-1]):
        dp[levels-1][j] = 0
    # Solve subproblems using dynamic programming
    for k in range(levels-2, -1, -1):
        for i in range(node_quantities[k]):
            for j in range(node_quantities[k+1]): 
                if transition_costs[k][i][j] < sys.maxsize:
                    new_cost = transition_costs[k][i][j] + dp[k+1][j]
                    if new_cost < dp[k][i]:
                        dp[k][i] = new_cost
                        directions[k][i] = j

    # Find the optimal path and cost
    path = [0] * levels
    path[0] = 0
    for k in range(levels-1):
        path[k+1] = directions[k][path[k]]
    total_cost = dp[0][0]
    
     # Print the optimal direction for every node of the graph
    print("Optimal directions:")
    for k in range(levels-1):
        for i in range(node_quantities[k]):
            print(f"From level {k+1} node {i+1} to level {k+2} node {directions[k][i]+1}")

    # Print the shortest path from the beginning to the end goal with its corresponding cost of transition
    print("\nShortest path:")
    print(" -> ".join([f"({k+1}, {path[k]+1})" for k in range(levels)]))
    print(f"Total cost of transition: {total_cost}")
    
    
    
    return (path, total_cost, dp)

# Get user input for levels, node quantities, and transition costs
levels = int(input("Enter the number of levels: "))
node_quantities = []
for k in range(levels):
    n = int(input(f"Enter the number of nodes in level {k+1}: "))
    node_quantities.append(n)
transition_costs = []
for k in range(levels-1):
    costs = []
    for i in range(node_quantities[k]):
        row = input(f"Enter the transition costs from level {k+1} node {i+1} to level {k+2} (separated by spaces): ").split()
        costs.append([int(c) for c in row])
    transition_costs.append(costs)

# Print the input values for verification
# print("levels:",levels)
# print("Nodes:",node_quantities)
# print("Costs:",transition_costs)

# Call the shortest_path_multistage function and print the results
path, total_cost, dp = shortest_path_multistage(levels, node_quantities, transition_costs)

