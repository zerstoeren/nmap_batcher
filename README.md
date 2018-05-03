NMAP-Batcher - a multithreaded python nmap scanner to increase performance of nmap scanning
========

Nmap is one of the world's most well-known network scanning and fingerprinting tools in the industry, but one of the problems is speed.  I ran 3 tests to come to the conclusion that this was the best route to take.

Test Scenario:

A single /24 with at least 50 active devices (OpenStack VMs, IOT, Network Hardware, Server Hardware, etc).  The scanning machine is a Quad Core, 8GB RAM, 1TB performance SATA hard drive.  10/100 network with many devices over 802.11 b/g/n.

Timed Trial of 30 minute.  Results:

Test 1: nmap -sT x.x.x.x/24 

Result:  CTRL-C did not finish

real	34m58.332s
user	0m2.924s
sys	0m3.572s

Test 2: python script using the python nmap module - ./nmapmod.py -netrange x.x.x.x/24 -sT 

Result: Completed

real	1m51.183s
user	0m11.484s
sys	0m4.880s

Test 3: nmapbatcher.py -netrange x.x.x.x/24 -params1 -sT

Result: Completed

real    0m52.197s
user    0m1.435s
sys     0m0.993s

These trials were run 5 times with the results being similar each time.  Because nmapbatcher was faster in each run, I decided to use that as my source for continuing with this method for optimization.

Note:
--------------

Nmap-batcher currently has limited flexibility when compared to nmap itself, but I plan to increase flexibility, features, and flags as I have more time.

Currently, the "-output" flag defaults to the console and if you set a "-output" to oG, oX, etc, but forget to set a "-output_file" nikto-batcher will automatically write the file to a root path results.txt file.

Dependencies:
=============

nmap
python netaddr

Usage:
======

```bash
root@docker# ./nmapbatcher.py -ip x.x.x.x -params1 sT
root@docker# ./nmapbatcher.py -ip x.x.x.x -params1 sT -params2 sV -output oX
root@docker# ./nmapbatcher.py -netrange x.x.x.x/24 -params1 sT -output oG -output_file file.txt
root@docker# ./nmapbatcher.py -target_file targets.txt -params1 sV
```
  
Example
===

```bash
root@docker# ./nmapbatcher.py -ip x.x.x.x -params1 sT
root@docker# ./nmapbatcher.py -ip x.x.x.x -params1 sT -params2 sV -output oX
root@docker# ./nmapbatcher.py -netrange x.x.x.x/24 -params1 sT -output oG -output_file file.txt
root@docker# ./nmapbatcher.py -target_file targets.txt -params1 sV
```

Bugs
====


TODO
===

- increase flexibility and features to support nmap.

If you find other bugs that I haven't mentioned, please create a ticket, and I will get to it when I can.  

Help or improvement suggestions are also welcome.  Just create a ticket and I will get back to you as soon as I can.
Enjoy.
