#!/bin/python2.7
from urllib2 import urlopen
from traceback import extract_stack
import re, time, sys
import socket, threading

################################################################################
## CONFIG
CREEPERS = 8

INFO = True
DEBUG = True
WARNING = True
ERROR = True

SLAVE_DATA_PORT = 37021
SLAVE_CONSOLE_PORT = 37022
MASTER_IP = ["192.168.1.1", 37031, 37032]
BUFFER = 65535
################################################################################
## GLOBAL
s_urls = list()
s_data = list()
s_newurls = list()
s_urls_mutex = threading.Lock()
s_data_mutex = threading.Lock()
s_newurls_mutex = threading.Lock()
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
## SLAVE CREEPER
class slave_creeper_thread(threading.Thread):
    def __init__(self, id):
        self.urls = list()
        self.id = id
        threading.Thread.__init__(self)

    def get_urls(self):
        if s_urls_mutex.acquire():
            for i in range(100):
                if len(s_urls) == 0: break
                self.urls.append(s_urls.pop(0))
            debug("Creeper ID= %d s_urls length= %d" % (self.id, len(s_urls)))
            s_urls_mutex.release()

    def docrawl(self):
        self.get_urls()
        if len(self.urls) == 0:
            time.sleep(10)
            return
        url = self.urls.pop(-1)
        debug("url= %s" % url)
        content = urlopen(url).read()
        if s_data_mutex.acquire():
            s_data.append(content)
            s_data_mutex.release()

    def run(self):
        info("Creeper ID= %d started" % self.id)
        while True:
            try:
                self.docrawl()
            except Exception, e:
                error("[EXCEPTION] creeper failed")
                if ERROR: print e
            time.sleep(1)
################################################################################
## SLAVE LISTENER
class slave_listener_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def dolisten(self, listener):
        while True:
            conn, addr = listener.accept()
            data = conn.recv(BUFFER)
            debug("recv data length= %d" % len(data))
            urlslist = data.split()
            debug("recv data list length= %d" % len(urlslist))
            if s_urls_mutex.acquire():
                for i in urlslist:
                    s_urls.append(i)
                debug("s_urls length= %d" % len(s_urls))
                s_urls_mutex.release()
            conn.close()

    def run(self):
        info("Listener started")
        listener = socket.socket()
        listener.bind(("127.0.0.1", SLAVE_DATA_PORT))
        listener.listen(5)
        info("Listener waiting for master....")
        while True:
            try:
                self.dolisten(listener)
            except Exception, e:
                error("[EXCEPTION] listener failed")
                if ERROR: print e
            time.sleep(1)
################################################################################
## SLAVE REQUESTER
class slave_requester_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def dosend(self):
        requester = socket.socket()
        requester.connect((MASTER_IP[0], MASTER_IP[1]))
        datastr = ""
        if s_data_mutex.acquire():
            while len(s_data) > 0:
                if len(s_data[-1]) + len(datastr) < BUFFER:
                    datastr += s_data.pop(-1) + "\n"
                else:
                    break
            s_data_mutex.release()
        requester.sendall(datastr)
        debug("send s_data length= %d" % len(datastr))
        requester.close()

    def run(self):
        info("requester start")
        while True:
            try:
                self.dosend()
                time.sleep(1)
            except Exception, e:
                error("[EXCEPTION] requester failed")
                if ERROR: print e
            time.sleep(10)
################################################################################
## SLAVE CONSOLE
class slave_console_thread(threading.Thread):
    def __init__(self):
        # this flag point if master port have been updated
        self.master_flag = True
        threading.Thread.__init__(self)

    def get_urls_length(self):
        length = ""
        if s_urls_mutex.acquire():
            length = str(len(s_urls))
            s_urls_mutex.release()
        return length

    def dosend(self, data, cmd):
        requester = socket.socket()
        requester.connect((MASTER_IP[0], MASTER_IP[2]))
        requester.sendall(cmd+" "+data)
        requester.close()

    def dolisten(self, console):
        while True:
            conn, addr = console.accept()
            cmd = conn.recv(BUFFER)
            cmdlist = cmd.split()
            debug("CONSOLE recv data length= %d" % len(cmd))
            if cmdlist[0] == "cmd_stop":
                pass
            elif cmdlist[0] == "cmd_send_urls_left":
                self.dosend(self.get_urls_length(), "cmd_send_urls_left")
            elif cmdlist[0] == "master" and self.master_flag:
                if len(cmdlist) == 3:
                    MASTER_IP[0] = addr[0]
                    MASTER_IP[1] = int(cmdlist[1])
                    MASTER_IP[2] = int(cmdlist[2])
                    info("update master: (%s,%s,%s)" % (addr[0], cmdlist[1], cmdlist[2]))
                    self.master_flag = False
            conn.close()

    def run(self):
        info("Console started")
        console = socket.socket()
        console.bind(("127.0.0.1", SLAVE_CONSOLE_PORT))
        console.listen(5)
        info("Console waiting for master....")
        while True:
            try:
                self.dolisten(console)
            except Exception, e:
                error("[EXCEPTION] console failed")
                if ERROR: print e
            time.sleep(1)
################################################################################
## SLAVE
def slave():
    info("Starting CONSOLE....")
    console_thread = slave_console_thread()
    console_thread.setDaemon(True)
    console_thread.start()
    time.sleep(1)
    info("Starting listener....")
    listener_thread = slave_listener_thread()
    listener_thread.setDaemon(True)
    listener_thread.start()
    time.sleep(1)
    info("Starting creepers CREEPERS=%s.... " % str(CREEPERS))
    creeper_threads = []
    for i in range(CREEPERS):
        creeper_thread = slave_creeper_thread(i)
        creeper_threads.append(creeper_thread)
    for thread in creeper_threads:
        thread.setDaemon(True)
        thread.start()
        time.sleep(1)
    info("Starting requester....")
    requester_thread = slave_requester_thread()
    requester_thread.setDaemon(True)
    requester_thread.start()
    time.sleep(1)
    info("RUNNING....")
    console_thread.join()
    listener_thread.join()
    for thread in creeper_threads:
        thread.join()
    requester_thread.join()


if __name__ == '__main__':
    slave()
