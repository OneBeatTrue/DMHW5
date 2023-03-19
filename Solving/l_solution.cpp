#include "inclusion.h"

void dfs_blocks(int v,
                int parent,
                const std::vector<std::set<int>>& graph,
                std::vector<std::set<int>>& biconnected_components,
                std::vector<int>& in, // in[v] — время входа поиска в глубину в вершину u
                std::vector<int>& up, // up[v] — минимум из времени захода в саму вершину in[v], времени захода в предка (необязательно родителя) in[p] если есть ребро (v, p), а также из всех значений up[с] для каждой вершины с, являющейся наследником v в дереве поиска
                std::vector<bool>& visited, // массив, хранящий информацию о (не) посещении вершины
                std::stack<std::pair<int, int>>& st, // стек для хранения дуг, в порядке обработки
                int& time)
{
    visited[v] = true;
    in[v] = time;
    up[v] = time;
    time++;

    // перебираем всех детей узла
    for (int neighbor : graph[v]) {
        if (neighbor != parent) {
            // neighbor является наследником v в дереве обхода
            if (!visited[neighbor]) {
                st.push({v, neighbor});
                dfs_blocks(neighbor, v, graph, biconnected_components, in, up, visited, st, time);

                up[v] = std::min(up[v], up[neighbor]);

                // условие точки сочленения
                if (up[neighbor] >= in[v]) {
                    std::set<int> component;
                    // записываем все дуги стека, до той, которая привела в данный блок (включительно)
                    while (true) {
                        std::pair<int, int> edge = st.top();
                        st.pop();
                        component.insert(edge.first);
                        component.insert(edge.second);
                        if (edge == std::make_pair(v, neighbor)) {
                            break;
                        }
                    }
                    biconnected_components.push_back(component);
                }
                if (up[neighbor] < up[v]) {
                    up[v] = up[neighbor];
                }
            }
                // neighbor является предком v в дереве обхода
            else if (in[neighbor] < in[v]) {
                st.push({v, neighbor});
                if (in[neighbor] < up[v]) {
                    up[v] = in[neighbor];
                }
            }
            else if (in[neighbor] < up[v]) {
                up[v] = up[neighbor];
            }


        }

    }
}

std::vector<std::set<int>> find_biconnected_components(const std::vector<std::set<int>>& graph) {
    std::vector<std::set<int>> biconnected_components;
    std::vector<int> in(graph.size(), -1);
    std::vector<int> up(graph.size(), -1);
    std::vector<bool> visited(graph.size(), false);
    std::stack<std::pair<int, int>> st;
    int time = 0;

    for (int v = 0; v < graph.size(); v++) {
        if (!visited[v]) {
            dfs_blocks(v, -1, graph, biconnected_components, in, up, visited, st, time);
        }
    }

    return biconnected_components;
}

void l_solution() {
    std::cout << "l) solution:\n";
    std::vector<std::set<int>> biconnected_components = find_biconnected_components(graph_g1);
    for (const std::set<int>& component : biconnected_components) {
        std::cout << "[";
        for (int v : component) {
            if (v != *component.begin()) {
                std::cout << ", \"" << g1_names[v] << "\"";
            }
            else {
                std::cout << "\"" << g1_names[v] << "\"";
            }
        }
        std::cout << "],\n";
    }

    std::cout << std::endl << std::endl;
}