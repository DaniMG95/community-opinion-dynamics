

def draw_graph(x: list, y: list, title: str, xlabel: str, ylabel: str, path: str) -> None:
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.savefig(path)
    plt.close()

draw_graph(x=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100], y=[40500, 41000, 40833, 41000, 40500, 40916, 41500, 41750, 41777, 41750],
           title='Number steps to convergence vs number of simulations p_inter 0.3 confidence 0.3',
           xlabel='Number of simulations', ylabel='Number steps to convergence',
           path='convergence_confidence_0.3_p_inter_0.3.png')


draw_graph(x=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100], y=[44500, 45000, 46666, 47375, 46700, 46333, 46000, 45935, 46000, 45950],
           title='Number steps to convergence vs number of simulations p_inter 0.9 confidence 0.3',
           xlabel='Number of simulations', ylabel='Number steps to convergence',
           path='convergence_confidence_0.3_p_inter_0.9.png')