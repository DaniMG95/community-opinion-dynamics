from execute_monte_carlo import ExecuteMonteCarloDW

NODES = 1000
EDGES = 5000
COMMUNITIES = 10
D = 0.01
V_CONVERGENCE = 0.25
NUM_EXECUTES = 3
SAVE_RESULTS = True
P_INTER_LIST = [0.3]
CONFIDENCE_THRESHOLD_LIST = [0.10, 0.15, 0.20, 0.25, 0.30]



executor = ExecuteMonteCarloDW(
        nodes=NODES,
        edges=EDGES,
        communities=COMMUNITIES,
        p_inter=0.3,
        d=D,
        v_convergence=V_CONVERGENCE,
        confidence_threshold=0.3,
        num_executes=NUM_EXECUTES,
        save_results=SAVE_RESULTS
    )

steps = executor.execute()
print(f"Average steps to convergence: {steps}")


executor = ExecuteMonteCarloDW(
        nodes=NODES,
        edges=EDGES,
        communities=COMMUNITIES,
        p_inter=0.3,
        d=D,
        v_convergence=V_CONVERGENCE,
        confidence_threshold=0.1,
        num_executes=NUM_EXECUTES,
        save_results=SAVE_RESULTS,
    max_steps=steps
    )

steps = executor.execute()
print(f"Average steps to convergence: {steps}")



executor = ExecuteMonteCarloDW(
        nodes=NODES,
        edges=EDGES,
        communities=COMMUNITIES,
        p_inter=0.9,
        d=D,
        v_convergence=V_CONVERGENCE,
        confidence_threshold=0.3,
        num_executes=NUM_EXECUTES,
        save_results=SAVE_RESULTS
    )

steps = executor.execute()
print(f"Average steps to convergence: {steps}")


executor = ExecuteMonteCarloDW(
        nodes=NODES,
        edges=EDGES,
        communities=COMMUNITIES,
        p_inter=0.9,
        d=D,
        v_convergence=V_CONVERGENCE,
        confidence_threshold=0.1,
        num_executes=NUM_EXECUTES,
        save_results=SAVE_RESULTS,
    max_steps=steps
    )

steps = executor.execute()
print(f"Average steps to convergence: {steps}")