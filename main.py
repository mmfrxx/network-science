from os import listdir
from os.path import isfile, join
import os
import json
import pickle
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms.community import modularity
from networkx.algorithms.community import label_propagation_communities
from networkx.algorithms.community import performance
from networkx.algorithms.community.louvain import louvain_communities
from networkx.algorithms.community import quality

mypath = os.path.abspath(os.getcwd()) + "/graphs"

from sklearn.metrics import normalized_mutual_info_score

                 
def calculate_nmi(graph, partition):
    original = list(map(lambda x: x[1], list(graph.nodes(data='community'))))
    algorithm = [0] * len(graph)

    for num, community in enumerate(partition):
        for node in community:
            algorithm[int(node)] = num

    return normalized_mutual_info_score(original, algorithm)

def create_result_dict_for_json(node_number, average_degree, mu, algorithm, score):
    return {
        "number": node_number,
        "avg" : average_degree,
        "mu": mu,
        "name": algorithm,
        "nmi": score
    }

# in following lines of code we find communities using three algorithms and calculate their nmi
def do_experiment():
    results = []
    
    for f in listdir(mypath):
        if isfile(join(mypath, f)):
            _, num, average_degree, mu = f[:-4].split("_")

            graph = nx.read_gml(join(mypath, f), destringizer = str)

            greedy_modularity = greedy_modularity_communities(graph)
            greedy_nmi = calculate_nmi(graph, greedy_modularity)
            results.append(create_result_dict_for_json(int(num), int(average_degree), float(mu), "greedy", greedy_nmi))
            with open('./partitions/greedy_{}.partt'.format(f[:-4]), 'wb') as file:
                pickle.dump(greedy_modularity, file)
            
            # with open('greedy.partt', 'rb') as config_dictionary_file:
            #     config_dictionary = pickle.load(config_dictionary_file)
            #     print(config_dictionary == greedy_modularity)

        
            label_propagation_g = label_propagation_communities(graph)
            lp_nmi = calculate_nmi(graph, list(label_propagation_g))
            results.append(create_result_dict_for_json(int(num), int(average_degree), float(mu), "label", lp_nmi))
            with open('./partitions/label_{}.partt'.format(f[:-4]), 'wb') as file:
                pickle.dump(list(label_propagation_g), file)


            louvain_communities_g = louvain_communities(graph)
            l_nmi = calculate_nmi(graph, louvain_communities_g)
            results.append(create_result_dict_for_json(int(num), int(average_degree), float(mu), "louvain", l_nmi))
            with open('./partitions/louvain_{}.partt'.format(f[:-4]), 'wb') as file:
                pickle.dump(louvain_communities_g, file)

    jsonString = json.dumps(results)
    jsonFile = open("results.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

if __name__ == '__main__':
    do_experiment()






