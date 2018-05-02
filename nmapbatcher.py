#!/usr/bin/python

import os
import sys
import time
import netaddr
import argparse
import threading
import subprocess
import subprocess, signal

def nmap_run_output(line):

    if nmapargs.params2 is None:
        sys.stdout.write("Please Wait: Scanning " + line + "and writing results to " + nmapargs.output_file + "\n")

        command = subprocess.Popen(["nmap",
                                    "-" + nmapargs.params1,
                                    "-" + nmapargs.output,
                                    nmapargs.output_file,
                                    line], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        command_output = command.communicate()[0]
        sys.stdout.write(command_output)


    else:
        sys.stdout.write("Please Wait: Scanning " + line + "and writing results to " + nmapargs.output_file + "\n")

        command = subprocess.Popen(["nmap",
                                    "-" + nmapargs.params1,
                                    "-" + nmapargs.params2,
                                    "-" + nmapargs.output,
                                    nmapargs.output_file,
                                    line], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        command_output = command.communicate()[0]
        sys.stdout.write(command_output)

def nmap_run(line):

    if nmapargs.output == "console":
        if nmapargs.params2 is None:

            sys.stdout.write("Please Wait: Currently scanning " + line + '\n')
            command = subprocess.Popen(["nmap", 
                                        "-" + nmapargs.params1, 
                                        line], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            command_output = command.communicate()[0]
            sys.stdout.write(command_output)

        else:

            sys.stdout.write("Please Wait: Currently scanning " + line + '\n')
            command = subprocess.Popen(["nmap", 
                                        "-" + nmapargs.params1, 
                                        "-" + nmapargs.params2, 
                                        line], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            command_output = command.communicate()[0]
            sys.stdout.write(command_output)

    else:
        nmap_run_output(line)

if __name__ == "__main__":

    nmapscan = argparse.ArgumentParser(description="Nmap Batch Scanner")
    nmapscan.add_argument("-netrange", type=str, required=False, help="CIDR Block")
    nmapscan.add_argument("-ip", type=str, required=False, help="IP Address")
    nmapscan.add_argument("-target_file", type=str, required=False, help="Use CIDRS or IPs")
    nmapscan.add_argument("-params1", type=str, required=True, help="nmap parameters. ex. P0, sT, sV, etc")
    nmapscan.add_argument("-params2", type=str, required=False, help="secondary param. ex. sV, sT, etc")
    nmapscan.add_argument("-output", type=str, required=False, default="console", help="desired nmap output flag. default is to screen")
    nmapscan.add_argument("-output_file", type=str, required=False, default="results.txt", help="path of results.  default is results.txt")
    nmapscan.add_argument("-packet_rate", type=int, required=False, default=1, help="Packet rate")
    nmapargs = nmapscan.parse_args()

    if nmapargs.netrange is not None:
        for ip in netaddr.IPNetwork(nmapargs.netrange).iter_hosts():
            threads = [nmapargs.packet_rate]
            nmapthread = threading.Thread(target=nmap_run, args=(str(ip),))
            threads.append(nmapthread)
            nmapthread.start()

    elif nmapargs.ip is not None:
        nmap_run(nmapargs.ip)

    elif nmapargs.target_file is not None:
        with open(nmapargs.target_file, mode='r', buffering=1) as targets_file:
            targets = targets_file.readlines()
            for target in targets:
                for ip in netaddr.IPNetwork(target).iter_hosts():
                    threads = [nmapargs.packet_rate]
                    nmapthread = threading.Thread(target=nmap_run, args=(str(ip),))
                    threads.append(nmapthread)
                    nmapthread.start()

    else:
        sys.stdout.write("Please provide a target. check usage.  nmapbatcher.py -h \n")
    exit
