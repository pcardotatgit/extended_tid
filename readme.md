extended_tid

GSSO Automation Challenge - Extended_TID automatically download and format public Security Feeds for making them compliant with FMC Threat Intelligence Director expected Format

Reads the feedlist.txt files which contains all Feed's URL of Public Feeds you want to download. Plus instructions for parsing and output.
  We have put 4 examples of public feeds . Public feeds are parsed and rewritten.
  
Parsing results are stored into a directory named /output. Resulting files respect the FMC TID expected sources format.

A web server is started at the end of the parsing operation. This web server listens on the 8888 port.

INSTRUCTION FOR RUNNING THE APPLICATION

1- create a subdirectory named  /temp in the /extended_tid directory

2- run the application : python extended_tid.py

3- Type Enter for every feed. ( just here to see the progression and avoiding waiting minutes without any prompt )

4- Finally confirm the Web server starting

5- Check availability of feed from a web browser.  open http:// server_ip_address:8888

6- URL to re formatted feeds can be configured as flat file sources into FMC TID
