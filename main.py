from os import listdir
from os.path import isfile, join
import os
import json
import pickle
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms.community.louvain import louvain_communities
from networkx.algorithms.community.centrality import girvan_newman

import leidenalg as la
import igraph as ig


mypath = os.path.abspath(os.getcwd()) + "/graphs"

from sklearn.metrics import normalized_mutual_info_score, adjusted_mutual_info_score

                 
def calculate_score(graph, partition):
    original = list(map(lambda x: x[1], list(graph.nodes(data='community'))))
    algorithm = [0] * len(graph)

    for num, community in enumerate(partition):
        for node in community:
            algorithm[int(node)] = num

    return (normalized_mutual_info_score(original, algorithm), adjusted_mutual_info_score(original, algorithm))

def create_result_dict_for_json(node_number, average_degree, mu, algorithm, nmi, ami):
    return {
        "number": node_number,
        "avg" : average_degree,
        "mu": mu,
        "name": algorithm,
        "nmi": nmi,
        "ami": ami
    }

# in following lines of code we find communities using three algorithms and calculate their nmi and ami
def do_experiment():
    results = []

    for idx in range(3):
        for f in listdir(mypath):
            if isfile(join(mypath, f)):
                _, num, average_degree, mu = f[:-4].split("_")

                print("iter {} num {} mu {}".format(idx, num, mu))
                graph = nx.read_gml(join(mypath, f), destringizer = str)
                igraph = ig.Graph.from_networkx(graph)

                greedy_modularity = greedy_modularity_communities(graph)
                greedy_nmi, greedy_ami = calculate_score(graph, greedy_modularity)
                result = create_result_dict_for_json(int(num), int(average_degree), float(mu), "greedy", greedy_nmi, greedy_ami)
                results.append(result)

                louvain_communities_g = louvain_communities(graph)
                l_nmi, l_ami = calculate_score(graph, louvain_communities_g)
                result = create_result_dict_for_json(int(num), int(average_degree), float(mu), "louvain", l_nmi, l_ami)
                results.append(result) 

                partition = la.find_partition(igraph, la.ModularityVertexPartition)
                leiden_part = [[] for i in range(max(partition.membership) + 1)]
                for node, community_idx in enumerate(partition.membership):
                    leiden_part[community_idx].append(node)
                leiden_nmi, leiden_ami = calculate_score(graph, leiden_part)
                result = create_result_dict_for_json(int(num), int(average_degree), float(mu), "leiden", leiden_nmi, leiden_ami)
                results.append(result) 

    jsonString = json.dumps(results)
    jsonFile = open("results.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

if __name__ == '__main__':
    do_experiment()