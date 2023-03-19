#include "inclusion.h"

void f_solution() {
    std::cout << "f) solution:\n";
    std::vector<std::set<int>> graph = graph_g;
    std::set<int> compsub;
    std::set<int> candidates;
    std::set<int> wrong;
    std::set<int> max_stable_set;

    for (int i = 0; i < graph.size(); i++) {
        candidates.insert(i);
    }

    std::vector<std::set<int>> add_graph (graph.size()); // добавляем в complement граф вершины без ребер
    for (int i = 0; i < graph.size(); i++) {
        // добавляем все возможные ребра, кроме тех, которые были в изначальном графе
        std::set_difference(candidates.begin(), candidates.end(), graph[i].begin(), graph[i].end(), std::inserter(add_graph[i], add_graph[i].begin()));
        add_graph[i].erase(i);
    }

    Bron_Kerbosch_algorithm(add_graph, compsub, candidates, wrong, max_stable_set); // реализация алгоритма в файле e_solution.cpp

    for (int v : max_stable_set) {
        std::cout << g_names[v] << std::endl;
    }

    std::cout << std::endl << std::endl;
}