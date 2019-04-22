extended_tid

GSSO Automation Challenge - Extended_TID automatically download and format public Security Feeds for making them compliant with FMC Threat Intellgience Director expected Format

Reads the feedlist.txt files which contains all Feed's URL of Public Feeds you want to download. plus instruction for parsing and output.

Parsing results are stored into a directory named output.

A web server is started at the end of the parsing operation. This web server listens on the 8888 port.

INSTRUCTION FOR RUNNING THE APPLICATION

1- create a directory named  /temp in the extended_tid directory
2- run the application : python extended_tid.py
3- Type Enter for everyfeeds. ( just here to see the progression and avoiding waiting minutes without any prompt )
4- Finalle confirm the Web server starting
5- Check availability of feed from a web browser.  open http:// server_ip_address:8888
