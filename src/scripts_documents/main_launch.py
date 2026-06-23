from community_opinions_dynamics.graph_factory import GraphFactory
from community_opinions_dynamics.graph_dw import GraphDW

NODES = 1000
EDGES = 5000
COMMUNITIES = 10
D = 0.01
V_CONVERGENCE = 0.25
NUM_EXECUTES = 10

for i in range(NUM_EXECUTES):
    steps = []
    graphs = []
    for p_inter in [0.3, 0.9]:
        graph_factory = GraphFactory(NODES, EDGES, COMMUNITIES, p_inter)
        graph, communities_nodes = graph_factory.generate_graph()
        graph_dw = GraphDW(graph=graph, communities=communities_nodes, d=D,
                                    save_history_opinions=False)
        graph_dw_clone = graph_dw.clone()
        graphs.append(graph_dw.clone())


        print("Applying DW with confidence threshold 0.1...")
        steps_0_1 = graph_dw.apply_dw(v_convergence=V_CONVERGENCE, confidence_threshold=0.1)
        print(f"Number of steps to convergence: {steps_0_1}")
        steps.append(steps_0_1)

        print("Applying DW with confidence threshold 0.3...")
        steps_0_3 = graph_dw_clone.apply_dw(v_convergence=V_CONVERGENCE, confidence_threshold=0.3)
        print(f"Number of steps to convergence: {steps_0_3}")
        steps.append(steps_0_3)

        del graph_dw_clone
        del graph_dw

    for graph, p_inter in zip(graphs, [0.3, 0.9]):
        graph_dw_clone_0_1 = graph.clone()
        graph_dw_clone_0_3 = graph.clone()
        max_steps = max(steps)

        graph_dw_clone_0_1.save_history_opinions = True
        graph_dw_clone_0_3.save_history_opinions = True

        graph_dw_clone_0_1.apply_dw_max_steps(v_convergence=V_CONVERGENCE, confidence_threshold=0.1, max_steps=max_steps)
        graph_dw_clone_0_1.draw_opinions(path=f"{i}_opinions_history_p_inter_{p_inter}_threshold_0_1.png",
                                         title=f"ε = 0.1 p={p_inter}")
        graph_dw_clone_0_3.apply_dw_max_steps(v_convergence=V_CONVERGENCE, confidence_threshold=0.3, max_steps=max_steps)
        graph_dw_clone_0_3.draw_opinions(path=f"{i}_opinions_history_p_inter_{p_inter}_threshold_0_3.png",
                                         title=f"ε = 0.3 and p={p_inter}")
        del graph_dw_clone_0_1
        del graph_dw_clone_0_3

