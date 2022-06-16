import networkx as nx
from networkx.utils import py_random_state
from networkx.generators.community import LFR_benchmark_graph


if __name__ == '__main__':
    # file1 = open('parameters.txt', 'r')
    # lines = file1.readlines()

    # for i, line in enumerate(lines):
    #     n, tau1, average_degree, min_degree, max_degree = list(map(int, line.split(" ")))
    #     tau2 = 1.5
    #     mu = 0.2
    #     min_community = 20
    #     G = LFR_benchmark_graph(
    #         n, tau1, tau2, mu, average_degree=average_degree, 
    #         min_community=min_community, seed=10)
    #     nx.write_gml(G, "graphs/graph_{}_{}_{}_{}_{}.gml".format(
    #         n, tau1, average_degree, min_degree, max_degree), stringizer=str)


    number_of_nodes = [250, 1000, 5000, 10000, 50000]
    mus = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    tau1 = 3
    tau2_small = 1.5
    tau2 = 2
    max_degree = 50
    min_community = 20

    average_degree_250_1 = 4
    average_degree_250_2 = 7

    average_degree_1 = 20
    average_degree_2 = 35

    for mu in mus:
        for i in range(1):
            for num in number_of_nodes:
                print("new")
                if num == 250:
                    print("graph_{}_{}_{}_{}.gml".format(
            num, average_degree_250_1, mu, i))
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
                    nx.write_gml(G, "graphs/graph_{}_{}_{}_{}.gml".format(
            num, average_degree_250_1, mu, i), stringizer=str)

                else:
                    print("graph_{}_{}_{}_{}.gml".format(
            num, average_degree_1, mu, i))
                    G = LFR_benchmark_graph(
                        n = num,
                        tau1 = tau1,
                        tau2 = tau2,
                        mu = mu,
                        average_degree = average_degree_1,
                        max_degree = max_degree,
                        min_community = min_community,
                        seed = i
                    )
                    nx.write_gml(G, "graphs/graph_{}_{}_{}_{}.gml".format(
            num, average_degree_1, mu, i), stringizer=str)
                    
            #         G = LFR_benchmark_graph(
            #             n = num,
            #             tau1 = tau1,
            #             tau2 = tau2,
            #             mu = mu,
            #             average_degree = average_degree_2,
            #             max_degree = max_degree,
            #             min_community = min_community,
            #             seed = i
            #         )
            #         nx.write_gml(G, "graphs/graph_{}_{}_{}_{}.gml".format(
            # num, average_degree_2, mu, i), stringizer=str)







