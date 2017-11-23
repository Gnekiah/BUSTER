#!/bin/python2.7

FILENAME = "graph.txt"

def loadgraph(filename):
    cnt = 0
    symbo = dict()
    graph = list()
    with open(filename, "rt") as f:
        for i in f:
            ids = i.strip("\r\n").split(",")
            if ids[0] not in symbo.keys():
                symbo[ids[0]] = cnt
                cnt += 1
            if ids[1] not in symbo.keys():
                symbo[ids[1]] = cnt
                cnt += 1
            while len(graph) < cnt:
                graph.append([])
            graph[symbo[ids[0]]].append([symbo[ids[1]], int(ids[2])])
    return symbo, graph



def dijkstra(filename=None):
    pass


if __name__ == "__main__":
    loadgraph("graph.txt")