from execute_monte_carlo import ExecuteMonteCarloDW


NODES = 1000
EDGES = 5000
COMMUNITIES = 10
D = 0.001
V_CONVERGENCE = 0.25
NUM_EXECUTES = 20
SAVE_RESULTS = True
P_INTER_LIST = [0.3, 0.5, 0.7, 0.9]
CONFIDENCE_THRESHOLD_LIST = [0.10, 0.15, 0.20, 0.25, 0.30]

for p_inter in P_INTER_LIST:
    for confidence_threshold in CONFIDENCE_THRESHOLD_LIST:
        print("---------------------------------------------")
        print(f"Executing Monte Carlo for p_inter: {p_inter}, confidence_threshold: {confidence_threshold}")
        execute_monte_carlo = ExecuteMonteCarloDW(nodes=NODES, edges=EDGES, communities=COMMUNITIES, p_inter=p_inter,
                                                  d=D, v_convergence=V_CONVERGENCE,
                                                  confidence_threshold=confidence_threshold,
                                                  num_executes=NUM_EXECUTES, save_results=SAVE_RESULTS)

        average_steps = execute_monte_carlo.execute()
        print(f"Average steps to convergence: {average_steps}")