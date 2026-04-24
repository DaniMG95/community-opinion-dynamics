
import matplotlib.pyplot as plt
from utils import draw_graph


def create_graph_threshold():

    X = [0.05*x for x in range(1, 21)]

    Y_0_9 = [72645, 787895, 316265, 115240, 98525, 46865, 37830, 34705, 34165, 33240, 32265, 31040, 31280, 30925, 30865,
             30685, 30705, 30290, 30875, 30510]
    Y_0_3 = [96140, 527085, 247930, 74255, 79350, 41885, 36880, 34680, 33990, 33580, 32510, 32300, 32135, 31455, 31475,
             31910, 31105, 31030, 31200, 31220]

    plt.figure(figsize=(8, 6), dpi=150)
    plt.plot(X, Y_0_9, label="Inter. prob.=0.9")
    plt.plot(X, Y_0_3, label="Inter. prob.=0.3")
    plt.title("average steps vs threshold Inter. prob.=0.9")
    plt.xlabel("threshold")
    plt.ylabel("time step")
    plt.legend(loc='lower center', fontsize=8)
    plt.tight_layout()
    plt.grid()
    plt.savefig("prueba.png", bbox_inches='tight', dpi=150)
    plt.close()

X = [i for i in range(50, 1001, 50)]
Y_0_3_0_1 = [750700, 741350, 646133, 634600, 604460, 572000, 583757, 565025, 563277, 586600, 572845, 574341, 568030,
             568307, 567786, 559512, 555770, 549416, 550910, 550850]
Y_0_3_0_3 = [39800, 40850, 40900, 41600, 41640, 41833, 41685, 41737, 41733, 41880, 41881, 41775, 41784, 41721, 41653,
             41662, 41605, 41672, 41684, 41685]
Y_0_9_0_1 = [860500, 821350, 884633, 833375, 838300, 811783, 801114, 792737, 800555, 785000, 772445, 767566, 770500,
             772192, 770493, 780912, 782100, 779144, 774189, 774310]
Y_0_9_0_3 = [45200, 45400, 46200, 46425, 46180, 46250, 46357, 46400, 46666, 46640, 46745, 46783, 46761, 46800, 46920,
             46937, 46900, 47022, 47026, 46945]


draw_graph(x=X, y=Y_0_3_0_1, title="steps vs simulations ε = 0.1 and Inter. prob.=0.3",
           xlabel="simulations", ylabel="average steps", path="steps_vs_simulations_0_1_0_3.png")
draw_graph(x=X, y=Y_0_3_0_3, title="steps vs simulations ε = 0.3 and Inter. prob.=0.3",
           xlabel="simulations", ylabel="average steps", path="steps_vs_simulations_0_3_0_3.png")
draw_graph(x=X, y=Y_0_9_0_1, title="steps vs simulations ε = 0.1 and Inter. prob.=0.9",
           xlabel="simulations", ylabel="average steps", path="steps_vs_simulations_0_1_0_9.png")
draw_graph(x=X, y=Y_0_9_0_3, title="steps vs simulations ε = 0.3 and Inter. prob.=0.9",
           xlabel="simulations", ylabel="average steps", path="steps_vs_simulations_0_3_0_9.png")

create_graph_threshold()



