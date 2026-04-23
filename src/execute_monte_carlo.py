from graph_dw import GraphDW
from graph_factory import GraphFactory
import statistics
import os
import shutil

class ExecuteMonteCarloDW:
    PATH_RESULTS = "./results"

    def __init__(self, nodes: int, edges: int, communities: int, p_inter: float, d: float, v_convergence: float,
                 confidence_threshold: float, num_executes: int, save_results: bool = True,
                 partition_average: int = None):
        self.p_inter = p_inter
        self.graph_factory = GraphFactory(nodes, edges, communities, p_inter)
        self.d = d
        self.v_convergence = v_convergence
        self.confidence_threshold = confidence_threshold
        self.num_executes = num_executes
        self.save_results = save_results
        self.path_directory = f"{self.PATH_RESULTS}/p_{self.p_inter}_threshold_{self.confidence_threshold}"
        if partition_average is None:
            self.partition_average = self.num_executes
        else:
            self.partition_average = partition_average



    def execute(self):
        steps_monte_carlo = []
        if os.path.exists(self.path_directory):
            print(f"Directory {self.path_directory} already exists. Results will be overwritten.")
            shutil.rmtree(self.path_directory)
        os.makedirs(self.path_directory)

        for i in range(self.num_executes):
            graph, communities_nodes = self.graph_factory.generate_graph()
            graph_dw = GraphDW(graph=graph, communities=communities_nodes, d=self.d,
                               save_history_opinions=self.save_results)
            steps = graph_dw.apply_dw(v_convergence=self.v_convergence, confidence_threshold=self.confidence_threshold)
            if self.save_results:
                graph_dw.draw_opinions(path=f"{self.path_directory}/opinions_history_{i}_steps_{steps}.png")
            steps_monte_carlo.append(steps)
            results = (f"Execution {i+1}/{self.num_executes} - steps : {steps} - p_inter {self.p_inter} "
                       f"- confidence_threshold {self.confidence_threshold}")
            if len(steps_monte_carlo) > 1:
                results += f" - stdev {statistics.stdev(steps_monte_carlo)}"
            print(results)
            # with open(f"{self.path_directory}/results.txt", "a+") as file:
            #     file.write(results + "\n")

        mean_steps = 0
        for i in range(0, len(steps_monte_carlo), self.partition_average):
            partition = steps_monte_carlo[:i + self.partition_average]
            mean_partition = statistics.mean(partition)
            with open(f"{self.path_directory}/results.txt", "a+") as file:
                file.write(f"Average steps for {i + self.partition_average} simulations: {mean_partition} - "
                           f"stdev {statistics.stdev(partition)}\n")
            mean_steps = mean_partition
        return mean_steps