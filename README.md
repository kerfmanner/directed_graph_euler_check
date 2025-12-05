
Дано орiєнтований граф G = (V, E). Потрiбно:
а) визначити, чи iснує в графi ейлеровий цикл (шлях, що проходить по кожному
ребру рiвно один раз i повертається в початкову вершину);
б) якщо ейлеровий цикл не iснує, перевiрити iснування ейлерового шляху;
в) у разi iснування — побудувати один iз них.
Вхiднi данi: кiлькiсть вершин, список орiєнтованих ребер.
Вихiднi данi: повiдомлення про вiдсутнiсть ейлерового шляху/циклу або послiдов-
нiсть вершин (або ребер), що утворюють такий шлях/цикл.

## Алгоритм
### 0) Підготовка
Ми знаходимо ейлерів цикл і шлях, степінь кожної вершини:
degree(v_i) = in_degree(v_i) + out_degree(v_i)
### 1) Визначити, чи iснує в графi ейлеровий цикл

Якщо б граф був не орієнтованим можна було би використати:

**Euler's Theorem:**
A connected graph has an Euler cycle if and only if every vertex has an even number of incident edges.

Але у задачі орієнтований граф тому для перевірки чи існує ейлерів цикл використаємо властивість:

A directed graph has an Eulerian cycle if and only if every vertex has equal [in degree](https://en.wikipedia.org/wiki/In_degree_\(graph_theory\) "In degree (graph theory)") and [out degree](https://en.wikipedia.org/wiki/Out_degree_\(graph_theory\) "Out degree (graph theory)"), and all of its vertices with nonzero degree belong to a single [strongly connected component](https://en.wikipedia.org/wiki/Strongly_connected_component "Strongly connected component").
Але імплементація networkx, має жорсткішу умову, що усі вершини, навіть із нульовим степенем мають належати одній компоненті сильної зв'язності графа. Я використаю умови теореми, адже це має більший математичний сенс.


### 2) Якщо ейлеровий цикл не iснує, перевiрити iснування ейлерового шляху

А для перевірки існування ейлерівого шляху використаємо таку властивість:
A directed graph has an Eulerian trail if and only if at most one vertex has ([out-degree](https://en.wikipedia.org/wiki/Out_degree_\(graph_theory\) "Out degree (graph theory)")) − ([in-degree](https://en.wikipedia.org/wiki/In_degree_\(graph_theory\) "In degree (graph theory)")) = 1(start_node), at most one vertex has (in-degree) − (out-degree) = 1(end_node), every other vertex has equal in-degree and out-degree, and all of its vertices with nonzero degree belong to a single connected component of the underlying undirected graph.

### 3) У разi iснування — побудувати один iз них.
Моя імплементація повертає ейлерів цикл, якщо він існує, в іншому випадку, якщо існує ейлерів шлях, то повертає його, якщо не існує ні ейлерівого цикли, ні шляху, тоді повертає повiдомлення про вiдсутнiсть обох:
```c++
enum class EulerType {
    NONE,      // нічого не існує
    PATH,      // існує ейлерів шлях, а циклу не існує
    CYCLE      // існує ейлерів цикл(наслідково існує також шлях)
};
```
 EulerType, sequence of vertices
 Але спершу напишу лише повернення послідовності вершин, які утворюють цикл/шлях, або порожню послідовність, якщо не існує ні того, ні того, або кількість вершин із ненульовим степенем дорівнює нулю.





```python
import networkx as nx
nx.has_eulerian_cycle(G)
nx.has_eulerian_path(G)
list(nx.eulerian_circuit(G))
```