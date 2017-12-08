#!/bin/python2.7
import sys

## 无向图
def load_ungraph(filename):
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
            graph[symbo[ids[1]]].append([symbo[ids[0]], int(ids[2])])
    return symbo, graph

## 有向图
def load_digraph(filename):
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


def dijkstra(symbo, graph, startpos):
    verts = symbo.values()
    paths = [[symbo[startpos],0]]
    verts.remove(symbo[startpos])
    while verts:
        currlen = sys.maxint
        currpos = 0
        currpath = None
        for ps in paths:
            for p in graph[ps[-2]]:
                if p[0] not in verts:
                    continue
                if p[1]+ps[-1] < currlen:
                    currlen = p[1]+ps[-1]
                    currpos = p[0]
                    currpath = ps
        newpath = currpath[:-1]
        newpath.extend([currpos, currlen])
        paths.append(newpath)
        verts.remove(currpos)
    for ps in paths:
        for i in range(0, len(ps)-1):
            ps[i] = list(symbo.keys())[list(symbo.values()).index(ps[i])]
    return paths


if __name__ == "__main__":
    filename = "graph-city.txt"
    startpos = "xian"
    symbo, graph = load_ungraph(filename)
    print symbo
    print graph
    paths = dijkstra(symbo, graph, startpos)
    for ps in paths:
        print  "%s => %s= %d \t\t" % (ps[0], ps[-2], ps[-1]),
        s = ""
        for i in ps[:-1]:
            s += i+" -> "
        print s[:-3]


