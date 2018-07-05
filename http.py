# -*- coding: utf-8 -*-
# Copyright 2017, A10 Networks
# Author: Mike Thompson: @mike @t @a10@networks!com
#
import os, sys, re, requests


import time
# HOST = os.environ['HM_SRV_IPADDR']
# PORT = int(os.environ['HM_SRV_PORT'])
HOST = "google.com"
PORT = 80
#HTTP Config
METHOD = "GET"
URI = "/"
PAYLOAD = None
RESPONSE_CODE = 200
RETURN_STRING = '<!doctype html>'
DATA = None
#SSL Config
HTTPS = True
CHECK_CERT = False
#String Match
#If Exact is True then a explicit match is required else it is a string compair.
# Example Exact = True: x=x: True
# Example Exact = True: x=z:False
# Example Exact = False: a in ABC: False
# Example Exact = False: a in abc: True
# Example EXACT = True & LOWER = False: a = ABC: False
# Example EXACT = False & LOWER = False: a in ABC: False
# Example EXACT = True & LOWER = True: a = ABC: False
# Example EXACT = False & LOWER = True: a in ABC: True
EXACT = False
LOWER = True
RETURN_STRING = '<!doctype html>'

if HTTPS is True:
    if PORT == 443 or PORT == 80:
        URL = "https://{host}/{URI}".format(host=HOST, URI=URI)
    else:
        URL = "https://{host}:{port}/{URI}".format(host=HOST, port=PORT, URI=URI)
else:
    if PORT == 443 or PORT == 80:
        URL = "http://{host}/{URI}".format(host=HOST, URI=URI)
    else:
        URL = "http://{host}:{port}/{URI}".format(host=HOST, port=PORT, URI=URI)


def http():
    if METHOD == "GET":
        return requests.get(URL, verify=CHECK_CERT)
    if METHOD == "POST":
        return requests.post(URL, data=DATA, verify=CHECK_CERT)


def handel_response(response, t):
    VALID_RESPONSE_TEXT = False
    VALID_RESPONSE_CODE = False
    status = response.status_code
    if status == RESPONSE_CODE:
        VALID_RESPONSE_CODE = True
    text = response.text
    if LOWER is True:
        text = text.lower()
    if EXACT is True and RETURN_STRING is not None:
        if  text == RETURN_STRING:
            VALID_RESPONSE_TEXT = True
    elif EXACT is False and RETURN_STRING is not None:
        if RETURN_STRING in text:
            VALID_RESPONSE_TEXT = True

    if VALID_RESPONSE_CODE:
        if RETURN_STRING is None:
            print "HTTP STATUS:", status, "Latency", str(t)
            sys.exit(-1)
        elif VALID_RESPONSE_TEXT:
            print "HTTP STATUS:", status,  "Byte Count", len(response.text), "Latency", str(t)
            sys.exit(-1)
        else:
            print "HTTP STATUS:", status, "MESSAGE", response.text, "Latency", str(t)
            sys.exit(1)
    else:
        print "HTTP STATUS:", status, "MESSAGE", response.text, "Latency", str(t)
        sys.exit(1)

t = time.time()
resp = http()
t = (time.time() - t)
print t
handel_response(resp, t)



if __name__ == "__main__":
    pass