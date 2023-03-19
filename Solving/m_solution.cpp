#include "inclusion.h"

void dfs_ebс(int v,
             int parent,
             const std::vector<std::set<int>>& graph,
             std::vector<std::set<int>>& edge_biconnected_components,
             std::vector<int>& in, // in[v] — время входа поиска в глубину в вершину u
             std::vector<int>& up, // up[v] — минимум из времени захода в саму вершину in[v], времени захода в предка (необязательно родителя) in[p] если есть ребро (v, p), а также из всех значений up[с] для каждой вершины с, являющейся наследником v в дереве поиска
             std::vector<bool>& visited, // массив, хранящий информацию о (не) посещении вершины
             std::stack<int>& st, // стек для хранения вершин, в порядке обработки
             int& time)
{
    visited[v] = true;
    in[v] = time;
    up[v] = time;
    time++;
    st.push(v);

    // перебираем всех детей узла
    for (int neighbor : graph[v]) {
        if (neighbor != parent) {

            // neighbor является предком v в дереве обхода
            if (in[neighbor] < in[v]) {
                up[v] = std::min(up[v], in[neighbor]);
            }
            // neighbor является наследником v в дереве обхода
            if (!visited[neighbor]) {
                dfs_ebс(neighbor, v, graph, edge_biconnected_components, in, up, visited, st, time);
                up[v] = std::min(up[v], up[neighbor]);

                // условие моста
                if (up[neighbor] > in[v]) {
                    std::cout << g1_names[v] << " - " << g1_names[neighbor] << std::endl;
                    std::set<int> component;
                    // записываем все вершины стека
                    while (!st.empty()) {
                        int vertex = st.top();
                        component.insert(vertex);
                        st.pop();
                        if (vertex == neighbor) {
                            break;
                        }
                    }
                    if (component.size() > 2) {
                        edge_biconnected_components.push_back(component);
                    }
                }
            }
        }
    }
}

std::vector<std::set<int>> find_edge_biconnected_components(const std::vector<std::set<int>>& graph) {
    std::vector<std::set<int>> edge_biconnected_components;
    std::vector<int> in(graph.size(), -1);
    std::vector<int> up(graph.size(), -1);
    std::vector<bool> visited(graph.size(), false);
    std::stack<int> st;
    int time = 0;
    std::cout << "Bridges:\n";
    for (int v = 0; v < graph.size(); v++) {
        if (!visited[v]) {
            dfs_ebс(v, -1, graph, edge_biconnected_components, in, up, visited, st, time);
        }
    }
    std::cout << "\n";
    if (!st.empty()) {
        std::set<int> component;
        while (!st.empty()) {
            component.insert(st.top());
            st.pop();
        }
        if (component.size() > 2) {
            edge_biconnected_components.push_back(component);
        }
    }
    return edge_biconnected_components;
}

void m_solution() {
    std::cout << "m) solution:\n";
    std::vector<std::set<int>> edge_biconnected_components = find_edge_biconnected_components(graph_g1);
    for (const std::set<int>& component : edge_biconnected_components) {
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