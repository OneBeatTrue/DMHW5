#include "inclusion.h"

std::vector<std::vector<int>> Floyd_Warshall_algorithm(const std::vector<std::set<int>>& graph) {
    // Создаем матрицу расстояний
    int n = graph.size();
    std::vector<std::vector<int>> distance_matrix(n, std::vector<int>(n, INT_MAX));
    for (int i = 0; i < n; i++) {
        distance_matrix[i][i] = 0;
        for (int j : graph[i]) {
            distance_matrix[i][j] = 1;
            distance_matrix[j][i] = 1;
        }
    }
    // Выполняем сам алгоритм
    for (int k = 0; k < n; k++) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (distance_matrix[i][k] != INT_MAX && distance_matrix[k][j] != INT_MAX) { // Проверяем, существует ли впринципе путь через вершину k
                    distance_matrix[i][j] = std::min(distance_matrix[i][j], distance_matrix[i][k] + distance_matrix[k][j]); // Берем путь проходящий через k, если он короче
                }
            }
        }
    }
    return distance_matrix;
}

int get_V(const std::vector<std::set<int>>& graph) {
    return graph.size();
}

int get_E(const std::vector<std::set<int>>& graph) {
    int v_sum = 0;
    // считаем сумму степеней вершин
    for (int i = 0; i < graph.size(); i++) {
        v_sum += graph[i].size();
    }
    return v_sum / 2; // количество ребер - сумма степеней вершин пополам (по лемме о рукопожатиях)
}

int get_d(const std::vector<std::set<int>>& graph) {
    int d = INT_MAX;
    for (int i = 0; i < graph.size(); i++) {
        d = std::min(d, static_cast<int> (graph[i].size())); //минимальная степень вершины в графе - минимальный размер списка смежных вершин среди вершин в графе
    }
    return d;
}

int get_D(const std::vector<std::set<int>>& graph) {
    int D = INT_MIN;
    for (int i = 0; i < graph.size(); i++) {
        D = std::max(D, static_cast<int> (graph[i].size())); //максимальная степень вершины в графе - максимальный размер списка смежных вершин среди вершин в графе
    }
    return D;
}

std::vector<int> get_eccentricity_list(const std::vector<std::vector<int>>& distance_matrix) {
    int n = distance_matrix.size();
    std::vector<int> eccentricity_list(n, INT_MIN);
    for (int i = 0; i < distance_matrix.size(); i++) {
        for (int j = 0; j < distance_matrix[i].size(); j++) {
            eccentricity_list[i] = std::max(eccentricity_list[i], distance_matrix[i][j]); //максимальное расстояние от данной вершины до любой другой - эксцентриситет по определению
        }
    }
    return eccentricity_list;
}

int get_rad(const std::vector<std::vector<int>>& distance_matrix) {
    int rad = INT_MAX;
    std::vector<int>eccentricity_list = get_eccentricity_list(distance_matrix);
    for (int i = 0; i < eccentricity_list.size(); i++) {
        rad = std::min(rad, eccentricity_list[i]); // ищем минимальный эксцентриситет
    }
    return rad;
}

int get_diam(const std::vector<std::vector<int>>& distance_matrix) {
    int diam = INT_MIN;
    std::vector<int>eccentricity_list = get_eccentricity_list(distance_matrix);
    for (int i = 0; i < eccentricity_list.size(); i++) {
        diam = std::max(diam, eccentricity_list[i]); // ищем максимальный эксцентриситет
    }
    return diam;
}

std::vector<std::string> get_center(const std::vector<std::vector<int>>& distance_matrix) {
    int rad = get_rad(distance_matrix); // получаем радиус графа
    std::vector<std::string> center;
    std::vector<int>eccentricity_list = get_eccentricity_list(distance_matrix);
    // ищем вершины эксцентриситет которых равен радиусу
    for (int i = 0; i < eccentricity_list.size(); i++) {
        if (rad == eccentricity_list[i]) {
            center.push_back(g_names[i]);
        }
    }
    return center;
}

void b_solution() {
    std::cout << "b) solution:\n";
    std::vector<std::set<int>> graph = graph_g;
    std::vector<std::vector<int>> distance_matrix = Floyd_Warshall_algorithm(graph); // матрица расстояний
    std::vector<std::string> center = get_center(distance_matrix);
    std::cout << get_V(graph) << '\n';
    std::cout << '\n';
    std::cout << get_E(graph) << '\n';
    std::cout << '\n';
    std::cout << get_d(graph) << '\n';
    std::cout << '\n';
    std::cout << get_D(graph) << '\n';
    std::cout << '\n';
    std::cout << get_rad(distance_matrix) << '\n';
    std::cout << '\n';
    std::cout << get_diam(distance_matrix) << '\n';
    std::cout << '\n';
    std::cout << 3 << '\n'; // минимальный размер цикла в графе (не мультиграфе) 3 - Швеция, Норвегия, Финляндия
    std::cout << '\n';
    for (int i = 0; i < center.size(); i++) {
        std::cout << center[i] << '\n';
    }
    std::cout << '\n';
    std::cout << 1 << '\n'; // минимальная вершинная связность для связного графа 1 - удаляем Испанию и Португалия отделяется в новую компоненту связности
    std::cout << '\n';
    std::cout << 1 << '\n'; // минимальная реберная связность для связного графа 1 - удаляем ребро между Испанией и Португалией и Португалия отделяется в новую компоненту связности
    std::cout << '\n';

    std::cout << std::endl << std::endl;
}