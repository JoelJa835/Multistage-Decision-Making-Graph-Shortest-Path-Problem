#!/usr/bin/env python3
import sys

def shortest_path_multistage(levels, node_quantities, transition_costs):
    n = sum(node_quantities) # total number of nodes
    dp = [[sys.maxsize for _ in range(node_quantities[k])] for k in range(levels)] # initialize DP table with large values
    directions = [[0 for j in range(node_quantities[k])] for k in range(levels)] # initialize directions table
    # Set values for last level
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

       
                                                 
    # Find shortest path and optimal directions
    path = [0] * levels
    path[0] = 0
    for k in range(levels-1):
        path[k+1] = directions[k][path[k]]
    total_cost = dp[0][0]
    return (path, total_cost, dp)

# Get user input
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

print("levels:",levels)
print("Nodes:",node_quantities)
print("Costs:",transition_costs)

path, total_cost, dp = shortest_path_multistage(levels, node_quantities, transition_costs)
print("Optimal sequence of directions for each node:", path)
print("Shortest path from origin to final destination:", dp[0][0])
print("Corresponding total transition cost:", total_cost)

    

    