from execute_monte_carlo import ExecuteMonteCarloDW

NODES = 1000
EDGES = 5000
COMMUNITIES = 10
D = 0.01
V_CONVERGENCE = 0.25
NUM_EXECUTES = 1000
SAVE_RESULTS = False
P_INTER_LIST = [0.3, 0.5, 0.7, 0.9]
CONFIDENCE_THRESHOLD_LIST = [0.10, 0.15, 0.20, 0.25, 0.30]


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

