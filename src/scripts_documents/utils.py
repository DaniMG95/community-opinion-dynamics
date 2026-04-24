

def draw_graph(x: list, y: list, title: str, xlabel: str, ylabel: str, path: str) -> None:
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 6), dpi=150)
    plt.plot(x, y, marker='o')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.savefig(path, bbox_inches='tight', dpi=150)
    plt.close()
