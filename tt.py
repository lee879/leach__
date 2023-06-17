
import random
import matplotlib.pyplot as plt
from PIL import Image

class Node:
    def __init__(self, id):
        self.id = id
        self.energy = 100  # 初始能量
        self.cluster_head = False  # 是否是聚簇头节点

class WirelessNetwork:
    def __init__(self, num_nodes, max_rounds):
        self.num_nodes = num_nodes
        self.max_rounds = max_rounds
        self.nodes = []
        self.round = 1

    def setup_nodes(self):
        # 创建节点
        for i in range(self.num_nodes):
            node = Node(i)
            self.nodes.append(node)

    def select_cluster_heads(self):
        # 选择聚簇头节点
        for node in self.nodes:
            if random.random() < 0.1:  # 10%的概率成为聚簇头节点
                node.cluster_head = True

    def run_round(self):
        # 每轮运行
        print(f"Round {self.round}")
        for node in self.nodes:
            if node.cluster_head:
                print(f"Node {node.id} is a cluster head.")
            else:
                cluster_head = self.select_cluster_head(node)
                print(f"Node {node.id} belongs to cluster head {cluster_head.id}")
        self.round += 1

    def select_cluster_head(self, node):
        # 选择所属的聚簇头节点
        cluster_heads = [n for n in self.nodes if n.cluster_head and n.energy > 0]
        if cluster_heads:
            return random.choice(cluster_heads)
        else:
            return None

    def run_simulation(self):
        self.setup_nodes()
        self.select_cluster_heads()
        while self.round <= self.max_rounds:
            self.run_round()
        self.plot_network('before_clustering.png')

        # 清空聚簇头标记，重新运行模拟
        for node in self.nodes:
            node.cluster_head = False
        self.round = 1
        self.select_cluster_heads()
        while self.round <= self.max_rounds:
            self.run_round()
        self.plot_network('after_clustering.png')

    def plot_network(self, filename):
        x = []
        y = []
        colors = []
        for node in self.nodes:
            x.append(node.id)
            y.append(0)
            if node.cluster_head:
                colors.append('red')
            else:
                colors.append('blue')

        plt.scatter(x, y, color=colors)
        plt.xlabel('Node ID')
        plt.ylabel('Cluster Head')
        plt.title('Wireless Network Clustering')
        plt.savefig(filename)
        plt.close()

    def save_as_image(self, filename):
        before_image = Image.open('before_clustering.png')
        after_image = Image.open('after_clustering.png')

        width = max(before_image.width, after_image.width)
        height = before_image.height + after_image.height

        new_image = Image.new('RGB', (width, height))
        new_image.paste(before_image, (0, 0))
        new_image.paste(after_image, (0, before_image.height))

        new_image.save(filename)
        before_image.close()
        after_image.close()
        new_image.close()

# 示例用法
network = WirelessNetwork(num_nodes=20, max_rounds=10)
network.run_simulation()
network.save_as_image('clustering_comparison.png')