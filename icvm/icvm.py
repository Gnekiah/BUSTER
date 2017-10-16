#! /bin/python2.7
# -*- coding: utf-8 -*-
#
# implementation of eleven internal clustering validation measures
# paper - "Understanding of Internal Clustering Validation Measures"
#
# environment: python 2.7 is recommended
# @Xiong X. 2017/10/15

from traceback import extract_stack
import math, sys, time, os

################################################################################
INFOR = True
ERROR = True
DEBUG = False

global nr_clusters      ## number of clusters
global nr_dsobjs        ## number of objects in dataset
global nr_dsattrs       ## number of attributes in dataset
global dscenter         ## center of dataset
global dsdx             ## vector variance of dataset

global nr_clobjs        ## number of objects of each cluster
global clcenter         ## center of each cluster
global cldx             ## vector variance of each cluster
################################################################################
def infor(info):
    es = extract_stack()
    if INFOR: print "[INFOR] <%s>" % es[-2][2], info

def debug(info):
    es = extract_stack()
    if DEBUG: print "[DEBUG] <%s>" % es[-2][2], info

def error(info):
    es = extract_stack()
    if ERROR: print "[ERROR] <%s>" % es[-2][2], info
    exit()

def toupper(x):
    return [i.upper() for i in x if isinstance(i, str)]

def intersec(x, y):
    return list((set(x).union(set(y))) ^ (set(x)^set(y)))

################################################################################
## mathematical functions
def dot_product(x):
    ret = 0.0
    for i in x:
        ret += i * i
    ret = math.sqrt(ret)
    return ret


def scalar_distance(x, y):
    dim = len(x)
    ret = 0.0
    for i in range(dim):
        d = y[i] - x[i]
        ret += d * d
    return math.sqrt(ret)


def vector_add(x, y):
    size = len(x)
    ret = []
    if size == 0 or len(y) != size:
        error("vectors x:%d and y:%d are mismatch." % (len(x), len(y)))
    for i in range(0, size):
        ret.append(x[i]+y[i])
    return ret


def vector_sub(x, y):
    size = len(x)
    ret = []
    if size == 0 or len(y) != size:
        error("vectors x and y are mismatch.")
    for i in range(0, size):
        ret.append(x[i]-y[i])
    return ret


def scalar_square(x):
    ret = []
    for i in range(0, len(x)):
        ret.append(x[i]*x[i])
    return ret

################################################################################
## do init
def calc_nr_clusters(clusters):
    return len(clusters)


def calc_nr_clobjs(clusters):
    global nr_clusters
    nr_clobjs = [0] * nr_clusters
    for i in range(0, nr_clusters):
        nr_clobjs[i] = len(clusters[i])
    return nr_clobjs


def calc_nr_dsobjs(clusters):
    global nr_clobjs
    nr = 0
    for i in nr_clobjs:
        nr += i
    return nr


def calc_nr_dsattrs(clusters):
    nr = 0
    for cluster in clusters:
        if len(cluster) != 0:
            nr = len(cluster[0])
            break
    return nr


def calc_dscenter(clusters):
    global nr_dsobjs
    global nr_dsattrs
    center = None
    if nr_dsattrs == 0 or nr_dsobjs == 0:
        error("calc dscenter failed, clusters cannot be empty.")
    center = [0.0] * nr_dsattrs
    for cluster in clusters:
        for item in cluster:
            center = vector_add(center, item)
    for i in range(0, nr_dsattrs):
        center[i] /= nr_dsobjs
    return center


def _calc_clcenter(cluster):
    global nr_dsattrs
    center = None
    nr = len(cluster)
    if nr_dsattrs == 0:
        error("calc clcenter failed, clusters cannot be empty.")
    center = [0.0] * nr_dsattrs
    for item in cluster:
        center = vector_add(center, item)
    for i in range(0, nr_dsattrs):
        center[i] /= nr
    return center


def calc_clcenter(clusters):
    global nr_clusters
    global nr_dsattrs
    center = []
    if nr_dsattrs == 0 or nr_clusters == 0:
        error("calc clcenter failed, clusters cannot be empty.")
    for cluster in clusters:
        center.append(_calc_clcenter(cluster))
    return center


def calc_dsdx(clusters):
    global nr_dsattrs
    global nr_dsobjs
    global dscenter
    dsdx = None
    if nr_dsattrs == 0:
        error("calc dsdx failed, clusters cannot be empty.")
    dsdx = [0.0] * nr_dsattrs
    for cluster in clusters:
        for item in cluster:
            tmp = vector_sub(item, dscenter)
            dsdx = vector_add(dsdx, scalar_square(tmp))
    for i in range(0, nr_dsattrs):
        dsdx[i] /= nr_dsobjs
    return dsdx


def _calc_cldx(cluster, center):
    global nr_dsattrs
    cldx = None
    nr = len(cluster)
    if nr_dsattrs == 0:
        error("calc cldx failed, clusters cannot be empty.")
    cldx = [0.0] * nr_dsattrs
    for item in cluster:
        tmp = vector_sub(item, center)
        cldx = vector_add(cldx, scalar_square(tmp))
    for i in range(0, nr_dsattrs):
        cldx[i] /= nr
    return cldx


def calc_cldx(clusters):
    global nr_dsattrs
    global clcenter
    cldx = []
    cnt = 0
    if nr_dsattrs == 0:
        error("calc cldx failed, clusters cannot be empty.")
    for cluster in clusters:
        cldx.append(_calc_cldx(cluster, clcenter[cnt]))
        cnt += 1
    return cldx

################################################################################
## functional patchs
def do_init(clusters):
    global nr_clusters
    global nr_dsobjs
    global nr_dsattrs
    global dscenter
    global dsdx
    global nr_clobjs
    global clcenter
    global cldx
    nr_clusters = calc_nr_clusters(clusters)
    nr_clobjs   = calc_nr_clobjs(clusters)
    nr_dsobjs   = calc_nr_dsobjs(clusters)
    nr_dsattrs  = calc_nr_dsattrs(clusters)
    dscenter    = calc_dscenter(clusters)
    clcenter    = calc_clcenter(clusters)
    dsdx        = calc_dsdx(clusters)
    cldx        = calc_cldx(clusters)
    debug("nr clusters= %d" % nr_clusters)
    debug("nr dsobjs= %d" % nr_dsobjs)
    debug("nr dsattrs= %d" % nr_dsattrs)
    debug("ds center= %s" % dscenter)
    debug("ds dx= %s" % dsdx)
    debug("nr clobjs= %s" % nr_clobjs)
    debug("cl center= %s" % clcenter)
    debug("cl dx= %s" % cldx)


## Root-mean-square std dev
def do_rmsstd(clusters):
    global nr_clobjs
    global nr_dsattrs
    global clcenter
    denom = 0.0
    molec = 0.0
    cnt = 0
    ret = 0.0
    for i in nr_clobjs:
        denom = denom + (i-1)
    denom = denom * nr_dsattrs
    for cluster in clusters:
        for item in cluster:
            tmp = vector_sub(item, clcenter[cnt])
            tmp = dot_product(tmp)
            molec = tmp * tmp + molec
        cnt += 1
    if denom == 0.0:
        error("calc rmsstd failed, denominator cannot be zero.")
    ret = math.sqrt(molec / denom)
    return ret


## R-squared
def do_rs(clusters):
    global clcenter
    global nr_clobjs
    global dscenter
    denom = 0.0
    molec = 0.0
    cnt = 0
    ret = 0.0
    for cluster in clusters:
        for item in cluster:
            tmp1 = vector_sub(item, dscenter)
            tmp1 = dot_product(tmp1)
            denom += (tmp1 * tmp1)
            tmp2 = vector_sub(item, clcenter[cnt])
            tmp2 = dot_product(tmp2)
            molec += (tmp2 * tmp2)
        cnt += 1
    if denom == 0.0:
        error("calc rs failed, denominator cannot be zero.")
    ret = (denom - molec) / denom
    return ret


def _do_gamma(cl1, cl2, center1, center2):
    ret = 0.0
    for i in cl1:
        for j in cl2:
            ret += (scalar_distance(i,j) * scalar_distance(center1,center2))
    return ret


## Modified Hubert Γ statistic
def do_gamma(clusters):
    global clcenter
    global nr_clusters
    global nr_dsobjs
    ret = 0.0
    for i in range(0, nr_clusters):
        if i == (nr_clusters-1):
            break
        for j in range(i+1, nr_clusters):
            tmp = _do_gamma(clusters[i],clusters[j],clcenter[i],clcenter[j])
            ret += tmp
    ret =(ret * 2) / (nr_dsobjs * (nr_dsobjs - 1))
    return ret


## Calinski-Harabasz index
def do_ch(clusters):
    global nr_clusters
    global nr_dsobjs
    global nr_clobjs
    global clcenter
    global dscenter
    denom = 0.0
    molec = 0.0
    ret = 0.0
    cnt = 0
    if (nr_clusters == 1):
        error("calc ch failed, number of clusters must bigger than 1.")
    if (nr_clusters == nr_dsobjs):
        error("calc ch failed, number of clusters cannot be equal to objects.")
    for ci in clcenter:
        tmp = scalar_distance(ci, dscenter)
        molec = tmp * tmp * nr_clobjs[cnt]
        cnt += 1
    molec /= (nr_clusters - 1)
    cnt = 0
    for cluster in clusters:
        for item in cluster:
            tmp = scalar_distance(item, clcenter[cnt])
            denom = tmp * tmp
        cnt += 1
    denom /= (nr_dsobjs - nr_clusters)
    ret = molec / denom
    return ret


## I index
def do_i(clusters):
    global nr_clusters
    global clcenter
    global dscenter
    maxdis = 0.0
    denom = 0.0
    molec = 0.0
    do_i_p = 2
    cnt = 0
    ret = 0.0
    if nr_clusters < 2:
        error("calc i failed, number of clusters must bigger than 1.")
    for i in range(0, nr_clusters):
        for j in range(i+1, nr_clusters):
            maxdis = max(maxdis, scalar_distance(clcenter[i], clcenter[j]))
    for cluster in clusters:
        for item in cluster:
            molec += scalar_distance(item, dscenter)
        denom += scalar_distance(item, clcenter[cnt])
        cnt += 1
    ret = pow(molec / (nr_clusters * denom) * maxdis, do_i_p)
    return ret


def _do_d(cl1, cl2, domin):
    ret = 0.0
    if domin:
        ret = float("inf")
    for i in range(0, len(cl1)):
        for j in range(0, len(cl2)):
            if domin:
                ret = min(ret, scalar_distance(cl1[i], cl2[j]))
            else:
                ret = max(ret, scalar_distance(cl1[i], cl2[j]))
    return ret


## Dunn’s indices
def do_d(clusters):
    global nr_clusters
    maxdis = 0.0
    mindis = float("inf")
    ret = 0.0
    if (nr_clusters == 1):
        error("calc d failed, number of clusters must bigger than 1.")
    for cluster in clusters:
        maxdis = max(maxdis, _do_d(cluster, cluster, False))
    for i in range(0, nr_clusters):
        if i == (nr_clusters-1):
            break
        for j in range(i+1, nr_clusters):
            mindis = min(mindis,(_do_d(clusters[i],clusters[j],True)/maxdis))
    ret = mindis
    return ret


def _do_s_x(x, ni, cl):
    ret = 0.0
    for item in cl:
        ret += scalar_distance(x, item)
    ret /= (ni - 1)
    return ret


def _do_s_y(x, cnt, cls):
    global nr_clusters
    global nr_clobjs
    ret = float("inf")
    for i in range(0, nr_clusters):
        if i == cnt:
            continue
        for item in cls[i]:
            ret = min(ret, scalar_distance(x, item) / nr_clobjs[i])
    return ret


def _do_s(cl, cnt, cls):
    global nr_clusters
    global nr_clobjs
    ret = 0.0
    for item in cl:
        a = _do_s_x(item, nr_clobjs[cnt], cl)
        b = _do_s_y(item, cnt, cls)
        ret += (b - a) / max(a, b)
    ret /= nr_clobjs[cnt]
    return ret


## Silhouette index
def do_s(clusters):
    global nr_clusters
    ret = 0.0
    cnt = 0
    if (nr_clusters == 1):
        error("calc s failed, number of clusters must bigger than 1.")
    for cluster in clusters:
        ret += _do_s(cluster, cnt, clusters)
        cnt += 1
    ret /= nr_clusters
    return ret


def _do_db(cl1, cl2, i, j):
    global nr_clobjs
    global clcenter
    xi = 0.0
    xj = 0.0
    ret = 0.0
    for item in cl1:
        xi += scalar_distance(item, clcenter[i])
    xi /= nr_clobjs[i]
    for item in cl2:
        xj += scalar_distance(item, clcenter[j])
    xj /= nr_clobjs[j]
    xk = scalar_distance(clcenter[i], clcenter[j])
    if xk == 0.0:
        return ret
    ret = (xi + xj) / xk
    return ret


## Davies-Bouldin index
def do_db(clusters):
    global nr_clusters
    ret = 0.0
    if (nr_clusters == 1):
        error("calc db failed, number of clusters must bigger than 1.")
    for i in range(0, nr_clusters):
        tmp = 0.0
        for j in range(0, nr_clusters):
            if i == j:
                continue
            tmp = max(tmp, _do_db(clusters[i], clusters[j], i, j))
        ret += tmp
    ret /= nr_clusters
    return ret


def _do_xb(cl1, cl2):
    ret = float("inf")
    for i in cl1:
        for j in cl2:
            tmp = scalar_distance(i, j)
            if tmp == 0.0:
                continue
            ret = min(ret, pow(tmp, 2))
    if ret == float("inf"):
        error("calc xb failed, denominator cannot be zero.")
    return ret


## Xie-Beni index
def do_xb(clusters):
    global nr_dsobjs
    global clcenter
    ret = 0.0
    cnt = 0
    for cluster in clusters:
        molec = 0.0
        for item in cluster:
            molec += pow(scalar_distance(item, clcenter[cnt]), 2)
        domen = nr_dsobjs * _do_xb(clusters[cnt], clusters[cnt])
        ret += molec / domen
        cnt += 1
    return ret


def __do_dis():
    global nr_clusters
    global clcenter
    ret = 0.0
    maxdis = 0.0
    mindis = float("inf")
    for i in clcenter:
        tmps = 0.0
        for j in clcenter:
            tmp = scalar_distance(i, j)
            maxdis = max(maxdis, tmp)
            if tmp != 0.0:
                mindis = min(mindis, tmp)
            tmps += tmp
        ret += (1 / tmps)
    if mindis == 0.0:
        error("calc dis failed, denominator cannot be zero.")
    ret *= (maxdis / mindis)
    return ret


def __do_scat():
    global nr_clusters
    global cldx
    global dsdx
    ret = 0.0
    ds_dx = dot_product(dsdx)
    for i in cldx:
        ret  += dot_product(i) / ds_dx
    ret /= nr_clusters
    return ret


def __do_stdev():
    global nr_dsattrs
    global nr_clusters
    global clcenter
    mean = [0.0] * nr_dsattrs
    dx = [0.0] * nr_dsattrs
    ret = 0.0
    for item in clcenter:
        mean = vector_add(mean, item)
    for i in range(0, nr_dsattrs):
        mean[i] /= nr_clusters
    for item in clcenter:
        tmp = vector_sub(item, mean)
        dx = vector_add(dx, scalar_square(tmp))
    ret = math.sqrt(dot_product(dx)) / nr_clusters
    return ret


def __do_uij(cluster):
    global nr_dsattrs
    nc = len(cluster)
    if nc == 0:
        error("calc uij failed, cluster cannot be empty.")
    uij = [0.0] * nr_dsattrs
    for item in cluster:
        uij = vector_add(uij, item)
    for i in range(0, nr_dsattrs):
        uij[i] /= nc
    return uij


def __do_density(cluster, center, stdev):
    ret = 0.0
    sigma = 0.0
    for item in cluster:
        dis = scalar_distance(item, center)
        sigma += 0 if dis > stdev else 1
    return sigma


def __do_densbw(clusters):
    global clcenter
    global nr_clusters
    ret = 0.0
    stdev = __do_stdev()
    for i in range(0, nr_clusters):
        for j in range(i+1, nr_clusters):
            uij = clusters[i] + clusters[j]
            molec = __do_density(uij, __do_uij(uij), stdev)
            denomi = __do_density(clusters[i],clcenter[i],stdev)
            denomj = __do_density(clusters[j],clcenter[j],stdev)
            denom = max(denomi, denomj)
            if denom == 0.0:
                error("calc densbw failed, denominator cannot be zero.")
            ret += molec / denom
    ret /= (nr_clusters * (nr_clusters - 1))
    return ret


## SD validity index
def do_sd(clusters):
    dis = __do_dis()
    ret = dis * __do_scat() + dis
    return ret


## S Dbw validity index
def do_sdbw(clusters):
    ret = __do_scat() + __do_densbw(clusters)
    return ret


## make Internal Clustering Validation Measures
## if want to save result onto a certain path, set rstpath
## you can specify which function do you wanna
## for example: func=["rs","ch","sd"]
def icvm(clusters, rstpath=None, func=None):
    global nr_clusters
    FUNC = ['RMSSTD','RS','GAMMA','CH','I','D','S','DB','XB','SD','SDBW']
    mat = "{:<10}{:}"
    icvs = {"RMSSTD":[0.0, do_rmsstd],
           "RS":    [0.0, do_rs],
           "GAMMA": [0.0, do_gamma],
           "CH":    [0.0, do_ch],
           "I":     [0.0, do_i],
           "D":     [0.0, do_d],
           "S":     [0.0, do_s],
           "DB":    [0.0, do_db],
           "XB":    [0.0, do_xb],
           "SD":    [0.0, do_sd],
           "SDBW":  [0.0, do_sdbw]}

    dofunc = FUNC if func == None else intersec(toupper(func), FUNC)
    if dofunc == []: error("func error, no function be specified.")
    do_init(clusters)
    for i in dofunc:
        icv = icvs.get(i)
        icv[0] = icv[1](clusters)
        infor(mat.format(i, icv[0]))

    now = time.time()
    result_rpt = "icvm-%s.csv" % str(now) if rstpath == None else rstpath
    exist_flag = True if os.path.isfile(result_rpt) else False
    with open(result_rpt, "at") as f:
        if not exist_flag:
            f.write("NC,RMSSTD,RS,GAMMA,CH,I,D,S,DB,XB,SD,SDBW\n")
        item = str(nr_clusters) + ","
        for i in range(0, len(dofunc)):
            item += str(icvs.get(dofunc[i])[0]) + ","
        f.write(item[:-1] + "\n")
    infor("Completed! Report File is %s" % result_rpt)


## if col. 0 is not id, set noid=True
def init_dataset(path, noid=False):
    clusters = [[]]
    source = []
    header = ""
    ids = 0
    beg = 0 if noid else 1
    with open(path, "rt") as f:
        header = f.readline()[:-1]
        for item in f:
            tmp = item[:-1]
            tmps = tmp.split(",")
            tmpl = []
            for i in tmps[beg:-1]:
                x = float(i)
                tmpl.append(x)
            id = int(tmps[-1])
            if ids < id:
                clusters.extend([[]] * (id-ids))
                ids = id
            clusters[id].append(tmpl)
    infor("load clusters [%s], header= [%s]" % (path, header))
    if noid:
        infor("id of csvfile is not ignnored.")
    else:
        infor("id of csvfile is ignnored.")
    infor
    return clusters


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "invalid parameter"
        exit()
    clusters = init_dataset(sys.argv[1])
    icvm(clusters, func=None)