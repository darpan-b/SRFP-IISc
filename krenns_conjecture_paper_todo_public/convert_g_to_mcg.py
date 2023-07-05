''' This program aims to convert a given graph to its corresponding matching covered graph. '''
''' This is supposed to be done by checking an edge and seeing if it is part of a perfect matching or not. '''

from max_matching import Node, Match

def convert(edges, nv):

    esz=len(edges)
    edges_copy=[]
    for e in edges: edges_copy.append(e)

    already_removed=set()
    for i in range(esz):
        v1, v2=edges[i][0], edges[i][1]
        removed_edges=[]
        for j in range(esz):
            if edges[j][0]==v1 or edges[j][0]==v2 or edges[j][1]==v1 or edges[j][1]==v2:
                if edges[j] in edges_copy: edges_copy.remove(edges[j])
                removed_edges.append(j)
        match = Match.from_edges(nv, edges_copy)
        unmatched_nodes = match.unmatched_nodes()
        print('unmatched nodes =', unmatched_nodes)
        for e in removed_edges:
            if e==i:
                if unmatched_nodes==2:
                    edges_copy.append(edges[e])
                else:
                    already_removed.add(e)
            elif e not in already_removed:
                edges_copy.append(edges[e])

    return edges_copy


def convert_to_mcg(adj_list, nv):
    edges_here=[]
    for i in range(nv):
        for e in adj_list[i]:
            if e>i:
                edges_here.append([i, e])

    print('initial edges =', edges_here)
    
    final_edges=convert(edges_here, nv)

    print('final edges = ', final_edges)

    for i in range(nv):
        for e in adj_list[i]:
            if e>i:
                if [i, e] not in final_edges:
                    adj_list[i].remove(e)
                    adj_list[e].remove(i)
    return adj_list

