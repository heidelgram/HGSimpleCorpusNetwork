import matplotlib.pyplot as plt
import networkx as nx
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


def draw_graph(max_count, project_name, g, show_preview):
    """Draw the graph.

    :param max_count: max. weight within the network
    :type max_count: int
    :param project_name: the project's name
    :type project_name: string
    :param g: a NetworkX object
    :type g: object
    :param show_preview: a boolean indicating if a preview should be shown to the user
    :type show_preview: int
    :return: returns nothing, but writes as network visualization as .png
    """
    # NetX
    count_cutoff = float(float(max_count) / 3)  # Needs Testing
    low_cut = round(count_cutoff, 0)
    middle_cut = round(count_cutoff * 2, 0)
    high_cut = round(count_cutoff * 3, 0)

    # nxEdges, 4 degrees of width
    pos = nx.spring_layout(g)  # positions for all nodes

    # nxNodes, Node shape
    ntext = [u for (u, d) in g.nodes(data=True) if d['node_type'] == 'text']
    esearchterms = [u for (u, d) in g.nodes(data=True) if d['node_type'] == 'search_term']

    nx.draw_networkx_nodes(g, pos, nodelist=ntext, node_size=700, node_shape='s', node_color='#808080')
    nx.draw_networkx_nodes(g, pos, nodelist=esearchterms, node_size=700, node_shape='o', node_color='#808080')

    etone = [(u, v) for (u, v, d) in g.edges(data=True) if d['weight'] == 1]  # weight = count
    etlow = [(u, v) for (u, v, d) in g.edges(data=True) if 1 < d['weight'] <= low_cut]
    etmiddle = [(u, v) for (u, v, d) in g.edges(data=True) if low_cut < d['weight'] <= 2]
    eshigh = [(u, v) for (u, v, d) in g.edges(data=True) if middle_cut < d['weight'] <= high_cut]

    nx.draw_networkx_edges(g, pos, edgelist=etone, width=1, arrows=True, edge_color='#FF8247')
    nx.draw_networkx_edges(g, pos, edgelist=etlow, width=2, arrows=True, edge_color='#F45B36')
    nx.draw_networkx_edges(g, pos, edgelist=etmiddle, width=4, arrows=True, edge_color='#E93425')
    nx.draw_networkx_edges(g, pos, edgelist=eshigh, width=6, arrows=True, edge_color='#DB000F')

    # nxLabels
    nx.draw_networkx_labels(g, pos, font_size=15, font_family='sans-serif')

    # nxDrawing
    plt.axis('off')
    if show_preview == 1:
        plt.show()
    plt.savefig('output/' + project_name + '/output.png')  # save as .png
