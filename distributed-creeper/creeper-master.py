#!/bin/python2.7
from urllib2 import urlopen
from traceback import extract_stack
import re, time, sys
import socket, threading

################################################################################
## CONFIG
SLAVE_DATA_PORT = 37021
SLAVE_CONSOLE_PORT = 37022
MASTER_DATA_PORT = 37031
MASTER_CONSOLE_PORT = 37032
SLAVE_IP = [("127.0.0.1", SLAVE_DATA_PORT, SLAVE_CONSOLE_PORT),
            ]

INFO = True
DEBUG = True
WARNING = True
ERROR = True

BUFFER = 65535
################################################################################
## GLOBAL
m_slaves = list()
m_urls = list()
m_data = list()
m_slaves_mutex = threading.Lock()
m_urls_mutex = threading.Lock()
m_data_mutex = threading.Lock()
################################################################################
## COMMON
def info(info):
    es = extract_stack()
    if INFO: print "[INFOR] <%s>" % es[-2][2], info

def debug(info):
    es = extract_stack()
    if DEBUG: print "[DEBUG] <%s>" % es[-2][2], info

def warning(info):
    es = extract_stack()
    if WARNING: print "[ALERT] <%s>" % es[-2][2], info

def error(info):
    es = extract_stack()
    if ERROR: print "[ERROR] <%s>" % es[-2][2], info
################################################################################
## MASTER LISTENER
class master_listener_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def dolisten(self, listener):
        while True:
            conn, addr = listener.accept()
            data = conn.recv(BUFFER)
            debug("recv data length= %d" % len(data))
            datalist = data.split("\n")
            debug("recv data list length= %d" % len(datalist))
            if m_data_mutex.acquire():
                for i in datalist:
                    m_data.append(i)
                m_data_mutex.release()
            debug("recv data length= %d" % len(data))
            conn.close()

    def run(self):
        info("Listener started")
        listener = socket.socket()
        listener.bind(("127.0.0.1", MASTER_DATA_PORT))
        listener.listen(10)
        info("Listener waiting for slave....")
        while True:
            try:
                self.dolisten(listener)
            except Exception, e:
                error("[EXCEPTION] listener failed")
                if ERROR: print e
            time.sleep(1)
################################################################################
## MASTER REQUESTER
class master_requester_thread(threading.Thread):
    def __init__(self):
        self.slaves = []
        if m_slaves_mutex.acquire():
            for ip in SLAVE_IP:
                # ip is slave's ip:port
                # 0 is the amount of urls that slave keep on now
                m_slaves.append([ip[0:2], 0])
                # ip is slave's ip:port
                # 0 is the amount of urls that master will send to slave
                self.slaves.append([ip[0:2], 0])
            m_slaves_mutex.release()
        threading.Thread.__init__(self)

    # ip_port targets to a slave
    # count indicates how many urls will sent to the slave
    def dosend(self, ip_port, count):
        requester = socket.socket()
        requester.connect(ip_port)
        datastr = ""
        cnt = 0
        if m_urls_mutex.acquire():
            while len(m_urls) > 0 and count > 0:
                count -= 1
                if len(m_urls[-1]) + len(datastr) < BUFFER:
                    datastr += m_urls.pop(-1) + " "
                    cnt += 1
                else:
                    break
            m_urls_mutex.release()
        try:
            requester.sendall(datastr)
            debug("send urls length= %d slave= %s: %d" % (cnt,ip_port[0],ip_port[1]))
            requester.close()
        except:
            urlslist = datastr.split()
            if m_urls_mutex.acquire():
                m_urls.extend(urlslist)
                m_urls_mutex.release()

    # do schedule such as how many urls should be sent to a slave
    def ioctl(self):
        if m_slaves_mutex.acquire():
            for i in range(len(self.slaves)):
                self.slaves[i][1] = 5000 - m_slaves[i][1]
                debug("slave= %s urls send= %d" % (self.slaves[i][0][0], self.slaves[i][1]))
            m_slaves_mutex.release()

    def run(self):
        info("requester started")
        ip = ""
        while True:
            try:
                self.ioctl()
                for slave in self.slaves:
                    ip = slave[0][0]
                    self.dosend(slave[0], slave[1])
                time.sleep(1)
            except Exception, e:
                info("[EXCEPTION] requester connect to slave: %s failed" % ip)
                if ERROR: print e
            time.sleep(10)
################################################################################
## MASTER WRITER
class master_writer_thread(threading.Thread):
    def __init__(self):
        self.data = list()
        threading.Thread.__init__(self)

    def dowrite(self):
        debug("do write")
        if m_data_mutex.acquire():
            for i in range(1000):
                if len(m_data) == 0: break
                self.data.append(m_data.pop(0))
            m_data_mutex.release()
        f = open("data.data", "at")
        for i in self.data:
            f.write(i + "\n")
        f.close()
            ####################################################################
            ## PARSE DATA AND DO SAVE

    def run(self):
        while True:
            try:
                time.sleep(30)
                self.dowrite()
            except Exception, e:
                error("[EXCEPTION] writer failed")
                if ERROR: print e
            time.sleep(1)
################################################################################
## MASTER CONSOLE
class master_console_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def update_urlsleft(self, data, addr):
        if m_slaves_mutex.acquire():
            for slave in m_slaves:
                if slave[0][0] == addr:
                    slave[1] = int(data)
                    break
            m_slaves_mutex.release()
        debug("recv s_urls length= %s ip= %s" % (data, addr))

    def dolisten(self, console):
        while True:
            conn, addr = console.accept()
            ret = conn.recv(BUFFER)
            debug("CONSOLE recv data length= %d" % len(ret))
            retlist = ret.split()
            if len(retlist) == 2 and retlist[0] == "cmd_send_urls_left":
                self.update_urlsleft(retlist[1], addr[0])
            else:
                pass
            conn.close()

    def run(self):
        info("Console started")
        console = socket.socket()
        console.bind(("127.0.0.1", MASTER_CONSOLE_PORT))
        console.listen(10)
        info("Console waiting for slaves....")
        while True:
            try:
                self.dolisten(console)
            except Exception, e:
                error("[EXCEPTION] console failed")
                if ERROR: print e
            time.sleep(1)
################################################################################
## MASTER COMMAND
class master_command_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def dosend(self, ip_port, data):
        requester = socket.socket()
        requester.connect(ip_port)
        requester.sendall(data)
        requester.close()

    def cmdctl(self):
        ports = "master"+" "+str(MASTER_DATA_PORT)+" "+str(MASTER_CONSOLE_PORT)
        while True:
            for ip in SLAVE_IP:
                self.dosend((ip[0], ip[2]), ports)
            time.sleep(10)
            for ip in SLAVE_IP:
                self.dosend((ip[0], ip[2]), "cmd_send_urls_left")

    def run(self):
        info("COMMAND started")
        while True:
            try:
                self.cmdctl()
            except Exception, e:
                error("[EXCEPTION] command failed")
                if ERROR: print e
            time.sleep(1)
################################################################################
## MASTER
def master():
    info("Starting CONSOLE....")
    console_thread = master_console_thread()
    console_thread.setDaemon(True)
    console_thread.start()
    time.sleep(1)
    info("Starting listener....")
    listener_thread = master_listener_thread()
    listener_thread.setDaemon(True)
    listener_thread.start()
    time.sleep(1)
    info("Starting requester....")
    requester_thread = master_requester_thread()
    requester_thread.setDaemon(True)
    requester_thread.start()
    time.sleep(1)
    info("Starting writer....")
    writer_thread = master_writer_thread()
    writer_thread.setDaemon(True)
    writer_thread.start()
    time.sleep(1)
    info("Starting COMMAND....")
    command_thread = master_command_thread()
    command_thread.setDaemon(True)
    command_thread.start()
    time.sleep(1)
    info("RUNNING....")
    console_thread.join()
    listener_thread.join()
    requester_thread.join()
    writer_thread.join()
    command_thread.join()


if __name__ == '__main__':
    ############################################################################
    ## Do Test, generate some urls for master
    for i in range(1,10000):
        m_urls.append("https://api.bilibili.com/vipinfo?mid=%s" % str(i))
    ############################################################################
    master()
