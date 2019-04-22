extended_tid

GSSO Automation Challenge - Extended_TID automatically download and format public Security Feeds for making them compliant with FMC Threat Intellgience Director expected Format

Reads the feedlist.txt files which contains all Feed's URL of Public Feeds you want to download. plus instruction for parsing and output.

Parsing results are stored into a directory named output.

A web server is started at the end of the parsing operation. This web server listens on the 8888 port.