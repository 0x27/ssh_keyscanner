#!/usr/bin/python2
# coding: utf-8
# ssh hostkey grabber/search-shodan-for tool.
# useful for identifying static keys for fun.
# References/Based-On:
# http://www.iodigitalsec.com/ssh-fingerprint-and-hostkey-with-paramiko-in-python/
# https://shodan.readthedocs.org/en/latest/
# https://github.com/ojarva/python-sshpubkeys
# imports here...
from sshpubkeys import SSHKey # ssh key shit
import paramiko # for ssh bullshit
import argparse # for args and shit
import hashlib  # for hashing shit
import socket   # so we can connect to shit
import shodan   # shodan all the shit
import base64   # base64 encryptin' shit liekpro
import socks    # for tor support
import sys      # exits and shit
# globals.
SHODAN_API_KEY = "LOL NO GTFO" # change this
# colours. don't change these
RED = "\x1b[1;31m"
GREEN = "\x1b[1;32m"
CLEAR = "\x1b[0m"
CYAN = "\x1b[1;36m"
BLUE = "\x1b[1;34m"
YELLOW = "\x1b[1;33m"
# for debugging. True or False.
DEBUG = False # if somethings going wierd just enable debug

def msg_info(msg): # informational.
	print "%s{i} %s%s" %(CYAN, msg, CLEAR)

def msg_status(msg): # statuses and shit
    print "%s{*} %s%s" %(BLUE, msg, CLEAR)

def msg_success(msg): # for the wins
    print "%s{+} %s%s" %(GREEN, msg, CLEAR)

def msg_fail(msg): # when shit breaks catastrophically, we return False
	print "%s{!} %s%s" %(RED, msg, CLEAR)
    return False

def msg_debug(msg): # for debug messages
    if DEBUG == True:
        print "%s{>} %s%s" %(YELLOW, msg, CLEAR)
    else:
        pass

def pubkey_to_fingerprint(pubkey): # done
    # converts pubkey in ssh-rsa BASE64SHIT to fingerprint
    try:
        msg_debug("Creating SSH key fingerprint")
        ssh = SSHKey(pubkey)
        fingerprint = ssh.hash()
        return fingerprint
    except Exception, e:
        msg_debug(e)
        msg_fail("ssh fingerprint generation failed.")
    
def grab_pubkey(host, port, tor=False): # done
    # connect to a remote host/port and get a ssh public key
    try:
        msg_debug("Creating socket()")
        if tor == False:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            msg_debug("Using Tor, so using a socks socket thing")
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
            s = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception, e:
        msg_debug(e)
        return msg_fail("Failed to create socket!")  
    try:
        msg_status("Connecting to %s:%s" %(host, port))
        s.connect((host, int(port)))
    except Exception, e:
        msg_debug(e)
        return msg_fail("Failed to connect!")
    try:
        msg_debug("Creating SSH client")
        trans = paramiko.Transport(s)
        trans.start_client()
    except Exception, e:
        msg_debug(e)
        return msg_fail("Failed to start SSH client")
    try:
        msg_status("Connected... Grabbing SSH key now")
        binary_key = trans.get_remote_server_key()
    except Exception, e:
        msg_debug(e)
        return msg_fail("Grabbing SSH key failure!")
    # the next 3 lines are bad and I should feel bad. fuck ssh.
    pubkey_data = base64.encodestring(binary_key.__str__()).replace('\n', '')
    pubkey_type = binary_key.get_name()
    pubkey = "%s %s" %(pubkey_type, pubkey_data)
    return pubkey
    
def remote_query(host, port, tor=False): # done
    pubkey = grab_pubkey(host, port, tor)
    fingerprint = pubkey_to_fingerprint(pubkey)
    msg_info("SSH Fingerprint: %s" %(fingerprint))
    do_shodan(fingerprint)

def list_query(hosts, tor=False):
    pass

def local_query(keyfile): # done
    msg_status("Running query using %s" %(keyfile))
    try:
        msg_debug("Opening file for reading...")
        f = open(keyfile, "rb")
    except Exception, e:
        msg_debug(e)
        return msg_fail("File open failed.")
    try:
        pubkey = f.read()
    except Exception, e:
        msg_debug(e)
        return msg_fail("File read failed.")
    fingerprint = pubkey_to_fingerprint(pubkey)
    msg_info("SSH Fingerprint: %s" %(fingerprint))
    do_shodan(fingerprint)

def do_shodan(fingerprint): 
    # run shodan query.
    try:
        api = shodan.Shodan(SHODAN_API_KEY)
    except Exception, e:
        msg_debug(e)
        return msg_fail("Shodan API (Key?) failed.")
    try:
        msg_status("Querying Shodan now...")
        results = api.search(fingerprint)
    except Exception, e:
        msg_debug(e)
        return msg_fail("Shodan query failure :(")
    try:
        msg_success("Hits Found: %s" %(results['total']))
        msg_info("Printing IP's now...")
        for result in results['matches']:
            print result['ip_str']
    except Exception, e:
        msg_debug(e)
        return msg_fail("Some fucking shit broke.")

def main():
    # args: -f (file), -i (ip), -p (port)
    parser = argparse.ArgumentParser("ssh public key scanner")
    parser.add_argument("-f", help="SSH PublicKey file")
    parser.add_argument("-i", help="Target IP/Host")
    parser.add_argument("-p", help="Target Port (default is 22)", default=22)
    parser.add_argument("-t", action="store_true", help="Use Tor for the SSH key grab (for hidden services, etc!)")
    args = parser.parse_args()
    if args.f:
        local_query(keyfile=args.f)
    elif args.i:
        if args.t:
            remote_query(host=args.i, port=args.p, tor=True)
        else:
            remote_query(host=args.i, port=args.p)
    elif args.l:
        if args.t:
            list_query(hosts=args.l, tor=True)
        else:
            list_query(hosts=args.l)
    elif not args.f or args.i or args.l:
        parser.error("give me some arguments or get the fuck out")
    
if __name__ == "__main__":
    main()
