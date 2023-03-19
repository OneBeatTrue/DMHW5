import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patch
import scipy as sp


def create(adj_list, order):
    global g_order
    graph = nx.Graph()
    for country in order:
        if (country in adj_list.keys()):
            graph.add_node(country)
            for bordering_country in adj_list[country]:
                graph.add_node(bordering_country)
                graph.add_edge(country, bordering_country)
    return graph

def create_bc(adj_list, order, component):
    global g_order
    graph = nx.Graph()
    for country in order:
        for bordering_country in adj_list[country]:
            if (country in component) and (bordering_country in component):
                graph.add_edge(country, bordering_country)
    return graph

def draw(graph):
    global g_colors, g_coloring, pos
    nx.draw_networkx_nodes(graph, pos, node_size=10, node_shape='o', node_color="#992e00")
    nx.draw_networkx_labels(graph, pos, font_size=5, verticalalignment='bottom', font_family='Georgia')
    nx.draw_networkx_edges(graph, pos, width=0.7, edge_color="#b5b5b5")
    plt.savefig(input() + ".png", dpi=1000)

def draw_v_colored(graph):
    global g_colors_v, g_coloring_v, pos

    nx.draw_networkx_nodes(graph, pos, node_size=10, node_shape='o', node_color=[g_colors_v[i] for i in coloring_v])
    nx.draw_networkx_labels(graph, pos, font_size=5, verticalalignment='bottom', font_family='Georgia')
    nx.draw_networkx_edges(graph, pos, width=0.7, edge_color="#b5b5b5")
    plt.savefig("G_v_colored.png", dpi=1000)

def draw_e_colored(graph):
    global g_colors_e, g_coloring_e, pos

    nx.draw_networkx_nodes(graph, pos, node_size=10, node_shape='o', node_color="#b5b5b5")
    nx.draw_networkx_labels(graph, pos, font_size=5, verticalalignment='bottom', font_family='Georgia')
    nx.draw_networkx_edges(graph, pos, width=0.7, edge_color=[g_colors_e[i] for i in coloring_e])
    plt.savefig("G_e_colored.png", dpi=1000)

def draw_highlighted(graph, adjacency_list, weighted=False):
    global pos, weights, g_order

    nx.draw_networkx_nodes(graph, pos, node_size=10, node_shape='o', node_color="#e6e6e6")
    nx.draw_networkx_labels(graph, pos, font_size=5, verticalalignment='bottom', font_family='Georgia')
    nx.draw_networkx_edges(graph, pos, width=0.7, edge_color="#e6e6e6")

    highlighted = create(adjacency_list, g_order)
    nx.draw_networkx_nodes(highlighted, pos, node_size=10, node_shape='o', node_color="#992e00")
    nx.draw_networkx_labels(highlighted, pos, font_size=5, verticalalignment='bottom', font_family='Georgia') # labels=l
    nx.draw_networkx_edges(highlighted, pos, width=0.7, edge_color="#ed9121")
    if weighted:
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=weights, font_size=3, bbox=dict(facecolor='white', edgecolor='none', pad=0))

    plt.savefig(input() + ".png", dpi=1000)

def draw_blocks(graph, adjacency_list, components):
    global pos, g1_order, g_colors_e

    nx.draw_networkx_nodes(graph, pos, node_size=10, node_shape='o', node_color="#e6e6e6")
    nx.draw_networkx_edges(graph, pos, width=0.7, edge_color="#e6e6e6")

    color = 0;
    for component in components:
        component_graph = create_bc(adjacency_list, g1_order, component)
        nx.draw_networkx_nodes(component_graph, pos, node_size=10, node_shape='o', node_color=g_colors_e[color])
        nx.draw_networkx_edges(component_graph, pos, width=0.7, edge_color=g_colors_e[color])
        color += 1

    nx.draw_networkx_labels(component_graph, pos, font_size=5, verticalalignment='bottom', font_family='Georgia')
    nx.draw_networkx_labels(graph, pos, font_size=5, verticalalignment='bottom', font_family='Georgia')
    plt.savefig(input() + ".png", dpi=1000)

def draw_BCT(adjacency_list, cut_vertice):
    global pos, g1_order, g_colors_BCT

    # nx.draw_networkx_nodes(graph, pos, node_size=10, node_shape='o', node_color="#e6e6e6")
    # nx.draw_networkx_edges(graph, pos, width=0.7, edge_color="#e6e6e6")

    cut_vertice_graph = nx.Graph()

    color = 0;
    for country in g1_order:
        if (country in cut_vertice):
            cut_vertice_graph.add_node(country)
        if (country in adjacency_list.keys()):
            graph = nx.Graph()
            if (len(adjacency_list.keys())):
                graph.add_node(country)
                nx.draw_networkx_nodes(graph, pos, label={}, node_size=10, node_shape='o', node_color=g_colors_BCT[color])
            for bordering_country in adjacency_list[country]:
                graph.add_edge(country, bordering_country)
                nx.draw_networkx_nodes(graph, pos, label={}, node_size=10, node_shape='o', node_color=g_colors_BCT[color])
                nx.draw_networkx_edges(graph, pos, width=0.7, edge_color=g_colors_BCT[color])
            color += 1;


    nx.draw_networkx_nodes(cut_vertice_graph, pos, node_size=10, node_shape='o', node_color="#b5b5b5")
    nx.draw_networkx_labels(cut_vertice_graph, pos, font_size=5, verticalalignment='bottom', font_family='Georgia')
    plt.savefig(input() + ".png", dpi=1000)

def draw_highlighted_vertices(graph, v_list):
    global pos, g_order

    nx.draw_networkx_nodes(graph, pos, node_size=10, node_shape='o', node_color="#e6e6e6")
    nx.draw_networkx_edges(graph, pos, width=0.7, edge_color="#e6e6e6")

    highlighted = nx.Graph()
    for country in g_order:
        if (country in v_list):
            print(country, end=', ')
            highlighted.add_node(country)
    nx.draw_networkx_nodes(highlighted, pos, node_size=10, node_shape='o', node_color="#992e00")
    nx.draw_networkx_labels(highlighted, pos, font_size=5, verticalalignment='bottom', font_family='Georgia') # labels=l

    plt.savefig(input() + ".png", dpi=1000)

def draw_highlighted_edges(graph, e_list):
    global pos, g_order

    nx.draw_networkx_nodes(graph, pos, node_size=10, node_shape='o', node_color="#e6e6e6")
    nx.draw_networkx_edges(graph, pos, width=0.7, edge_color="#e6e6e6")

    highlighted = nx.Graph()
    for e in e_list:
        highlighted.add_edge(e[0], e[1])
    nx.draw_networkx_nodes(highlighted, pos, node_size=10, node_shape='o', node_color="#992e00")
    nx.draw_networkx_edges(highlighted, pos, width=0.7, edge_color="#ed9121")
    nx.draw_networkx_labels(highlighted, pos, font_size=5, verticalalignment='bottom', font_family='Georgia')

    plt.savefig(input() + ".png", dpi=1000)

G_1_adjacency_list = {
    "Armenia": ["Turkey", "Georgia"],
    "Albania": ["Greece", "North Macedonia", "Montenegro", "Kosovo"],
    "Andorra": ["France", "Spain"],
    "Austria": ["Germany", "Czech Republic", "Slovakia", "Hungary", "Slovenia", "Italy", "Switzerland", "Liechtenstein"],
    "Belarus": ["Russia", "Latvia", "Lithuania", "Poland", "Ukraine"],
    "Belgium": ["Netherlands", "Germany", "Luxembourg", "France"],
    "Bosnia and Herzegovina": ["Croatia", "Serbia", "Montenegro"],
    "Bulgaria": ["Romania", "Serbia", "North Macedonia", "Greece", "Turkey"],
    "Croatia": ["Slovenia", "Hungary", "Serbia", "Bosnia and Herzegovina", "Montenegro"],
    "Cyprus": [],
    "Czech Republic": ["Germany", "Poland", "Slovakia", "Austria"],
    "Denmark": ["Germany"],
    "Estonia": ["Russia", "Latvia"],
    "Finland": ["Sweden", "Norway", "Russia"],
    "France": ["Belgium", "Luxembourg", "Germany", "Switzerland", "Italy", "Spain", "Andorra", "Monaco"],
    "Germany": ["Denmark", "Netherlands", "Belgium", "Luxembourg", "France", "Switzerland", "Austria", "Czech Republic", "Poland"],
    "Georgia": ["Russia", "Turkey", "Armenia"],
    "Greece": ["Albania", "North Macedonia", "Bulgaria", "Turkey"],
    "Hungary": ["Austria", "Slovakia", "Ukraine", "Romania", "Serbia", "Croatia", "Slovenia"],
    "Iceland": [],
    "Ireland": ["United Kingdom"],
    "Italy": ["France", "Switzerland", "Austria", "Slovenia", "Vatican City", "San Marino"],
    "Kosovo": ["Albania", "Montenegro", "Serbia", "North Macedonia"],
    "Latvia": ["Estonia", "Russia", "Belarus", "Lithuania"],
    "Liechtenstein": ["Austria", "Switzerland"],
    "Lithuania": ["Latvia", "Belarus", "Poland", "Russia"],
    "Luxembourg": ["Belgium", "Germany", "France"],
    "Malta": [],
    "Moldova": ["Romania", "Ukraine"],
    "Monaco": ["France"],
    "Montenegro": ["Croatia", "Bosnia and Herzegovina", "Serbia", "Kosovo", "Albania"],
    "Netherlands": ["Belgium", "Germany"],
    "North Macedonia": ["Kosovo", "Serbia", "Albania", "Greece", "Bulgaria"],
    "Norway": ["Finland", "Sweden", "Russia"],
    "Poland": ["Germany", "Czech Republic", "Slovakia", "Ukraine", "Belarus", "Lithuania", "Russia"],
    "Portugal": ["Spain"],
    "Romania": ["Hungary", "Ukraine", "Moldova", "Bulgaria", "Serbia"],
    "Russia": ["Norway", "Finland", "Estonia", "Latvia", "Lithuania", "Poland", "Belarus", "Ukraine", "Georgia"],
    "San Marino": ["Italy"],
    "Serbia": ["Hungary", "Romania", "Bulgaria", "North Macedonia", "Montenegro", "Bosnia and Herzegovina", "Croatia", "Kosovo"],
    "Slovakia": ["Poland", "Czech Republic", "Austria", "Hungary", "Ukraine"],
    "Slovenia": ["Austria", "Italy", "Hungary", "Croatia"],
    "Spain": ["France", "Portugal", "Andorra"],
    "Sweden": ["Norway", "Finland"],
    "Switzerland": ["Germany", "Austria", "Liechtenstein", "Italy", "France"],
    "Turkey": ["Greece", "Bulgaria", "Georgia", "Armenia"],
    "Ukraine": ["Belarus", "Russia", "Poland", "Slovakia", "Hungary", "Romania", "Moldova"],
    "United Kingdom": ["Ireland"],
    "Vatican City": ["Italy"]
}
G_adjacency_list = {
    "Armenia": ["Turkey", "Georgia"],
    "Albania": ["Greece", "North Macedonia", "Montenegro", "Kosovo"],
    "Andorra": ["France", "Spain"],
    "Austria": ["Germany", "Czech Republic", "Slovakia", "Hungary", "Slovenia", "Italy", "Switzerland", "Liechtenstein"],
    "Belarus": ["Russia", "Latvia", "Lithuania", "Poland", "Ukraine"],
    "Belgium": ["Netherlands", "Germany", "Luxembourg", "France"],
    "Bosnia and Herzegovina": ["Croatia", "Serbia", "Montenegro"],
    "Bulgaria": ["Romania", "Serbia", "North Macedonia", "Greece", "Turkey"],
    "Croatia": ["Slovenia", "Hungary", "Serbia", "Bosnia and Herzegovina", "Montenegro"],
    "Czech Republic": ["Germany", "Poland", "Slovakia", "Austria"],
    "Denmark": ["Germany"],
    "Estonia": ["Russia", "Latvia"],
    "Finland": ["Sweden", "Norway", "Russia"],
    "France": ["Belgium", "Luxembourg", "Germany", "Switzerland", "Italy", "Spain", "Andorra", "Monaco"],
    "Germany": ["Denmark", "Netherlands", "Belgium", "Luxembourg", "France", "Switzerland", "Austria", "Czech Republic", "Poland"],
    "Georgia": ["Russia", "Turkey", "Armenia"],
    "Greece": ["Albania", "North Macedonia", "Bulgaria", "Turkey"],
    "Hungary": ["Austria", "Slovakia", "Ukraine", "Romania", "Serbia", "Croatia", "Slovenia"],
    "Italy": ["France", "Switzerland", "Austria", "Slovenia", "Vatican City", "San Marino"],
    "Kosovo": ["Albania", "Montenegro", "Serbia", "North Macedonia"],
    "Latvia": ["Estonia", "Russia", "Belarus", "Lithuania"],
    "Liechtenstein": ["Austria", "Switzerland"],
    "Lithuania": ["Latvia", "Belarus", "Poland", "Russia"],
    "Luxembourg": ["Belgium", "Germany", "France"],
    "Moldova": ["Romania", "Ukraine"],
    "Monaco": ["France"],
    "Montenegro": ["Croatia", "Bosnia and Herzegovina", "Serbia", "Kosovo", "Albania"],
    "Netherlands": ["Belgium", "Germany"],
    "North Macedonia": ["Kosovo", "Serbia", "Albania", "Greece", "Bulgaria"],
    "Norway": ["Finland", "Sweden", "Russia"],
    "Poland": ["Germany", "Czech Republic", "Slovakia", "Ukraine", "Belarus", "Lithuania", "Russia"],
    "Portugal": ["Spain"],
    "Romania": ["Hungary", "Ukraine", "Moldova", "Bulgaria", "Serbia"],
    "Russia": ["Norway", "Finland", "Estonia", "Latvia", "Lithuania", "Poland", "Belarus", "Ukraine", "Georgia"],
    "San Marino": ["Italy"],
    "Serbia": ["Hungary", "Romania", "Bulgaria", "North Macedonia", "Montenegro", "Bosnia and Herzegovina", "Croatia", "Kosovo"],
    "Slovakia": ["Poland", "Czech Republic", "Austria", "Hungary", "Ukraine"],
    "Slovenia": ["Austria", "Italy", "Hungary", "Croatia"],
    "Spain": ["France", "Portugal", "Andorra"],
    "Sweden": ["Norway", "Finland"],
    "Switzerland": ["Germany", "Austria", "Liechtenstein", "Italy", "France"],
    "Turkey": ["Greece", "Bulgaria", "Georgia", "Armenia"],
    "Ukraine": ["Belarus", "Russia", "Poland", "Slovakia", "Hungary", "Romania", "Moldova"],
    "Vatican City": ["Italy"]
}

g1_order = [
    "Armenia",
    "Albania",
    "Andorra",
    "Austria",
    "Belarus",
    "Belgium",
    "Bosnia and Herzegovina",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Georgia",
    "Germany",
    "Greece",
    "Hungary",
    "Iceland",
    "Ireland",
    "Italy",
    "Kosovo",
    "Latvia",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Moldova",
    "Monaco",
    "Montenegro",
    "Netherlands",
    "North Macedonia",
    "Norway",
    "Poland",
    "Portugal",
    "Romania",
    "Russia",
    "San Marino",
    "Serbia",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
    "Switzerland",
    "Turkey",
    "Ukraine",
    "United Kingdom",
    "Vatican City"
]
g_order = [
    "Armenia",
    "Albania",
    "Andorra",
    "Austria",
    "Belarus",
    "Belgium",
    "Bosnia and Herzegovina",
    "Bulgaria",
    "Croatia",
    "Czech Republic",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Georgia",
    "Germany",
    "Greece",
    "Hungary",
    "Italy",
    "Kosovo",
    "Latvia",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Moldova",
    "Monaco",
    "Montenegro",
    "Netherlands",
    "North Macedonia",
    "Norway",
    "Poland",
    "Portugal",
    "Romania",
    "Russia",
    "San Marino",
    "Serbia",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
    "Switzerland",
    "Turkey",
    "Ukraine",
    "Vatican City"
]


G_1 = create(G_1_adjacency_list, g1_order)
G = create(G_adjacency_list, g_order)

pos = {
    'Armenia': [-0.41683211, 0.66338365],
    'Albania': [0.32057994, 0.7657439],
    'Andorra': [0.36865637, -0.66103056],
    'Austria': [0.18276003, -0.14058737],
    'Belarus': [-0.14591598, 0.16719016],
    'Belgium': [-0.08436126, -0.54270092],
    'Bosnia and Herzegovina': [0.40012074, 0.35522665],
    'Bulgaria': [0.03786798, 0.56177757],
    'Croatia': [0.36003292, 0.22338542],
    'Czech Republic': [-0.04066695, -0.18012241],
    'Denmark': [-0.25268269, -0.23785008],
    'Estonia': [-0.36594335, 0.2364503],
    'Finland': [-0.5747087, 0.40506586],
    'France': [0.17585331, -0.50694188],
    'Germany': [-0.04323467, -0.32871619],
    'Georgia': [-0.38002199, 0.42525609],
    'Greece': [0.03143175, 0.77949336],
    'Hungary': [0.14363314, 0.13193318],
    'Italy': [0.48610727, -0.30489726],
    'Kosovo': [0.30911187, 0.57714857],
    'Latvia': [-0.28904643, 0.12937239],
    'Liechtenstein': [0.31817326, -0.28621317],
    'Lithuania': [-0.21461282, 0.00281096],
    'Luxembourg': [0.02227141, -0.47948382],
    'Moldova': [-0.1621424, 0.34941581],
    'Monaco': [0.0709844, -0.76330357],
    'Montenegro': [0.53501515, 0.50400419],
    'Netherlands': [-0.2647463, -0.4530787],
    'North Macedonia': [0.21084047, 0.64002629],
    'Norway': [-0.47359035, 0.46410898],
    'Poland': [-0.21045397, -0.09526938],
    'Portugal': [0.30352817, -1.],
    'Romania': [0.03221188, 0.3195179],
    'Russia': [-0.49304861, 0.33109633],
    'San Marino': [0.61764943, -0.42901847],
    'Serbia': [0.23831638, 0.3901491],
    'Slovakia': [0.01383155, 0.00049414],
    'Slovenia': [0.34006156, -0.01565818],
    'Spain': [0.24632615, -0.76023827],
    'Sweden': [-0.70929194, 0.57962959],
    'Switzerland': [0.20365287, -0.37723063],
    'Turkey': [-0.19514486, 0.64308268],
    'Ukraine': [-0.03580471, 0.23373648],
    'Vatican City': [0.6632321, -0.28715871],
    'Cyprus': [-0.51045397, -0.09526938],
    'Iceland': [-0.61045397, -0.09526938],
    'Malta': [-0.71045397, -0.09526938],
    'United Kingdom': [-0.3709844, -0.75330357],
    'Ireland': [-0.5709844, -0.65330357],
}
weights = {
    ("Italy", "Vatican City") : 5,
    ("Austria", "Slovakia") : 83,
    ("Kosovo", "North Macedonia") : 94,
    ("Croatia", "Slovenia") : 140,
    ("Albania", "Montenegro") : 150,
    ("Belarus", "Lithuania") : 180,
    ("Hungary", "Slovakia") : 200,
    ("Belgium", "Luxembourg") : 210,
    ("Belgium", "Netherlands") : 210,
    ("Bosnia and Herzegovina", "Montenegro") : 230,
    ("Bulgaria", "North Macedonia") : 230,
    ("Liechtenstein", "Switzerland") : 230,
    ("Albania", "Kosovo") : 250,
    ("Austria", "Hungary") : 250,
    ("Kosovo", "Montenegro") : 250,
    ("Armenia", "Georgia") : 280,
    ("Albania", "North Macedonia") : 290,
    ("Latvia", "Lithuania") : 290,
    ("Bosnia and Herzegovina", "Serbia") : 300,
    ("Belgium", "France") : 310,
    ("Estonia", "Latvia") : 310,
    ("Italy", "San Marino") : 320,
    ("Kosovo", "Serbia") : 320,
    ("Austria", "Czech Republic") : 330,
    ("Czech Republic", "Slovakia") : 330,
    ("Croatia", "Hungary") : 340,
    ("Bulgaria", "Romania") : 360,
    ("Czech Republic", "Germany") : 360,
    ("France", "Luxembourg") : 360,
    ("Hungary", "Serbia") : 380,
    ("Bulgaria", "Serbia") : 400,
    ("Bosnia and Herzegovina", "Croatia") : 420,
    ("Montenegro", "Serbia") : 420,
    ("North Macedonia", "Serbia") : 430,
    ("Austria", "Slovenia") : 440,
    ("Croatia", "Serbia") : 460,
    ("Hungary", "Slovenia") : 460,
    ("Italy", "Slovenia") : 460,
    ("Belarus", "Latvia") : 470,
    ("Moldova", "Ukraine") : 470,
    ("Moldova", "Romania") : 490,
    ("Finland", "Sweden") : 510,
    ("Lithuania", "Poland") : 510,
    ("Norway", "Sweden") : 520,
    ("Belarus", "Poland") : 560,
    ("Belarus", "Ukraine") : 560,
    ("Denmark", "Germany") : 560,
    ("France", "Switzerland") : 570,
    ("Germany", "Poland") : 570,
    ("Romania", "Serbia") : 590,
    ("Andorra", "Spain") : 610,
    ("Portugal", "Spain") : 620,
    # ("Ireland", "United Kingdom") : 630,
    ("Austria", "Liechtenstein") : 660,
    ("Germany", "Netherlands") : 660,
    ("Poland", "Slovakia") : 660,
    ("Greece", "North Macedonia") : 670,
    ("Austria", "Germany") : 680,
    ("Belarus", "Russia") : 720,
    ("Croatia", "Montenegro") : 720,
    ("Albania", "Greece") : 730,
    ("Czech Republic", "Poland") : 740,
    ("Germany", "Luxembourg") : 740,
    ("Belgium", "Germany") : 760,
    ("Bulgaria", "Greece") : 760,
    ("Poland", "Ukraine") : 770,
    ("Hungary", "Romania") : 830,
    ("Austria", "Switzerland") : 840,
    ("Russia", "Ukraine") : 850,
    ("Andorra", "France") : 860,
    ("Italy", "Switzerland") : 910,
    ("Latvia", "Russia") : 920,
    ("Lithuania", "Russia") : 950,
    ("France", "Monaco") : 960,
    ("Germany", "Switzerland") : 960,
    ("Bulgaria", "Turkey") : 1000,
    ("Finland", "Norway") : 1000,
    ("France", "Germany") : 1000,
    ("Romania", "Ukraine") : 1000,
    ("Austria", "Italy") : 1100,
    ("Estonia", "Russia") : 1100,
    ("Finland", "Russia") : 1100,
    ("Hungary", "Ukraine") : 1100,
    ("France", "Spain") : 1300,
    ("Georgia", "Turkey") : 1300,
    ("Poland", "Russia") : 1300,
    ("Slovakia", "Ukraine") : 1300,
    ("Armenia", "Turkey") : 1400,
    ("France", "Italy") : 1400,
    ("Greece", "Turkey") : 1500,
    ("Norway", "Russia") : 2100,
    ("Georgia", "Russia") : 2800
}

coloring_v = [0, 0, 0, 1, 2, 0, 0, 0, 1, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 2, 0, 0, 1, 2, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0]
g_colors_v = {
    0 : "#992e00", # красный
    1 : "#006400", # зеленый
    2 : "#ed9121", # желтый
    3 : "#6666ff"  # синий
}

coloring_e = [3, 5, 3, 6, 7, 1, 5, 6, 2, 0, 3, 1, 8, 5, 4, 6, 4, 1, 3, 8, 6, 5, 6, 7, 2, 4, 0, 2, 3, 4, 5, 0, 2, 7, 5, 6, 1, 4, 1, 7, 8, 3, 8, 3, 2, 8, 4, 1, 3, 0, 6, 7, 6, 4, 7, 5, 0, 3, 2, 1, 0, 3, 4, 7, 2, 8, 1, 3, 4, 0, 2, 8, 2, 0, 7, 2, 1, 1, 0, 3, 1, 4, 7, 6, 7, 0, 1, 2, 5, 5, 4]
g_colors_e = {
    0 : "#992e00",  # красный
    1 : "#006400",  # темно-зеленый
    2 : "#ed9121",  # оранжевый
    3 : "#9400d3",  # фиолетовый
    4 : "#8cb300",  # светло-зеленый
    5 : "#edff21",  # желтый
    6 : "#75c1ff",  # голубой
    7 : "#110ff2",  # синий
    8 : "#ffc0cb"   # розовый
}

bi_edge_con_comps = [
    ["Armenia", "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia",
     "Cyprus", "Czech Republic", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece", "Hungary", "Iceland",
     "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta", "Moldova", "Montenegro",
     "Netherlands", "North Macedonia", "Norway", "Poland", "Romania", "Russia", "Serbia", "Slovakia", "Slovenia", "Spain",
     "Sweden", "Switzerland", "Turkey", "Ukraine"]
]
blocks = [
    ["Portugal", "Spain"],
    ["Andorra", "France", "Spain"],
    ["Italy", "San Marino"],
    ["Italy", "Vatican City"],
    ["France", "Monaco"],
    ["Denmark", "Germany"],
    ["Finland", "Norway", "Russia", "Sweden"],
    ["Armenia", "Albania", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia",
     "Czech Republic", "Estonia", "France", "Georgia", "Germany", "Greece", "Hungary", "Italy", "Kosovo", "Latvia",
     "Liechtenstein", "Lithuania", "Luxembourg", "Moldova", "Montenegro", "Netherlands", "North Macedonia", "Poland",
     "Romania", "Russia", "Serbia", "Slovakia", "Slovenia", "Switzerland", "Turkey", "Ukraine"],
    ["Ireland", "United Kingdom"],
]

MST_adjacency_list = {
        "Armenia" : ["Georgia"],
        "Albania" : ["Kosovo", "Montenegro"],
        "Andorra" : ["France", "Spain"],
        "Austria" : ["Czech Republic", "Liechtenstein", "Slovakia"],
        "Belarus" : ["Lithuania", "Russia", "Ukraine"],
        "Belgium" : ["France", "Luxembourg", "Netherlands"],
        "Bosnia and Herzegovina" : ["Montenegro", "Serbia"],
        "Bulgaria" : ["North Macedonia", "Romania", "Turkey"],
        "Croatia" : ["Hungary", "Slovenia"],
        "Czech Republic" : ["Austria", "Germany"],
        "Denmark" : ["Germany"],
        "Estonia" : ["Latvia"],
        "Finland" : ["Russia", "Sweden"],
        "France" : ["Andorra", "Belgium", "Monaco", "Switzerland"],
        "Georgia" : ["Armenia", "Turkey"],
        "Germany" : ["Czech Republic", "Denmark"],
        "Greece" : ["North Macedonia"],
        "Hungary" : ["Croatia", "Serbia", "Slovakia"],
        "Italy" : ["San Marino", "Slovenia", "Vatican City"],
        "Kosovo" : ["Albania", "North Macedonia"],
        "Latvia" : ["Estonia", "Lithuania"],
        "Liechtenstein" : ["Austria", "Switzerland"],
        "Lithuania" : ["Belarus", "Latvia", "Poland"],
        "Luxembourg" : ["Belgium"],
        "Moldova" : ["Romania", "Ukraine"],
        "Monaco" : ["France"],
        "Montenegro" : ["Albania", "Bosnia and Herzegovina"],
        "Netherlands" : ["Belgium"],
        "North Macedonia" : ["Bulgaria", "Greece", "Kosovo"],
        "Norway" : ["Sweden"],
        "Poland" : ["Lithuania"],
        "Portugal" : ["Spain"],
        "Romania" : ["Bulgaria", "Moldova"],
        "Russia" : ["Belarus", "Finland"],
        "San Marino" : ["Italy"],
        "Serbia" : ["Bosnia and Herzegovina", "Hungary"],
        "Slovakia" : ["Austria", "Hungary"],
        "Slovenia" : ["Croatia", "Italy"],
        "Spain" : ["Andorra", "Portugal"],
        "Sweden" : ["Finland", "Norway"],
        "Switzerland" : ["France", "Liechtenstein"],
        "Turkey" : ["Bulgaria", "Georgia"],
        "Ukraine" : ["Belarus", "Moldova"],
        "Vatican City" : ["Italy"],
}

BCT_adjacency_list = {
        "Andorra" : ["France", "Spain"],
        "Denmark" : ["Germany"],
        # "Germany" : ["Denmark", "Slovakia"],
        # "Italy" : ["San Marino", "Vatican City"],
        # "France" : ["Andorra", "Monaco", "Slovakia"],
        "Monaco" : ["France"],
        "Portugal" : ["Spain"],
        # "Russia" : ["Sweden", "Slovakia"],
        "San Marino" : ["Italy"],
        "Slovakia" : ["Germany", "France", "Russia", "Italy"],
        "Sweden" : ["Russia"],
        "United Kingdom" : [],
        "Vatican City" : ["Italy"],
}
CV = {"Germany", "Italy", "France", "Russia", "Spain"}
g_colors_BCT = {
    0 : "#006400", # темно-зеленый
    1 : "#edff21", # желтый
    2 : "#8cb300", # светло-зеленый
    3 : "#992e00", # красный
    4 : "#ed9121", # оранжевый
    5 : "#110ff2", # синий
    6 : "#75c1ff", # голубой
    7 : "#ffc0cb", # розовый
    8 : "#9400d3", # фиолетовый
}

Edge_covering_adjacency_list = {
    "Armenia": ["Georgia"],
    "Albania": ["Kosovo"],
    "Andorra" : ["Spain"],
    "Austria": ["Slovenia"],
    "Belarus": ["Lithuania"],
    "Belgium" : ["Luxembourg"],
    "Bosnia and Herzegovina": ["Croatia"],
    "Bulgaria": ["North Macedonia"],
    "Croatia": ["Bosnia and Herzegovina"],
    "Czech Republic": ["Slovakia"],
    "Denmark" : ["Germany"],
    "Estonia": ["Latvia"],
    "Finland": ["Sweden"],
    "France": ["Monaco"],
    "Germany" : ["Netherlands"],
    "Georgia": ["Armenia"],
    "Greece": ["Turkey"],
    "Hungary": ["Serbia"],
    "Italy": ["Vatican City", "San Marino"],
    "Kosovo": ["Albania"],
    "Latvia": ["Estonia"],
    "Liechtenstein": ["Switzerland"],
    "Lithuania": ["Belarus"],
    "Luxembourg": ["Belgium"],
    "Moldova": ["Romania"],
    "Monaco" : ["France"],
    "Montenegro": ["Serbia"],
    "Netherlands": ["Germany"],
    "North Macedonia": ["Bulgaria"],
    "Norway": ["Russia"],
    "Poland": ["Ukraine"],
    "Portugal" : ["Spain"],
    "Romania": ["Moldova"],
    "Russia": ["Norway"],
    "San Marino" : ["Italy"],
    "Serbia": ["Hungary", "Montenegro"],
    "Slovakia": ["Czech Republic"],
    "Slovenia": ["Austria"],
    "Spain": ["Portugal", "Andorra"],
    "Sweden": ["Finland"],
    "Switzerland": ["Liechtenstein"],
    "Turkey": ["Greece"],
    "Ukraine": ["Poland"],
    "Vatican City" : ["Italy"]
}

Matching_adjacency_list = {
    "Armenia": ["Georgia"],
    "Albania": ["Kosovo"],
    # "Andorra" : ["Spain"],
    "Austria": ["Slovenia"],
    "Belarus": ["Lithuania"],
    "Belgium" : ["Luxembourg"],
    "Bosnia and Herzegovina": ["Croatia"],
    "Bulgaria": ["North Macedonia"],
    "Croatia": ["Bosnia and Herzegovina"],
    "Czech Republic": ["Slovakia"],
    "Denmark" : ["Germany"],
    "Estonia": ["Latvia"],
    "Finland": ["Sweden"],
    "France": ["Monaco"],
    # "Germany" : ["Netherlands"],
    "Georgia": ["Armenia"],
    "Greece": ["Turkey"],
    "Hungary": ["Serbia"],
    # "Italy": ["Vatican City", "San Marino"],
    "Italy": ["Vatican City"],
    "Kosovo": ["Albania"],
    "Latvia": ["Estonia"],
    "Liechtenstein": ["Switzerland"],
    "Lithuania": ["Belarus"],
    "Luxembourg": ["Belgium"],
    "Moldova": ["Romania"],
    "Monaco" : ["France"],
    # "Montenegro": ["Serbia"],
    # "Netherlands": ["Germany"],
    "North Macedonia": ["Bulgaria"],
    "Norway": ["Russia"],
    "Poland": ["Ukraine"],
    "Portugal" : ["Spain"],
    "Romania": ["Moldova"],
    "Russia": ["Norway"],
    # "San Marino" : ["Italy"],
    # "Serbia": ["Hungary", "Montenegro"],
    "Serbia": ["Hungary"],
    "Slovakia": ["Czech Republic"],
    "Slovenia": ["Austria"],
    # "Spain": ["Portugal", "Andorra"],
    "Spain": ["Portugal"],
    "Sweden": ["Finland"],
    "Switzerland": ["Liechtenstein"],
    "Turkey": ["Greece"],
    "Ukraine": ["Poland"],
    "Vatican City" : ["Italy"]
}

Stable_set = {"Armenia", "Andorra", "Belarus", "Bosnia and Herzegovina", "Czech Republic", "Denmark", "Estonia", "Greece", "Hungary", "Kosovo", "Liechtenstein", "Luxembourg", "Moldova", "Monaco", "Netherlands", "Portugal", "San Marino", "Sweden", "Vatican City"}

Vertex_covering = {"Sweden", "Finland", "Russia", "Georgia", "Turkey", "Greece", "North Macedonia", "Kosovo", "Montenegro", "Croatia", "Serbia", "Romania", "Moldova", "Hungary", "Austria", "Slovakia", "Belarus", "Latvia", "Poland", "Germany", "Switzerland", "Italy", "Belgium", "France", "Spain"}

# draw_highlighted_vertices(G, Vertex_covering)
# draw_highlighted(G, Matching_adjacency_list);
# draw_highlighted_edges(G, ax.min_maximal_matching(G))
# draw_highlighted_vertices(G, Stable_set)
# draw_highlighted(G, Edge_covering_adjacency_list, False);
# draw_blocks(G_1, G_1_adjacency_list, bi_edge_con_comps)
# draw_BCT(BCT_adjacency_list, CV)
# draw_blocks(G_1, G_1_adjacency_list, blocks)
# draw_highlighted(G, MST_adjacency_list, False);
# draw(G)



