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
    print('Vertex connectivity =', total_flow)
    # if total_flow >= 2:
    #     print('2-connected')
    # else:
    #     print('Not 2-connected')

def main():
    print('Enter the number of vertices:')
    nV = int(input())
    print('Enter the number of edges:')
    nE = int(input())
    adj = [[] for i in range(nV)]
    capacity = [[0 for i in range(nV)] for j in range(nV)]
    print('Enter 2 space-separated integers, u, v where there is an edge from u to v')
    print('Enter the edges')
    for i in range(nE):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
        capacity[u][v] = 1
        capacity[v][u] = 1
    source, sink = 0, nV-1
    check_connected(adj, capacity, source, sink)

main()
