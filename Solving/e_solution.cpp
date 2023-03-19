#include "inclusion.h"

bool check(const std::vector<std::set<int>>& graph, const std::set<int>& candidates, const std::set<int>& wrong) {
    // wrong не содержит вершину, соединенную со всеми вершинами из candidates
    for (int v: wrong) {
        if (graph[v] == candidates) {
            return false;
        }
    }
    return true;
}

void Bron_Kerbosch_algorithm(
        const std::vector<std::set<int>>& graph,
        std::set<int>& compsub, // множество, содержащее на каждом шаге рекурсии полный подграф для данного шага
        std::set<int>& candidates, //  множество вершин, которые могут увеличить compsub
        std::set<int>& wrong, //  множество вершин, которые уже использовались для расширения compsub на предыдущих шагах алгоритма
        std::set<int>& max_clique)
{
    while(!candidates.empty() && check(graph, candidates, wrong)) {
        int v = *candidates.begin(); // выбираем вершину v из candidates
        // формируем new_compsub добавляя v
        std::set<int> new_compsub(compsub);
        new_compsub.insert(v);
        // формируем new_candidates и new_wrong, удаляя из candidates и not вершины, не соединенные с v
        std::set<int> new_candidates;
        std::set_intersection(candidates.begin(), candidates.end(), graph[v].begin(), graph[v].end(),
                              std::inserter(new_candidates, new_candidates.begin()));

        std::set<int> new_wrong;
        std::set_intersection(wrong.begin(), wrong.end(), graph[v].begin(), graph[v].end(),
                              std::inserter(new_wrong, new_wrong.begin()));
        if (new_candidates.empty() && new_wrong.empty()) { // клика найдена
            // проверяем, является ли наибольшей
            if (new_compsub.size() > max_clique.size()) {
                max_clique = new_compsub;
            }
        } else {
            // запускаем функцию рекурсивно
            Bron_Kerbosch_algorithm(graph, new_compsub, new_candidates, new_wrong, max_clique);
        }
        // удаляем v из candidates и помещаем в wrong
        candidates.erase(v);
        wrong.insert(v);
    }
}

void e_solution() {
    std::cout << "e) solution:\n";
    std::vector<std::set<int>> graph = graph_g;
    std::set<int> compsub;
    std::set<int> candidates;
    std::set<int> wrong;
    std::set<int> max_clique;

    for (int i = 0; i < graph.size(); i++) {
        candidates.insert(i);
    }

    Bron_Kerbosch_algorithm(graph, compsub, candidates, wrong, max_clique);

    for (int v : max_clique) {
        std::cout << g_names[v] << std::endl;
    }
    std::cout << std::endl << std::endl;
}
