import random # for random.randint()

'''
To check whether a graph is k-connected, I'm using the Edmonds-Karp algorithm to find the maximum flow of a
graph in O(|V||E|^2) time.
The max-flow-min-cut theorem states that the maximum flow of a graph is equal to the minimum cut of a graph.
If the min cut of a graph is >= k, that means the graph is k-connected. Thus we can find out the minimum cut
of a graph, and hence check whether the graph is 2-connected or 3-connected.
'''

'''
Performs breadth first search required for finding an augmenting path according to the Ford-Fulkerson method.
Returns 0 if no augmenting path is found.
'''
def bfs(adj, capacity, source, sink, parent):
    nV = len(adj)
    for i in range(nV): parent[i] = -1
    parent[source] = -2
    q = []
    INF = 1e18
    q.append([source, INF])
    while q:
        curnode = q[0][0]
        curflow = q[0][1]
        q.pop(0)
        for u in adj[curnode]:
            if parent[u] != -1 or capacity[curnode][u] == 0:
                continue
            parent[u] = curnode
            newflow = min(curflow, 1)
            if u == sink: return newflow
            q.append([u, newflow])
    return 0


'''
Finds out the connectivity of a graph, by finding the maximum flow of a graph. Basically what it does is:
- Find an augmenting path in the graph using bfs.
- If augmenting path is found, add the flow of the augmenting path to the maximum flow and perform bfs again.
- If augmenting path is not found, return the maximum flow obtained so far since that is the maximum flow of
the graph, or the minimum cut of the graph.

Here we are assuming the graph to be undirected and connected, thus source and sink can be any two random
vertices.
'''
def check_connected(adj, capacity, source, sink):
    nV = len(adj)
    total_flow = 0
    parent = [-1 for i in range(nV)]
    while True:
        new_flow = bfs(adj, capacity, source, sink, parent)
        if new_flow == 0: break
        total_flow += new_flow
        curnode = sink
        while curnode != source:
            par = parent[curnode]
            capacity[curnode][par] += new_flow
            capacity[par][curnode] -= new_flow
            curnode = par
    return total_flow


'''
Performs depth first search in order to find a matching (here it is always a perfect matching since it is
a matching-covered graph) of the graph.
'''
def dfs(cur_v, par_v, adj_list, contains, cur_matching, visited):
    visited[cur_v] = True
    visited[par_v] = True
    if cur_v not in contains and par_v not in contains:
        contains.add(par_v)
        contains.add(cur_v)
        cur_matching.append([par_v, cur_v])
    for u in adj_list[cur_v]:
        if visited[u]:
            continue
        dfs(u, cur_v, adj_list, contains, cur_matching, visited)


'''
Basically direct implementation of algorithm 1 in the paper, apart from a few changes, which, if needed will
be commented.
'''
def find_type(adj_list, degree, nv):
    # Given that the input graph is a non-trivial matching covered graph, if Δ(G) >= 5, μ(G) = 1.
    if max(degree) >= 5:
        return 1
    
    # Choosing an arbitrary vertex v
    v = random.randint(0, nv - 1)
    C = []
    matchings_v = [] # Stores all the matchings of the graph

    for u in adj_list[v]:
        contains = set()
        cur_matching = [] # Stores the matching containing the edge (u,v)
        visited = [False] * nv
        dfs(u, v, adj_list, contains, cur_matching, visited)
        matchings_v.append(cur_matching)
    
    
    tot_matchings = len(matchings_v)
    
    for i in range(tot_matchings):
        for j in range(i + 1, tot_matchings):
            m1 = matchings_v[i]
            m2 = matchings_v[j]
            
            # Checking if m1 U m2 forms a Hamiltonian cycle
            if len(m1) != nv // 2 or len(m2) != nv // 2:
                continue

            # To check if m1 U m2 is a Hamiltonian cycle - 
            # - Both matchings should be perfect matchings
            # - In each matching, every vertex, u is connected to a vertex, v; but in both the matchings,
            # (u,v) should not be present. Like, if m1 contains (u,v), m2 should contain (u,w), and not (u,v).
            count1, count2 = [0] * nv, [0] * nv
            with1, with2 = [-1] * nv, [-1] * nv
            for e in m1:
                count1[e[0]] += 1
                count1[e[1]] += 1
                with1[e[0]] = e[1]
                with1[e[1]] = e[0]
            for e in m2:
                count2[e[0]] += 1
                count2[e[1]] += 1
                with2[e[0]] = e[1]
                with2[e[1]] = e[0]
            is_hamiltonian = True
            for k in range(nv):
                if count1[k] == 1 and count2[k] == 1 and with1[k] != with2[k]:
                    continue
                else:
                    is_hamiltonian = False
                    break
            if is_hamiltonian:
                m = m1
                for e in m2:
                    m.append(e)
                C.append(m)

    # If C = Φ, μ(G) = 1.
    if not C:
        return 1
    
    # Checking if all other edges in the graph other than the cycle edges are legal edges or not.
    # I do this by re-numbering the vertices, and then checking their legality using the parity of the
    # re-numbered vertices.
    lc = len(C)
    matching = C[random.randint(0, lc - 1)]
    parity = [-1 for i in range(nv)]
    for i in range(nv // 2):
        v1 = matching[i][0]
        v2 = matching[i][1]
        if parity[v1] == -1 and parity[v2] == -1:
            parity[v1], parity[v2] = 0, 1
        elif parity[v1] == -1:
            parity[v2] = parity[v1] ^ 1
        elif parity[v2] == -1:
            parity[v1] = parity[v2] ^ 1
        if parity[v1] == parity[v2]:
            assert(False)
    for i in range(nv // 2, nv):
        v1 = matching[i][0]
        v2 = matching[i][1]
        if parity[v1] == -1 and parity[v2] == -1:
            parity[v1], parity[v2] = 0, 1
        elif parity[v1] == -1:
            parity[v2] = parity[v1] ^ 1
        elif parity[v2] == -1:
            parity[v1] = parity[v2] ^ 1
        if parity[v1] == parity[v2]:
            assert(False)
    actual_numbering = [-1] * nv
    actual_numbering[0] = 0
    cur = 1
    cur_vertex = with1[0]
    while cur_vertex != 0:
        actual_numbering[cur_vertex] = cur
        cur += 1
        if cur % 2 == 0:
            cur_vertex = with2[cur_vertex]
        else:
            cur_vertex = with1[cur_vertex]
    matching_set = set()
    for e in matching:
        matching_set.add(tuple(e))
    legal_edges, illegal_edges = set(), []
    for i in range(nv):
        for u in adj_list[i]:
            if (i, u) in matching_set or (u, i) in matching_set:
                continue
            if parity[i] == parity[u]:
                if (u, i) not in legal_edges and (i, u) not in legal_edges:
                    legal_edges.add((u, i))
            else:
                illegal_edges.append([u, i])
                break
        if illegal_edges:
            break
    if illegal_edges:
        return 1
    le_list = []
    for e in legal_edges:
        le_list.append(list(e))
    n_le = len(le_list)

    # Now I'm checking whether all crossing pairs form a drum, and if they form a drum, checking if
    # each edge is part of exactly 1 drum.
    drum_no = [-1 for i in range(n_le)]
    drums = 0
    possible = True
    for i in range(n_le):
        for j in range(i + 1, n_le):
            crossing = []
            crossing.append([le_list[i][0], 0])
            crossing.append([le_list[i][1], 0])
            crossing.append([le_list[j][0], 1])
            crossing.append([le_list[j][1], 1])
            crossing.sort()
            if crossing[0][1] == crossing[2][1]:
                if parity[crossing[0][0]] == parity[crossing[1][0]]:
                    possible = False
                    break
                else:
                    if drum_no[i] != -1 or drum_no[j] != -1:
                        possible = False
                        break
                    drum_no[i] = drums
                    drum_no[j] = drums
                    drums += 1
        if not possible:
            break
    if not possible:
        return 1
    return 2
            

def main():
    nv, ne = 0, 0
    print('Number of vertices in the graph:')
    nv = int(input())
    # Using adjacency list instead of an adjacency matrix because it is faster(?)
    adj_list = [[] for i in range(nv)]
    degree = [0 for i in range(nv)]
    print('Number of edges in the graph:')
    ne = int(input())
    capacity = [[0 for i in range(nv)] for j in range(nv)]
    print('Edges of the graph (0-indexed):')
    for i in range(ne):
        u, v = map(int, input().split())
        adj_list[u].append(v)
        adj_list[v].append(u)   
        degree[u] += 1
        degree[v] += 1
        capacity[u][v] = 1
        capacity[v][u] = 1
    is_type2 = (find_type(adj_list, degree, nv) == 2)
    is_2_connected = (check_connected(adj_list, capacity, 0, nv - 1) >= 2)
    is_3_connected = (check_connected(adj_list, capacity, 0, nv - 1) >= 3)
    
    print('Is type 2:', 'Yes' if is_type2 else 'No')
    print('Is 2-connected:', 'Yes' if is_2_connected else 'No')
    print('Is 3-connected:', 'Yes' if is_3_connected else 'No')

main()
