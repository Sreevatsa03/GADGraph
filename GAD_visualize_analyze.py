
import networkx as nx
import matplotlib.pyplot as plt

FONT_FAMILY = 'monospace'

class GADVisualizeAnalyze():

    def __init__(self):
        """
        Initialize GADVisualizeAnalyze class
        """

        # create a graph
        self.G = nx.DiGraph()

    def set_graph(self, graph):
        """
        Set graph to instance variable G

        :param graph: graph
        :type graph: networkx.classes.graph.DiGraph
        """

        # set graph
        self.G = graph

    def create_graph(self, edges_list, genes = None, diseases = None):
        """
        Create a graph from a list of edges

        :param edges_list: list of edges
        :type edges_list: list
        :param genes: list of genes
        :type genes: list
        :param diseases: list of diseases
        :type diseases: list
        :return: graph
        :rtype: networkx.classes.graph.DiGraph
        """

        # add nodes with attributes
        if (genes is not None) and (diseases is not None):
            self.G.add_nodes_from(genes, type='gene')
            self.G.add_nodes_from(diseases, type='disease')

        # add edges
        self.G.add_edges_from(edges_list)

    def draw_graph(self, title = None, layout = 'spring', font_size = 8, alpha = 0.3, node_size = 750, edge_color = 'grey', font_family = FONT_FAMILY, arrows = True):
        """
        Draw graph from instance variable G and various parameters

        :param title: title of graph
        :type title: str
        :param layout: layout of graph
        :type layout: str
        :param font_size: font size of labels
        :type font_size: int
        :param alpha: alpha value of nodes
        :type alpha: float
        :param node_size: size of nodes
        :type node_size: int
        :param edge_color: color of edges
        :type edge_color: str
        :param font_family: font family of labels
        :type font_family: str
        :param arrows: show arrows
        :type arrows: bool
        """

        # create figure
        plt.figure(figsize=(10, 8))
        ax = plt.gca()
        mono_font = {'fontname':FONT_FAMILY}

        # set title
        if title is not None:
            ax.set_title(title, **mono_font)

        # color map
        color_map = []
        for node in list(self.G.nodes):
            if self.G.nodes[node]["type"] == "disease":
                color_map.append('green')
            else:
                color_map.append('gray')

        # set positions
        if layout == 'spring':
            pos = nx.spring_layout(self.G, scale=30)
        elif layout == 'circular':
            pos = nx.shell_layout(self.G, scale=30)

        pos_higher = {}
        y_off = 0.1  # offset on the y axis

        for k, v in pos.items():
            
            # check if node is a disease
            if self.G.nodes[k]["type"] == "disease":

                # set y offset
                pos_higher[k] = (v[0], v[1] + y_off)
            else:
                pos_higher[k] = v

        # draw graph
        nx.draw_networkx_nodes(self.G, pos=pos, alpha=alpha, node_size=node_size, node_color=color_map, margins=0.1, ax=ax)
        nx.draw_networkx_edges(self.G, pos=pos, alpha=(alpha + (alpha / 1.25)), edge_color=edge_color, arrows=arrows, 
                               connectionstyle='arc3, rad = 0.075', ax=ax)
        nx.draw_networkx_labels(self.G, pos=pos_higher, alpha=(alpha * 2), font_size=font_size, font_family=font_family, font_weight='bold')

        # show graph
        plt.show()
        plt.close('all')

    def recursive_search(self, node, min_num, seen = None):
        """
        Recursively search for nodes with min_num or greater edges
        
        :param node: geneSymbol or diseaseName
        :type node: str
        :param min_num: int minimum number of edges from node
        :type min_num: int
        :param seen: nodes added to subgraph
        :type seen: set
        :return: nodes in subgraph
        :rtype: set
        """

        # convert to undirected graph
        H = self.G.to_undirected()

        # seen is new set of nodes if not recurred yet
        if seen is None:
            seen = set([node])

        # add all nodes that have min_num or greater edges
        for neighbor in H.neighbors(node):
            if neighbor not in seen:
                if len(list(H.neighbors(neighbor))) > int(min_num):

                    # recurse if node has min_num or greater edges
                    seen.add(neighbor)
                    self.recursive_search(neighbor, min_num, seen)

        # return subgraph nodes
        return seen
    
    def create_subgraph(self, nodes):
        """
        Create subgraph from node with min_num or greater edges
        
        :param nodes: list of nodes
        :type nodes: list
        :return: subgraph
        :rtype: networkx.classes.graph.DiGraph
        """

        # create subgraph
        subgraph = nx.subgraph(self.G, list(nodes))

        # return subgraph
        return subgraph
    
    def get_graph(self):
        """
        Return graph

        :return: graph
        :rtype: networkx.classes.graph.DiGraph
        """

        # return graph
        return self.G
    
    def count_associations_bar(self, node_count_list):
        """
        Create bar chart of given nodes and count of associations

        :param node_count_list: list of tuples of nodes and count of associations
        :type node_count_list: list[tuple]
        """

        # create figure
        plt.figure(figsize=(10, 8))
        ax = plt.gca()

        # set title
        ax.set_title('Number of Associations per Node', fontname=FONT_FAMILY)

        # get nodes and count of associations
        nodes, num_associations = zip(*node_count_list)

        # check if nodes are genes or diseases
        if self.G.nodes[nodes[0]]["type"] == "disease":
            ax.set_xlabel('Diseases', fontname=FONT_FAMILY)
            color = 'darkgreen'
        else:
            ax.set_xlabel('Genes', fontname=FONT_FAMILY)
            color = 'darkgray'

        # set y label
        ax.set_ylabel('Number of Associations', fontname=FONT_FAMILY)

        # set x ticks rotation
        plt.xticks(rotation=30)

        # create bar chart
        plt.bar(nodes, num_associations, color=color, alpha=0.3)

        # show graph
        plt.show()
        plt.close('all')
