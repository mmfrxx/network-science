from os import listdir
from os.path import isfile, join

import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms.community import modularity
from networkx.algorithms.community import label_propagation_communities
from networkx.algorithms.community import performance
from networkx.algorithms.community.louvain import louvain_communities
from networkx.algorithms.community import quality


from networkx.algorithms.community import girvan_newman

mypath = "graphs/"

from sklearn.metrics import normalized_mutual_info_score


def calculate_intersection(graph, partition):

    original = [[0 for j in range(len(graph))] for i in range(len(graph))] 
    algorithm = [[0 for j in range(len(graph))] for i in range(len(graph))] 
    

    for i, community in list(graph.nodes(data='community')):
        community = list(community[1:-1].split(","))
        for node in community:
            original[int(i)][int(node)] = 1
    
    for community in partition:
        community = list(community)
        for i in range(len(community)):
            for j in range(len(community)):
                algorithm[int(community[i])][int(community[j])] = 1
    
    correct = 0
    total = 0

    for i in range(len(graph)):
        for j in range(len(graph)):
            if i <= j:
                if original[i][j] == algorithm[i][j]:
                    correct += 1
                total += 1
    return correct / total
                 
def calculate_nmi(graph, partition):
    original = list(map(lambda x: x[1], list(graph.nodes(data='community'))))
    algorithm = [0] * len(graph)

    for num, community in enumerate(partition):
        for node in community:
            algorithm[int(node)] = num

    return normalized_mutual_info_score(original, algorithm)

for f in listdir(mypath):
    if isfile(join(mypath, f)):
        graph = nx.read_gml(join(mypath, f), destringizer = str)

        greedy_modularity = greedy_modularity_communities(graph)
        
        print("Community intersection for greedy modularity: {}".format(calculate_intersection(graph, greedy_modularity)))
        print("NMI for greedy modularity: {}".format(calculate_nmi(graph, greedy_modularity)))


        label_propagation_g = label_propagation_communities(graph)

        print("Community intersection for label propagation: {}".format(calculate_intersection(graph, label_propagation_g)))
        print("NMI for label propagation: {}".format(calculate_nmi(graph, label_propagation_g)))


        louvain_communities_g = louvain_communities(graph)

        print("Community intersection for louvain: {}".format(calculate_intersection(graph, louvain_communities_g)))
        print("NMI for louvain: {}".format(calculate_nmi(graph, louvain_communities_g)))

        gn = next(girvan_newman(graph))

        print("Community intersection for girvan newman: {}".format(calculate_intersection(graph, gn)))
        print("NMI for girvan newman: {}".format(calculate_nmi(graph, gn)))

        

        print(f)







