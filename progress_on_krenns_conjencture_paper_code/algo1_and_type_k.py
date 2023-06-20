from max_matching import Node, Match
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


def find_mu(adjacency_list, degrees, nv):
    v = random.randint(0, nv-1) # Pick any v \in V(G), arbitrarily

    C = [] # C = \phi

    if max(degrees) >= 5: return 1 # if d(v) >= 5 then mu(G) <- 1

    # now try to find a perfect matching for every edge (u,v)
    # after you find that, then try and pick arbitrary perfect matchings {e1, e2} such that e1 \in M1 and e2 \in M2


    ''' It is probably not working becaue the Edmond's Blossom Algorithm implementation in /max_matching.py does not
        cater to graphs with disconnected components.'''

    # nodes = [Node() for i in range(nv)]
    # for i in range(nv):
    #     for u in adjacency_list[i]:
    #         nodes[i].neighbors.append(nodes[u])

    # for u in adjacency_list[v]:
    #     # remove the edge (u,v) from the graph
    #     for e in adjacency_list[u]:
    #         nodes[e].neighbors.remove(nodes[u])
    #     for e in adjacency_list[v]:
    #         nodes[e].neighbors.remove(nodes[v])

    # match = Match(nodes)

    # print('Matching is:')
    # for node in nodes:
    #     if node.mate != None:
    #         assert node.mate.mate == node
    #         print(node, node.mate)

    all_matchings = []
    for u in adjacency_list[v]:
        print('u', u, 'v', v)

        nodes = [Node() for i in range(nv-2)]
        prev_value = [i for i in range(nv)]
        for i in range(nv):
            if i == u or i == v: continue
            curno = i
            if i > u: curno -= 1
            if i > v: curno -= 1
            prev_value[curno] = i
            print('prev value = ', prev_value, 'i =', i, 'nv = ', nv)
        for i in range(nv):
            if i == u or i == v: continue
            curnode = i
            if i > u: curnode -= 1
            if i > v: curnode -= 1
            for e in adjacency_list[i]:
                neighnode = e
                if e == u or e == v: continue
                if e > u: neighnode -= 1
                if e > v: neighnode -= 1
                nodes[curnode].neighbors.append(nodes[neighnode])
        
        match = Match(nodes)
        print('unmatched_nodes =', match.unmatched_nodes())
        print('Matching =')
        already_present = set()
        current_matching = [[u,v]]
        for node in nodes:
            if node.mate != None:
                assert node.mate.mate == node
                # print(node, node.mate)
                num1 = (node.index)%(nv-2)
                num2 = (node.mate.index)%(nv-2)
                # if num1+1 >= min(u,v): num1 += 1
                # if num1+1 >= max(u,v): num1 += 1
                # if num2+1 >= min(u,v): num2 += 1
                # if num2+1 >= max(u,v): num2 += 1
                if prev_value[num1] in already_present: continue
                smaller, bigger = prev_value[num1], prev_value[num2]
                if smaller > bigger: smaller, bigger = bigger, smaller
                current_matching.append([smaller, bigger])
                already_present.add(prev_value[num1])
                already_present.add(prev_value[num2])
                print(prev_value[num1]+1, prev_value[num2]+1)

        print('current matching = ')
        print(current_matching)
        all_matchings.append(current_matching)

    '''
    DO NOT TOUCH FROM HERE ONWARDS!!!
    '''





    
    tot_matchings = len(all_matchings)

    hamiltonian_cycle = []
    w1, w2 = [-1 for i in range(nv)], [-1 for i in range(nv)]

    for i in range(tot_matchings):
        if hamiltonian_cycle: break
        for j in range(i+1, tot_matchings):
            m1, m2 = all_matchings[i], all_matchings[j]
            assert(len(m1) == len(m2) and len(m1) == nv//2)
            # m1_s = set()
            # for e in m1: m1_s.add(e)
            is_hamiltonian = True
            for k in range(nv//2):
                if m2[k] in m1:
                    is_hamiltonian = False
                    break
            if not is_hamiltonian: continue


            ''' TODO: CHECK PROPERLY WHETHER A HAMILTONIAN CYCLE IS FORMED OR NOT!!!'''



            for e in m1:
                w1[e[0]], w1[e[1]] = e[1], e[0]
                hamiltonian_cycle.append(e)
            for e in m2:
                w2[e[0]], w2[e[1]] = e[1], e[0]
                hamiltonian_cycle.append(e)
            break

    print('hamiltonian cycle', hamiltonian_cycle)
    
    re_numbering = [-1 for i in range(nv)]
    re_numbering[0] = 0
    current_number = 1
    current_vertex = w1[0]
    while current_vertex != 0:
        re_numbering[current_vertex] = current_number
        current_number += 1
        if current_number % 2 == 0:
            current_vertex = w2[current_vertex]
        else:
            current_vertex = w1[current_vertex]
    
    print('re_numbering', re_numbering)
    
    is_2 = True
    edge_set = []
    '''checking property 1'''
    for i in range(nv):
        for u in adjacency_list[i]:
            if u > i: continue
            edge_set.append([u, i])
            found = False
            for e in hamiltonian_cycle:
                if (e[0] == i and e[1] == u) or (e[0] == u and e[1] == i):
                    found = True
                    break

            ''' DOES NOT REALLY MAKE SENSE TO KEEP IT BECAUSE WHAT EXACTLY IS A HAMILTONIAN CYCLE VARIES '''
            ''' WHAT IS A C-EDGE IN SOME HAMILTONIAN CYCLE CAN BE A DRUM IN ANOTHER HAMILTONIAN CYCLE '''
            # if not found:
            #     if re_numbering[u] % 2 != re_numbering[i] % 2:
            #         is_2 = False
            #         print('YO')
            #         return 1

    print('edge set')
    print(edge_set)
    '''checking property 2'''
    n_es = len(edge_set)
    drum_no = [-1 for i in range(n_es)]
    drums = 0
    for i in range(n_es):
        if edge_set[i] in hamiltonian_cycle:
            drum_no[i] = -2
            continue
        if [edge_set[i][1],edge_set[i][0]] in hamiltonian_cycle:
            drum_no[i] = -2
            continue
        for j in range(i+1, n_es):
            if edge_set[i][0] == edge_set[j][1] and edge_set[i][1] == edge_set[j][0]: continue
            e1, e2 = edge_set[i], edge_set[j]
            if e2 in hamiltonian_cycle: continue
            if [edge_set[j][1],edge_set[j][0]] in hamiltonian_cycle: continue
            v1, v2, v3, v4 = e1[0], e1[1], e2[0], e2[1]
            print('v1', v1+1, 'v2', v2+1, 'v3', v3+1, 'v4', v4+1)
            lv = [v1, v2, v3, v4]
            lv.sort()
            if not((lv[0] == v1 and lv[2] == v2) or (lv[0] == v2 and lv[2] == v1) or (lv[1] == v1 and lv[3] == v2) or (lv[1] == v2 and lv[3] == v1)):
                continue
            poss1 = [[v1, v3], [v2, v4]]
            poss2 = [[v1, v4], [v2, v3]]
            f1 = [False, False]
            f2 = [False, False]
            for e in hamiltonian_cycle:
                if (e[0] == poss1[0][0] and e[1] == poss1[0][1]) or (e[0] == poss1[0][1] and e[1] == poss1[0][0]):
                    f1[0] = True
                if (e[0] == poss1[1][0] and e[1] == poss1[1][1]) or (e[0] == poss1[1][1] and e[1] == poss1[1][0]):
                    f1[1] = True
                if (e[0] == poss2[0][0] and e[1] == poss2[0][1]) or (e[0] == poss2[0][1] and e[1] == poss2[0][0]):
                    f2[0] = True
                if (e[0] == poss2[1][0] and e[1] == poss2[1][1]) or (e[0] == poss2[1][1] and e[1] == poss2[1][0]):
                    f2[1] = True
            if (f1[0] and f1[1]) or (f2[0] and f2[1]):
                if drum_no[i] != -1 or drum_no[j] != -1:
                    print('YAO')
                    return 1
                drums += 1
                drum_no[i], drum_no[j] = drums, drums
            else:
                print('MEOW?')
                return 1
    
    '''checking property 3'''
    if drums == 0: return 2
    d_count = [0 for i in range(drums)]
    for i in range(n_es):
        if drum_no[i] == -1: return 1
        if drum_no[i] == -2: continue
        d_count[drum_no[i]-1] += 1
    print('d_count = ', d_count)
    if max(d_count) == 2 and min(d_count) == 2: return 2
    else: return 1

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
    print('Edges of the graph (1-indexed):')
    for i in range(ne):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj_list[u].append(v)
        adj_list[v].append(u)   
        degree[u] += 1
        degree[v] += 1
        capacity[u][v] = 1
        capacity[v][u] = 1
    is_type2 = (find_mu(adj_list, degree, nv) == 2)
    connectivity = check_connected(adj_list, capacity, 0, nv - 1)
    is_2_connected = (connectivity >= 2)
    is_3_connected = (connectivity >= 3)
    
    print('Is type 2:', 'Yes' if is_type2 else 'No')
    print('Is 2-connected:', 'Yes' if is_2_connected else 'No')
    print('Is 3-connected:', 'Yes' if is_3_connected else 'No')

main()
