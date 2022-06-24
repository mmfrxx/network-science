import matplotlib.pyplot as plt
import json
import os

mypath = os.path.abspath(os.getcwd()) + "/results.json"

#(mu, name, node_number, avg_degree) 
mus = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
algos = ["greedy", "leiden", "louvain"]

algo_full_names = {
    'greedy': 'greedy modularity optimization',
    'leiden' : 'Leiden algorithm',
    'louvain' : 'Louvain method'
}

colors = {
    ("greedy", "ami"): '#6C3483',
    ("greedy", "nmi"): '#BB8FCE',
    ("leiden", "ami"): '#239B56',
    ("leiden", "nmi"): '#82E0AA',
    ("louvain", "ami"): '#2874A6',
    ("louvain", "nmi"): '#85C1E9',
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

#Reads data from results.json and stores in dictionary with keys (mu, algo, node, deg)
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
            data[(mu, algo, node, deg)] = {'total_nmi' : 0, 'count' : 0, 'total_ami':0}
        data[(mu, algo, node, deg)]['total_nmi'] += result['nmi']
        data[(mu, algo, node, deg)]['total_ami'] += result['ami']
        data[(mu, algo, node, deg)]['count'] += 1
    
    return data


def draw_graphics(data):
    for mu in mus:
        #for sparser graphs
        for algo in algos:
            x = []
            y_nmi = []
            y_ami = []
            for deg, node in sparser:
                if (mu, algo, node, deg) in data:
                    x.append(node)
                    avg_nmi = data[(mu, algo, node, deg)]['total_nmi']  / data[(mu, algo, node, deg)]['count'] 
                    avg_ami = data[(mu, algo, node, deg)]['total_ami']  / data[(mu, algo, node, deg)]['count'] 
                    y_nmi.append(avg_nmi)
                    y_ami.append(avg_ami)

            plt.plot(x, y_nmi, label = algo_full_names[algo] + ", nmi", color = colors[(algo, "nmi")])
            plt.plot(x, y_ami, label = algo_full_names[algo] + ", ami", color = colors[(algo, "ami")])
        plt.xlabel('Number of nodes')
        plt.ylabel('NMI and AMI')
        plt.title('NMI and AMI of algorithms on sparser graphs for mu = {}'.format(mu))
        plt.legend()
        plt.savefig(os.path.abspath(os.getcwd()) + "/graphics/sparse_{}.png".format(mu))

        plt.clf()

        #for denser graphs
        for algo in algos:
            x = []
            y_nmi = []
            y_ami = []
            for deg, node in denser:
                if (mu, algo, node, deg) in data:
                    x.append(node)
                    avg_nmi = data[(mu, algo, node, deg)]['total_nmi']  / data[(mu, algo, node, deg)]['count'] 
                    avg_ami = data[(mu, algo, node, deg)]['total_ami']  / data[(mu, algo, node, deg)]['count'] 
                    y_nmi.append(avg_nmi)
                    y_ami.append(avg_ami)
            plt.plot(x, y_nmi, label = algo_full_names[algo] + ", nmi", color = colors[(algo, "nmi")])
            plt.plot(x, y_ami, label = algo_full_names[algo] + ", ami", color = colors[(algo, "ami")])
        plt.xlabel('Number of nodes')
        plt.ylabel('NMI and AMI')
        plt.title('NMI and AMI of algorithms on denser graphs for mu = {}'.format(mu))
        plt.legend()
        plt.savefig(os.path.abspath(os.getcwd()) + "/graphics/dense{}.png".format(mu))

        plt.clf()



if __name__ == "__main__":
    data = process_data()
    draw_graphics(data)