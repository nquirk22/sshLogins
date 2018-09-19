#!/usr/bin/env python3

import datetime
import re

def logtime2datetime(logts):
    now = datetime.datetime.now()
    mark = datetime.datetime.strptime(logts,"%b %d %H:%M:%S")

    year = now.year
    if now.month < mark.month:
        year -= 1

    ts = str(mark)
    return  str(year)+ts[4:]

def getFileLines(f,expr=""): #retrieve lines from file filtered by expr
    f = open(f,"r")
    lines = f.readlines()
    pattern = re.compile(expr)
    send_lines = []
    for line in lines:
        line = line.rstrip("\n")
        if expr == "" or pattern.search(line):
            send_lines.append(line)
    return send_lines

if __name__ == "__main__":
    expr = r":\s(Failed|Accepted)\spassword" 

    for log_file in ( 
		"auth.log.test",
        #"/var/log/auth.log", 
        #"/var/log/auth.log.1",
    ):
        print("==> file : " + log_file)
        lines = getFileLines(log_file,expr)
        for line in lines:
            print(line)

