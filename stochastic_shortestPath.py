#!/usr/bin/env python3
import sys
import random

# Define the function for computing the shortest path in multistage graphs with stochastic transitions
def stochastic_shortest_path_multistage(p, levels, node_quantities, transition_costs):
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
                # Check if there is a valid transition between nodes i and j
                if transition_costs[k][i][j] < sys.maxsize:
                    # Compute the new cost with stochastic transitions
                    new_cost = transition_costs[k][i][j] + dp[k+1][j]
                    # Update the cost and direction if the new cost is smaller
                    if new_cost < dp[k][i]:
                        dp[k][i] = new_cost
                        directions[k][i] = j

    # Find the optimal path and minimum expected cost
    path = [0] * levels
    path[0] = 0
    for k in range(levels-1):
        path[k+1] = directions[k][path[k]]
    minimum_expected_cost = dp[0][0]

    # Print the optimal direction for every node of the graph
    print("Optimal directions:")
    for k in range(levels-1):
        for i in range(node_quantities[k]):
            print(f"From level {k+1} node {i+1} to level {k+2} node {directions[k][i]+1}")

    # Print the shortest path from the beginning to the end goal with its corresponding cost of transition
    print("\nShortest path:")
    print(" -> ".join([f"({k+1}, {path[k]+1})" for k in range(levels)]))
    print(f"Minimum expected cost: {minimum_expected_cost}")

    return (path, minimum_expected_cost, dp)

# Get user input for the probability p, levels, node quantities, and transition costs
p = float(input("Enter the probability p: "))
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
        costs.append([int(c) if c != '100' else sys.maxsize for c in row])
    transition_costs.append(costs)

# Modify the transition costs to account for stochastic transitions
# Modify the transition costs to account for stochastic transitions
for k in range(levels-1):
    for i in range(node_quantities[k]):
        num_transitions = node_quantities[k+1]
        if num_transitions > 1:
            transition_probabilities = [p] + [(1-p) / (num_transitions - 1)] * (num_transitions - 1)
            random.shuffle(transition_probabilities)
            expected_costs = [cost * prob for cost, prob in zip(transition_costs[k][i], transition_probabilities)]
            transition_costs[k][i] = expected_costs
        else:
            transition_costs[k][i][0] = 0  # Only one direction, cost is 0



path, total_cost, dp = stochastic_shortest_path_multistage(p, levels, node_quantities, transition_costs)
