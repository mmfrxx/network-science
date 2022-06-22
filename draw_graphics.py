import matplotlib.pyplot as plt
import json
import os

mypath = os.path.abspath(os.getcwd()) + "/results.json"

#(mu, name, node_number, avg_degree) 
mus = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
algos = ["greedy", "label", "louvain"]

algo_full_names = {
    'greedy': 'greedy modularity optimization',
    'label' : 'label propagation',
    'louvain' : 'louvain communities'
}

nodes = [250, 500, 1000, 2500, 5000, 10000]
avg_degrees = {
    250 : [4, 7],
    500 : [15, 25],
    1000 : [15, 25],
    2500 : [15, 25],
    5000 : [15, 25],
    10000 : [15, 25]
}

sparser = [
    (4, 250), (15, 500),(15, 1000),(15, 2500),(15, 5000),(15, 10000)
]

denser = [
    (7, 250), (25, 500),(25, 1000),(25, 2500),(25, 5000),(25, 10000)
]

def process_data():
    results_file = open(mypath)
    results = json.load(results_file)

    data = {}

    for result in results:
        mu = result['mu']
        algo = result['name']
        node = result['number']
        deg = result['avg']
        if (mu, algo, node, deg) not in data:
            data[(mu, algo, node, deg)] = {'total' : 0, 'count' : 0}
        data[(mu, algo, node, deg)]['total'] += result['nmi']
        data[(mu, algo, node, deg)]['count'] += 1
    
    return data

def draw_graphics(data):

    for mu in mus:
        for algo in algos:
            x = []
            y = []
            for deg, node in sparser:
                if (mu, algo, node, deg) in data:
                    x.append(node)
                    mean = data[(mu, algo, node, deg)]['total']  / data[(mu, algo, node, deg)]['count'] 
                    y.append(mean)

            plt.plot(x, y, label = algo_full_names[algo])
        plt.xlabel('Number of nodes')
        plt.ylabel('NMI')
        plt.title('NMI of algorithms on sparser graphs for mu = {}'.format(mu))
        plt.legend()
        plt.savefig(os.path.abspath(os.getcwd()) + "/graphics/sparse_{}.png".format(mu))

        plt.clf()

        for algo in algos:
            x = []
            y = []
            for deg, node in denser:
                if (mu, algo, node, deg) in data:
                    x.append(node)
                    mean = data[(mu, algo, node, deg)]['total']  / data[(mu, algo, node, deg)]['count'] 
                    y.append(mean)
            plt.plot(x, y, label = algo_full_names[algo])
        plt.xlabel('Number of nodes')
        plt.ylabel('NMI')
        plt.title('NMI of algorithms on denser graphs for mu = {}'.format(mu))
        plt.legend()
        plt.savefig(os.path.abspath(os.getcwd()) + "/graphics/dense{}.png".format(mu))

        plt.clf()



if __name__ == "__main__":
    data = process_data()
    draw_graphics(data)