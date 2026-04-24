from community_opinions_dynamics.execute_monte_carlo import ExecuteMonteCarloDW

NODES = 1000
EDGES = 5000
COMMUNITIES = 10
D = 0.01
V_CONVERGENCE = 0.25
NUM_EXECUTES = 1000
SAVE_RESULTS = False
# P_INTER_LIST = [0.3, 0.5, 0.7, 0.9]
# CONFIDENCE_THRESHOLD_LIST = [0.10, 0.15, 0.20, 0.25, 0.30]

P_INTER_LIST = [0.3, 0.9]
CONFIDENCE_THRESHOLD_LIST = [0.10, 0.30]

import concurrent.futures


def run_simulation(params):
    p_inter, confidence_threshold = params

    print(f"Iniciando: p_inter={p_inter}, threshold={confidence_threshold}")

    executor = ExecuteMonteCarloDW(
        nodes=NODES,
        edges=EDGES,
        communities=COMMUNITIES,
        p_inter=p_inter,
        d=D,
        v_convergence=V_CONVERGENCE,
        confidence_threshold=confidence_threshold,
        num_executes=NUM_EXECUTES,
        save_results=SAVE_RESULTS,
        partition_average=50
    )

    average_steps = executor.execute()
    return (p_inter, confidence_threshold, average_steps)


if __name__ == "__main__":

    tasks = []
    for p_inter in P_INTER_LIST:
        for ct in CONFIDENCE_THRESHOLD_LIST:
            tasks.append((p_inter, ct))

    print(f"Lanzando {len(tasks)} configuraciones en paralelo...")

    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(run_simulation, tasks))

    print("\n--- RESUMEN DE RESULTADOS ---")
    for p, ct, steps in results:
        print(f"p_inter: {p} | Threshold: {ct} | Avg Steps: {steps}")



# for p_inter in P_INTER_LIST:
#     for confidence_threshold in CONFIDENCE_THRESHOLD_LIST:
#         print("---------------------------------------------")
#         print(f"Executing Monte Carlo for p_inter: {p_inter}, confidence_threshold: {confidence_threshold}")
#         execute_monte_carlo = ExecuteMonteCarloDW(nodes=NODES, edges=EDGES, communities=COMMUNITIES, p_inter=p_inter,
#                                                   d=D, v_convergence=V_CONVERGENCE,
#                                                   confidence_threshold=confidence_threshold,
#                                                   num_executes=NUM_EXECUTES, save_results=SAVE_RESULTS)
#
#         average_steps = execute_monte_carlo.execute()
#         print(f"Average steps to convergence: {average_steps}")
#
# from graph_factory import GraphFactory
# from graph_dw import GraphDW
# graph_factory = GraphFactory(nodes=1000, edges=5000, communities=10, p_inter=0.3)
# graph, communities_nodes = graph_factory.generate_graph()
#
# print("Graph generated. Starting Deffuant-Weisbuch model...")
# graph_dw = GraphDW(graph=graph, communities=communities_nodes, d=0.001)
# steps = graph_dw.apply_dw(v_convergence=0.25, confidence_threshold=0.1)
# print(f"Number of steps to convergence: {steps}")
# graph_dw.draw_opinions(path="opinions_history.png")