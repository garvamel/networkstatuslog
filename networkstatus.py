#!/usr/bin/env bash

import socket
import datetime
import time
import csv

with open('networklog.csv', 'a') as logfile:
    fieldnames = ['Down', 'Up', 'Interval']
    writer = csv.DictWriter(logfile, fieldnames=fieldnames)
    writer.writeheader()

def internet_connection(host="8.8.8.8", port=53, timeout=10):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False

prevstatus = internet_connection()
if  not prevstatus:
    time_down = datetime.datetime.now()

while True:
    test_time = datetime.datetime.now()
    status = internet_connection()

    if status == prevstatus:
        pass
    elif not status and status != prevstatus:
        time_down = test_time
        prevstatus = status
    elif status and status != prevstatus:
        time_up = test_time
        with open('networklog.csv', 'a') as logfile:
            fieldnames = ['Down', 'Up', 'Interval']
            writer = csv.DictWriter(logfile, fieldnames=fieldnames)
            writer.writerow({'Down': time_down.strftime('%Y-%m-%d %H:%M:%S'), 'Up': time_up.strftime('%Y-%m-%d %H:%M:%S'), 'Interval': str(time_up-time_down)})
        prevstatus = status
    time.sleep(1)

