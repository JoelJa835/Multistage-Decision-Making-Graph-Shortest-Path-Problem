#!/usr/bin/env python3
import sys

def stochastic_shortest_path_multistage(levels, node_quantities, transition_costs, p):
    n = sum(node_quantities)
    V = [[float('inf') for _ in range(node_quantities[k])] for k in range(levels)]
    decisions = [[0 for _ in range(node_quantities[k])] for k in range(levels)]

    # Base case: Set the value function at the final stage to 0
    V[levels - 1] = [0] * node_quantities[levels - 1]

    # Dynamic programming iteration
    for i in range(levels - 2, -1, -1):
        for state in range(node_quantities[i]):
            min_cost = float('inf')
            min_decision = -1

            for decision in range(node_quantities[i + 1]):
                num_decisions = node_quantities[i + 1]
                transition_cost = transition_costs[i][state][decision]

                if num_decisions > 1:
                    prob_other_decisions = (1 - p) / (num_decisions - 1)
                    cost = transition_cost + p * V[i + 1][decision]
                    cost += prob_other_decisions * sum(V[i + 1][decision] for d in range(num_decisions) if d != decision)
                else:
                    p=1
                    cost = transition_cost + p * V[i + 1][decision]

                if cost < min_cost:
                    min_cost = cost
                    min_decision = decision

            V[i][state] = min_cost
            decisions[i][state] = min_decision

    # Find the optimal path
    path = [0] * levels
    path[0] = decisions[0][0]

    for i in range(1, levels):
        path[i] = decisions[i - 1][path[i - 1]]

    total_cost = V[0][path[0]] + transition_costs[0][0][path[0]]
    
    # Print the shortest path from the beginning to the end goal with its corresponding cost of transition
    print("\nShortest path:")
    print(" -> ".join([f"({k}, {path[k]})" for k in range(levels)]))
    print(f"Total cost of transition: {total_cost}")

    return path, total_cost, V



def parse_graph_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    p = float(lines[0].strip())
    levels = int(lines[1].strip())
    node_quantities = [int(lines[i].strip()) for i in range(2, levels + 2)]

    transition_costs = []
    index = levels + 2
    for level in range(levels - 1):
        costs = []
        for _ in range(node_quantities[level]):
            line = lines[index].strip()
            costs.append(list(map(int, line.split())))
            index += 1
        transition_costs.append(costs)

    return levels, node_quantities, transition_costs, p


# Get the graph file path from command-line arguments
file_path = sys.argv[1]

# Parse the graph file
levels, node_quantities, transition_costs, p = parse_graph_file(file_path)

# Call the shortest_path_multistage function
path, total_cost, dp = stochastic_shortest_path_multistage(levels, node_quantities, transition_costs, p)

# Print the optimal path
print( path)


