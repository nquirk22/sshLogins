#!/usr/bin/env python3

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "progsite.settings")

django.setup()

from logins.models import Fail
from django.db import IntegrityError

import pprint, re, datetime
import support

# get object for pretty-printing the entries
pp = pprint.PrettyPrinter()

# in debugging mode print out lots of extra information
debug = False


# this is the regular expression used for the initial filter
# done by suppport.getFileLines
filter_expr = ":\s(Failed|Accepted)\s(password|none)"

# this is a regular expression used to match the lines in order
# to extract information

# NOTE: this is what you had:
#line_expr = r"([a-zA-Z]{3}\s\d+\s\d+:\d+:\d+).*sshd\[(\d+)\]:\s(Failed|Accepted).*for\s(?:invalid\suser\s)?(\w+)\sfrom\s([\w\.:]+)"

# this is a fix from Dr. Kline:
line_expr = r"([a-zA-Z]{3}\s+\d+\s\d+:\d+:\d+).*sshd\[(\d+)\]:\s(Failed|Accepted).*for\s(?:invalid\suser\s)?(\w+)\sfrom\s([\w\.:]+)"

line_pattern = re.compile(line_expr)

# get a log file
for log_file in (
    #'auth.log.test',
    "/var/log/auth.log",
    "/var/log/auth.log.1",
):

    # now start processing the log file
    print ("\n==> processing: {} on {}".format( log_file, datetime.datetime.now() ))
    
    # failed entries, a dict with key = ssh process id
    entries = {}
    
    # get filtered lines
    lines = support.getFileLines( log_file, filter_expr )
    
    for line in lines:
        if debug: print (line) # debugging only
        matches = line_pattern.search( line )
        if matches:#probably no point to this check
            access = support.logtime2datetime(matches.group(1))
            pid = matches.group(2)
            status = matches.group(3)
            login = matches.group(4)
            ip = matches.group(5)
            
            #get first fail instance and insert it once
            if status != "Accepted" and pid not in entries:
                entries[pid] = (access, login, ip)
            #take out anything that eventually becomes "Accepted"
            elif status == "Accepted" and pid in entries:
                del entries[pid]
                
    if debug:
        pp.pprint(entries)
        
    if debug:
        print ("\nadd new entries into database\n")
        
    for entry in entries.values():
        try:
            fail = Fail(
                initiated=entry[0],
                login=entry[1],
                ip=entry[2]
            )
            fail.save()
            print("new entry: ( {}, {}, {}".format(entry[0], entry[1], entry[2]))
            
        except IntegrityError as intErr:#catch duplicate entry exception
            print("already logged: ( {}, {}, {}".format(entry[0], entry[1], entry[2]))
        except Exception as err:#catch everything else
            print(err)
  
