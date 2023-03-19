#include "inclusion.h"

std::vector<int> Pufer_algorithm(std::vector<std::set<int>> &tree) {
    std::vector<int> pruffer_code;
    for (int n = 0; n < tree.size() - 2; n++) { // код Прюфера имеет на 2 вершины меньше, чем кодируемое дерево, так как последнее ребро исходя из возможности однозначного декодирования не записывается
        for (int v = 0; v < tree.size(); v++) {
            // является ли вершина листом
            if (tree[v].size() == 1) {
                pruffer_code.push_back(*tree[v].begin()); // записываем ее родителя в код

                // удаляем вершину из дерева
                tree[*tree[v].begin()].erase(v);
                tree[v].clear();
                break;
            }
        }
    }
    return pruffer_code;
}

void p_solution() {
    std::cout << "p) solution:\n";
    std::pair<std::vector<std::set<int>>, int> ret = Kruskal_algorithm(graph_g); // реализация алгоритма в файле n_solution.cpp
    std::vector<std::set<int>> MST = ret.first;
    std::vector<int> pruffer_code = Pufer_algorithm(MST);
    for (int v : pruffer_code) {
        std::cout << v << ' ';
    }
    std::cout << std::endl << std::endl;
}