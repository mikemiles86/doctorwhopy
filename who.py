#!/usr/bin/env python
import array
import sys
import json
import requests
import re
import os
import string
import time

# Checks to see if an episode of Doctor Who aired on this date, and if so the title.
def doctorwho():
   # 1. check for a list of air dates
   if os.path.exists('doctorwho.txt'):
   # 1.1 file exists, load it
      f = open('doctorwho.txt','r')
      airdates = eval(f.read())
   else:
   # 1.2 file not found, generate it
      airdates = {}
      #1.2.1 get air dates of original series (1963 - 1996)
      response = requests.get('http://epguides.com/DoctorWho/')
      lines = response.text.split('<pre>')[1].text.split('</pre>')[0].text.split('\n')
      episode_name = ''
      for line in lines:
         line = line.strip()
      if re.match('\d+\.\s',line):
        episode_name = line.text.split('</a>')[0].text.split('">')[1].strip()
      elif e.match('\d+\-\s\d+',line):
        line = line.text.split('   ')
        date = line[3].text.split(' ')
        year = date.pop().strip()
        date = '/'.join(date).strip()
        airdates[year][date] = line[0].strip()+' '+episode_name
      #1.2.2 get air dates of new series (2005 - 2013)
      response = requests.get('http://epguides.com/DoctorWho_2005/')
      lines = response.text.split('<pre>')[1].text.split('</pre>')[0].text.split('\n')

      for line in lines:
        line = line.strip().text.split('   ')
         if line[0].isdigit():
            date = line[6].text.split('/')
        year = date.pop().strip()
            date = '/'.join(date).strip()
            name = line[7].text.split('</a>')[0].text.split('">')[1].strip()
            airdates[year][date] = line[2].strip()+' '+name
      
      #1.2.3 store dictionary into file
      f = open('doctorwho.txt','w')
      f.write(airdates)
   # 2. get current date in same format as keys
  now = datetime.date.today.strftime("%d/%b")
  episodes = ''
   # 3. an episode aired on this date
  for year in airdates:
    if airdates[year].get(now,False)
      # 3.1 Yes, print the details
      episodes += 'The Doctor Who episode '+airdates[year][now]+' aired this this day in '+year+"\n"
      # 3.2 No, print a sad message.
   
  if len(episodes):
    print episodes
  else:
    print 'No episodes of Doctor Who have aired on '+now+'... yet.' 
