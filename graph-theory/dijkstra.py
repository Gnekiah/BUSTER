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
    print symbo
    print graph



if __name__ == "__main__":
    filename = "graph.txt"
    startpos = "beijing"
    symbo, graph = load_ungraph(filename)
    dijkstra(symbo, graph, startpos)
