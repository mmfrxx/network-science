import networkx as nx
from networkx.utils import py_random_state
from networkx.generators.community import LFR_benchmark_graph


if __name__ == '__main__':
    number_of_nodes = [250, 500, 1000, 2500, 5000, 10000]
    mus = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    tau1 = 3
    tau2_small = 1.5
    tau2 = 2
    max_degree = 50
    min_community = 22

    average_degree_250_1 = 4
    average_degree_250_2 = 7

    average_degree_1 = 15
    average_degree_2 = 25

    
    for mu in mus:
        for num in number_of_nodes:
            if num == 250:
                G = LFR_benchmark_graph(
                            n = num,
                            tau1 = tau1,
                            tau2 = tau2_small,
                            mu = mu,
                            average_degree = average_degree_250_1,
                            max_degree = max_degree,
                            min_community = min_community,
                            seed = 10
                        )
                nx.write_gml(G, "graphs/graph_{}_{}_{}.gml".format(
                num, average_degree_250_1, mu), stringizer=str)

                G = LFR_benchmark_graph(
                            n = num,
                            tau1 = tau1,
                            tau2 = tau2_small,
                            mu = mu,
                            average_degree = average_degree_250_2,
                            max_degree = max_degree,
                            min_community = min_community,
                            seed = 10
                        )
                nx.write_gml(G, "graphs/graph_{}_{}_{}.gml".format(
                num, average_degree_250_2, mu), stringizer=str)

            else:
                G = LFR_benchmark_graph(
                            n = num,
                            tau1 = tau1,
                            tau2 = tau2,
                            mu = mu,
                            average_degree =  average_degree_1,
                            max_degree = max_degree,
                            min_community = min_community,
                            seed = 10
                        )
                nx.write_gml(G, "graphs/graph_{}_{}_{}.gml".format(
                num, average_degree_1, mu), stringizer=str)

                G = LFR_benchmark_graph(
                            n = num,
                            tau1 = tau1,
                            tau2 = tau2,
                            mu = mu,
                            average_degree =  average_degree_2,
                            max_degree = max_degree,
                            min_community = min_community,
                            seed = 10
                        )
                nx.write_gml(G, "graphs/graph_{}_{}_{}.gml".format(
                num, average_degree_2, mu), stringizer=str)





