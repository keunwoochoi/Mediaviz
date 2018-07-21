import matplotlib.pyplot as plt
from adjustText import adjust_text
import networkx as nx
from .utils import set_node_size, set_node_color, set_node_label, edgecolor_by_source,filter_graph, get_subgraph_pos
from .utils import draw_networkx_nodes_custom

def draw_networkx_graph_customized(G, pos=None, 
                      num_nodes=None,num_labels=None,
                      node_colors=None,color_by=None,colormap=None,
                      size_field=None,min_size=0.1, max_size=100,
                      with_labels = True, label_field = None,
                      filter_Graph=False,filter_by=None,top=None,
                      adjust_labels=True, color_edge_by_source = True,
                      node_opacity = 0.5, edge_opacity=0.01, 
                      font_size=8,
                      filename = "untitled.png",**kwargs):
    
    if num_nodes == None:
        num_nodes = len(G.nodes())
    if with_labels == True and num_labels == None:
        num_labels = len(G.nodes())
    
    if pos == None:
        pos = nx.spring_layout(G)

    if filter_Graph:
        if filter_by == None or top == None:
            raise ValueError("For filtering graph filter_by and number of top nodes for subgraph must be given")
        G = filter_graph(G,filter_by=filter_by,top=top).to_undirected()
        pos = get_subgraph_pos(G,pos)

    if node_colors == None:
        node_colors = set_node_color(G,color_by=color_by,colormap=colormap)
    

    node_sizes = set_node_size(G,size_field= size_field,min_size = 0.1, max_size=200)

   
    if with_labels:
        node_labels = set_node_label(G,label_field = label_field)
        subset_label_nodes = sorted(zip(G.nodes(),node_sizes), key= lambda x:x[1], reverse = True)[0:num_labels]
        subset_labels = {n[0]:node_labels[n[0]] for n in subset_label_nodes}
    
    if color_edge_by_source:
        edge_colors = edgecolor_by_source(G,node_colors)

    # plot the visualization
    
    fig = plt.figure(figsize=(10,10),dpi=100)
    ax = fig.add_subplot(111)

    # Draw the nodes, edges, labels separately 
    
    draw_networkx_nodes_custom(G,pos=pos,node_size=node_sizes,node_color=node_colors,ax=ax,alpha=node_opacity,**kwargs)
    plt.axis("scaled")
    nx.draw_networkx_edges(G,pos=pos,edge_color=edge_colors,alpha=edge_opacity,**kwargs)
    labels = nx.draw_networkx_labels(G,pos=pos,labels=subset_labels, font_size=font_size, **kwargs)

    if adjust_labels:
        # Adjust label overlapping
        x_pos = [v[0] for k,v in pos.items()]
        y_pos = [v[1] for k,v in pos.items()]
        adjust_text(texts = list(labels.values()), 
                    x = x_pos, y = y_pos,
                    arrowprops=dict(arrowstyle='->', color='lightgray'))

    # save the plot
    
    plt.savefig(filename)
    
    # Show the plot
    plt.show()