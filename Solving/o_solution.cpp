#include "inclusion.h"

void dfs(
        int v, // рассматриваемый узел
        int parent, // предок рассматриваемого узла
        const std::vector<std::set<int>> &tree, // дерево
        int weight, // суммарный размер дерева (w.r.t. weight function)
        std::vector<int>& subtree_size, // массив размеров поддеревьев каждого узла
        std::set<int>& centroids) // множество центроидов
{
    bool is_centroid = true;

    // перебираем всех детей узла
    for (int child : tree[v]) {
        if (child != parent) {
            dfs(child, v, tree, weight, subtree_size, centroids);
            subtree_size[v] += distances[v][child] + subtree_size[child];

            // проверяем не будет ли превышать размер поддерева данного ребенка половину общего размера дерева
            if (subtree_size[child] > weight / 2) {
                is_centroid = false;
            }
        }
    }

    // проверяем не будет ли превышать размер оставшегося (без данного узла и его детей) дерева половину общего размера дерева
    if (weight - subtree_size[v] > weight / 2) {
        is_centroid = false;
    }

    if (is_centroid) {
        centroids.insert(v);
    }
}

std::set<int> find_centroid(const std::vector<std::set<int>> &tree, int weight) {
    std::vector<int> subtree_size(tree.size(), 0);
    std::set<int> centroids;

    dfs(0, -1, tree, weight, subtree_size, centroids);

    return centroids;
}

void o_solution() {
    std::cout << "o) solution:\n";
    std::pair<std::vector<std::set<int>>, int> ret = Kruskal_algorithm(graph_g); // реализация алгоритма в файле n_solution.cpp
    std::vector<std::set<int>> MST = ret.first;
    int weight = ret.second;
    std::set<int> centroids = find_centroid(MST, weight);
    for (int v : centroids) {
        std::cout << g_names[v] << std::endl;
    }

    std::cout << std::endl << std::endl;
}