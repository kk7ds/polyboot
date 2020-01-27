#!/usr/bin/python3

# Copyright 2022 Dan Smith <dsmith+polyboot@danplanet.com>
#
# This is capable of rebooting Polycom phones running UCS 4.x (and
# maybe later?) via http. Tested with IP321, IP331, IP335 phones.

import argparse
import logging
import re
import requests
import sys

p = argparse.ArgumentParser()
p.add_argument('--password', '-p', default='456')
p.add_argument('--verbose', '-v', action='store_true')
p.add_argument('--debug', action='store_true')
p.add_argument('--timeout', type=int, default=10)
p.add_argument('--action', choices=['Reboot', 'Restart'],
               default='Restart')
p.add_argument('phone', help="IP or hostname of the phone")
args = p.parse_args()

def verbose(s):
    if (args.verbose):
        print(s)

if args.debug:
    logging.basicConfig(level=logging.DEBUG)

auth = requests.auth.HTTPBasicAuth('Polycom', args.password)
session = requests.Session()

# Try to authenticate and get a session cookie
try:
    r = session.post('http://%s/form-submit/auth.htm' % args.phone, auth=auth,
                     verify=False, timeout=10)
except (requests.exceptions.ConnectTimeout,
        requests.exceptions.ReadTimeout):
    print('Failed to login to %s (Timeout)' % args.phone)
    sys.exit(1)
except requests.exceptions.ConnectionError as e:
    print('Failed to login to %s: %s' % (args.phone, e))
    sys.exit(1)
if r.status_code != 200:
    print('Failed login: %s' % r.content)
    sys.exit(1)
verbose('Login successful to %s' % args.phone)

# Get the main page so we can find the super secret token
r = session.get('http://%s/index.htm' % args.phone, verify=False,
                timeout=10)
if r.status_code != 200:
    print('Failed to get web interface')
    sys.exit(2)

m = re.search('csrf-token. content="(.*)"', r.content.decode())
if not m:
    print('Unable to find super-secret login token')
    sys.exit(2)
token = m.group(1)
verbose('Retrieved super-secret token: %s' % token)

# Do the actual reboot with the super secret token
r = session.post('http://%s/form-submit/%s' % (args.phone, args.action),
                 verify=False, data='', timeout=10,
                 headers={'Content-Type': 'application/x-www-form-urlencoded',
                          'anti-csrf-token': token,
                          'Content-Length': '0'})
if r.status_code != 200:
    print('%s rejected: %s' % (args.action, r.content))
    sys.exit(2)
verbose('%s successful' % args.action)
