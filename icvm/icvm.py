#! /bin/python2.7

from traceback import extract_stack
import math

################################################################################
INFOR = True
DEBUG = True
ERROR = True

global nr_clusters
global nr_dsobjs
global nr_dsattrs
global dscenter
global dsdx

global nr_clobjs
global clcenter
global cldx
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

################################################################################
## mathematical functions
def dot_product(x):
    ret = 0.0
    for i in x:
        ret += i * i
    ret = math.sqrt(ret)
    return ret


def distance(x, y):
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
        error("vectors x and y are mismatch.")
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
        cldx[i] /=nr
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


def do_rmsstd(clusters):
    pass


def icvm(clusters):
    do_init(clusters)

    icv_rmsstd  = do_rmsstd(clusters)
'''
    icv_rs      = do_rs(clusters)
    icv_gamma   = do_gamma(clusters)
    icv_ch      = do_ch(clusters)
    icv_i       = do_i(clusters)
    icv_d       = do_d(clusters)
    icv_s       = do_s(clusters)
    icv_db      = do_db(clusters)
    icv_xb      = do_xb(clusters)
    icv_sd      = do_sd(clusters)
    icv_sdbw    = do_sdbw(clusters)
'''

if __name__ == "__main__":
    clusters = [[[5,2,3,4,5,6,7],[2,3,4,5,6,7,8],[3,4,5,6,7,8,9]],
                [[9,1,1,1,1,1,1],[2,3,4,3,2,1,2],[3,3,3,4,4,2,1]],
                [[6,5,4,6,7,8,9],[4,4,2,8,3,4,5],[5,5,5,5,5,5,4]]]
    icvm(clusters)