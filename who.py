#!/usr/bin/env python

import array
import sys
import json
import requests
import re
import os
import string
import math
import time

# Checks to see if an episode of Doctor Who aired on this date, and if so the title.
# be gentle, I am new to python
def doctorwho(lookup_date=False):
        # 1. check for a list of air dates
        if os.path.exists('doctorwho.txt'):
                # 1.1 file exists, load it
                f = open('doctorwho.txt','r')
                airdates = eval(f.read())
                f.close()
        else:
                # 1.2 file not found, generate it
                airdates = {}
                #1.2.1 get air dates of original series (1963 - 1996)
                response = requests.get('http://epguides.com/DoctorWho/')
                lines = response.text.split('<pre>')[1].split('</pre>')[0].split('\n')
                for line in lines:
                        line = line.strip()
                        if re.match('\d+\.',line):
                                episode_title = line.split('</a>')[0].split('>')[1].strip()
                        elif re.match('\d+\-',line):
                                line = re.sub('\s{2,}','~',line).split('~')
                                date = line[2].strip().split(' ')
                                year = date.pop().strip()
                                date = '/'.join(date).strip()
                                title = line.pop().strip()
                                if re.match('\d+',year):
                                        year = '19'+year
                                        if title[:4]=='Part':
                                                title = episode_title+':'+title
                                        if airdates.get(year,False) == False:
                                                airdates[year] = {}                                
                                        airdates[year][date] = line[0].strip()+' '+title
                #1.2.2 get air dates of new series (2005 - 2013)
                response = requests.get('http://epguides.com/DoctorWho_2005/')
                lines = response.text.split('<pre>')[1].split('</pre>')[0].split('\n')
                for line in lines:
                        line = re.sub('\s{2,}','~',line).split('~')
                        if re.match('\d+',line[0]) and len(line)==4:
                                date = line[2].strip().split('/')
                                year = date.pop().strip()
                                date = '/'.join(date).strip()
                                name = line.pop().split('</a>')[0].split('>').pop().strip()
                                if re.match('\d+',year):
                                        year = '20'+year
                                        if airdates.get(year,False) == False:
                                                airdates[year] = {}
                                        airdates[year][date] = line[1].strip()+' '+name
                #1.2.3 store dictionary into file
                f = open('doctorwho.txt','w')
                f.write(str(airdates))
                f.close()
        # 2. get current date in same format as keys
        if lookup_date:
                now = lookup_date
        else:
                now = time.strftime("%d/%b")
        episodes = ''
        # 3. an episode aired on this date
        for year in airdates:
                if airdates[year].get(now,False):
                # 3.1 Yes, print the details
                        episodes += 'The Doctor Who episode "'+airdates[year][now]+'" aired on this day in '+year+"\n"
        if len(episodes):
                print episodes
        else:
                print 'No episodes of Doctor Who have aired on '+now+'... yet.' 
