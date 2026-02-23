# Community Opinion Dynamics: DW Model Experimentation

This project explores the **Deffuant-Weisbuch (DW) Model** to analyze how community structures within a social network influence the formation of consensus.

## Research Objective
The core hypothesis of this experiment is that while a strong community structure (high internal interconnection probability) might hinder the speed of social influence, **consensus ultimately depends on the confidence threshold ($\epsilon$)**.  
The community structure acts as a bottleneck that **slows down the convergence time**, but it does not change the final state of opinions—whether the population reaches a total consensus or remains fragmented depends solely on the agents' openness to different ideas.  

## Experimental Setup
The simulation generates synthetic graphs with a clear community structure where most edges are "internal" to specific groups.

### Fixed Parameters
- **Nodes (n)**: 1000
- **Edges (m)**: 5000
- **Number of Communities (c)**: 10
- **Convergence Tolerance** (d): 0.01
- **Convergence Speed (mu)**: 0.25
- **Monte Carlo Simulations**: 30 executions per configuration to ensure statistical significance and measure variability

### Variable Parameters
- **Internal Edge Probability (p_in)**: 0.1, 0.3, 0.5, 0.7, 0.9 (Higher values mean more isolated communities).
- **Confidence Threshold ($\epsilon$)**: 0.1, 0.3, 0.5, 0.7, 0.9 (Higher values mean more open-minded agents).

## Project Structure
Based on the source code organization, the project is divided into specialized modules:
- `src/graph_factory.py`: Handles the generation of graphs with community structures using the parameters $n, m, c,$ and $p$.
- `src/graph_dw.py`: Implements the Deffuant-Weisbuch logic where agents update their opinions if the difference between them is less than $\epsilon$.
- `src/execute_monte_carlo.py`: Manages stochastic repetitions to compute aggregate data like average convergence time and standard deviation.
- `src/main.py`: The entry point that executes the 400+ required simulations.
- `results/`: Directory containing the processed output for each Monte Carlo batch.

## Analysis of Results
The experiment measures two main outputs:
1. **Convergence Time**: The number of iterations until opinions stabilize ($|X(t) - X(t-2|E|)| < d$).
2. **Opinion Clusters**: The number of final groups with distinct opinions. A result of $1$ signifies global consensus.

## Conclusion
- **$\epsilon$ is King**: If the confidence threshold is high (e.g., 0.35), the system always tends toward consensus. If it is low (e.g., 0.10), the population fragments into multiple clusters regardless of the graph shape.  
- **The Delay Effect**: Higher community isolation ($p = 0.9$) significantly increases the number of iterations needed to reach the final state compared to more integrated graphs ($p = 0.3$), confirming that communities delay but do not prevent consensus.