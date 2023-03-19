#include "inclusion.h"

bool edge::operator<(const edge& b) const {
    if (weight < b.weight) {
        return true;
    }
    else if (weight == b.weight) {
        if (first < b.first) {
            return true;
        }
        else if (first == b.first) {
            if (second < b.second) {
                return true;
            }
            return false;
        }
        return false;
    }
    return false;
}

std::ostream& operator<<(std::ostream& stream, const edge& e) {
    if (e.weight) {
        stream << g_names[e.first] << " - " << g_names[e.second] << " : " << e.weight;
    }
    else {
        stream << "(\"" << g_names[e.first] << "\", \"" << g_names[e.second] << "\"),";
    }
    return stream;
}

std::set<edge> get_edges(const std::vector<std::set<int>>& graph) {
    std::set<edge> edges;
    for (int v = 0; v < graph.size(); v++) {
        for (int u : graph[v]) {
            edges.insert({std::min(v, u), std::max(v, u), distances[u][v]});
        }
    }
    return edges;
}

std::pair<std::vector<std::set<int>>, int> Kruskal_algorithm(const std::vector<std::set<int>>& graph) {
    std::set<edge> edges = get_edges(graph);
    std::vector<std::set<int>> MST(graph.size()); // добавляем в дерево вершины без ребер

    int weight = 0;

    std::set<std::set<int>> con_components; // множество компонент связности
    for (int i = 0; i < graph.size(); i++) {
        con_components.insert({i});
    }
    std::set<int> first_con_component;
    std::set<int> second_con_component;
    std::set<int> joined;


    for (edge e : edges) { // ребра хранятся в set, который обеспечивает неубывающий порядок веса, благодаря перегрузке оператора сравнения структуры edge, это обеспечивает минимальный итоговый вес

        // ищем какие компоненты связности соединяет гипотетическое ребро дерева
        for (std::set<int> con_component : con_components) {
            if (con_component.find(e.first) != con_component.end()) {
                first_con_component = con_component;
            }
            if (con_component.find(e.second) != con_component.end()) {
                second_con_component = con_component;
            }
        }
        // добавляем ребро в дерево, только если оно соединяет разные компоненты связности, не соблюдение этого условия приведет к образованию цикла
        if (first_con_component != second_con_component) {
            weight += e.weight;
            MST[e.first].insert(e.second);
            MST[e.second].insert(e.first);
            std::set_union(first_con_component.begin(), first_con_component.end(), second_con_component.begin(), second_con_component.end(), std::inserter(joined, joined.begin()));
            con_components.insert(joined);
            joined.clear();
            con_components.erase(first_con_component);
            con_components.erase(second_con_component);
        }
    }
    return {MST, weight};
}

void n_solution() {
    std::cout << "n) solution:\n";
    std::pair<std::vector<std::set<int>>, int> ret = Kruskal_algorithm(graph_g);
    std::vector<std::set<int>> MST = ret.first;
    int weight = ret.second;
    std::cout << "Weight : " << weight << "\n\n";
    for (int v = 0; v < MST.size(); v++) {
        std::cout << "\"" << g_names[v] << "\" : [";
        for (int u : MST[v]) {
            if (u != *MST[v].begin()) {
                std::cout << ", \"" << g_names[u] << "\"";
            }
            else {
                std::cout << "\"" << g_names[u] << "\"";
            }
        }
        std::cout << "],\n";
    }

    std::cout << std::endl << std::endl;
}