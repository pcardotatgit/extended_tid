# coding: utf-8
import requests
import csv
import re
import http.server
#import cgitb

def read_csv(file):
	'''
	read URL FEEDS List
	'''
	donnees=[]
	with open (file) as csvfile:
		entries = csv.reader(csvfile, delimiter=';')
		for row in entries:
			#print (' print the all row  : ' + row)
			#print ( ' print only some columuns in the rows  : '+row[1]+ ' -> ' + row[2] )	
			row[1]=row[1].lower()	
			payload = {
				"url":row[0],
				"parser":row[1],
				"Type":row[2],
				"output":row[3],
			}			
			donnees.append(payload)
	return (donnees)
	
def read_all_lines_until_first_word_is(file,mot):
	# read the text file line by lines until the first string of the line is what the user has defined
	# si le string n'est pas trouve  toutes les lignes sont lues
	# la fin de fichier est détectée lorsque on lit 100 consecutives une ligne vide	
	fh = open(file, "r")
	line=''
	#txt  = fh.readline()
	stop=0
	nb_lignes_vides=0
	while( stop == 0 ):
		txt = fh.readline()
		ii=0
		#print(txt)
		if txt !='':
			stop=1
			while( ii < len(txt) ):
				#print (str(ii) + ' : ' + txt[ii] + ' - ')	
				line += txt[ii]				
				ii += 1
				i2=0
				while i2 < len(mot):
					#print (mot[i2])	
					if i2 < len(txt):						
						if txt[i2] != mot[i2]:
							stop=0
					i2 = i2+1
		else:
			#print ('empty line')
			nb_lignes_vides+=1
			if nb_lignes_vides > 100:
				stop=1
	fh.close()
	print("READ ALL LINES DONE")
	return(line)	

def parse_words(texte,filter):	
	#filtre=".*\\"+ filter+"\\s"  // pour se termine par le contenu de filter
	filtre=".*\\"+ filter
	selection = re.findall(filtre, texte)
	data=[]
	for s in selection:
		data.append(s.strip())
	return(data)
	
def parse(texte,a,mots1:list,mots2:list,start,end,parse_first_line,colomn:list,add_eol):
	#	a =	separator
	# 	colomn  =	colomns to keep  if colomn[0] =999 keep all colomns
	#	mots1 = 	list of words to find in the line we want to keep. if the first and only word in the list is 'ALLWORDS'
	# 	mots2 =	list of words to not find in the line we want to keep. if one wor is found then the line is not kept
	#	start 	=	if the line begins with with this word then start to keep lines  until the end word is found
	#	parse_first_line = 1 if we want to parse the first kept line  and = 0 if we don't want
	#	if add_eol = 1 then add end of Line after every line read, if =0 concatenate all line read together
	lignes = texte.split('\n')
	commencer=0
	output=""
	for ligne in lignes:
		if ligne.find(start) >= 0:
			commencer=1
			if parse_first_line ==1:
				i1=1
				while i1 != 0:		
					ligne=ligne.replace('  ',' ')
					if ligne.find("  ") >= 0:
						ligne=ligne.replace("  "," ")
						i1=1
					else :
						i1=0				
				tableau=ligne.split(a)
				i2=1
				for x in tableau:
					x=x.strip()
					if i2 in colomn:
						OK2=1
					else:
						OK2=0
					if colomn[0] == 999:
						OK2=1
					if x !='' and OK2:
						# REMPLACEMENT de CARACTERES DEBUT
						x=x.replace('"','')
						x=x.replace(',','')		
						# REMPLACEMENT de CARACTERES FIN		
						x = x + ';'
						#fa.write(x)
						#fa.write(';')
					i2=i2+1
				#print ("=====")	
				x = x + "\r\n"
				#print(x)
				output=output + x
				#fa.write('\n')				
		if ligne.find(end) >= 0:
			commencer=0
			x = x + "\r\n"
			output=output + x
			#fa.write('\n')
		if commencer:
			if mots1[0] != 'ALLWORDS':
				OK=0
				for x in mots1:
					if x in ligne:
						OK=1
			else:
				OK=1					
			for x in mots2:
				if x in ligne:
					OK=0	
			if OK:
				i1=1
				while i1 != 0:		
					ligne=ligne.replace('  ',' ')
					if ligne.find("  ") >= 0:
						ligne=ligne.replace("  "," ")
						i1=1
					else :
						i1=0				
				tableau=ligne.split(a)
				#i2=i2
				i2=1
				for x in tableau:
					x=x.strip()
					if i2 in colomn:
						OK2=1
					else:
						OK2=0
					if colomn[0] == 999:
						OK2=1
					if x !='' and OK2:
						# REMPLACEMENT de CARACTERES DEBUT
						x=x.replace('"','')
						x=x.replace(',','')
						# REMPLACEMENT de CARACTERES FIN
						x = x + ';'
						#print(x)
						if add_eol:
							x = x + "\r\n"
						output=output + x
						#fa.write(x)
						#fa.write(';')
					i2=i2+1
				#print ("=====")
				#fa.write('\n')	
	print("PARSING DONE")
	return(output)
	
def query(URL,index):
	counter = 0
	res = requests.get(URL)
	#if wee want to create several file
	#i=str(index)
	#fichier="./temp/feed_"+i+".txt"
	fichier="./temp/feed.txt"
	with open(fichier, "w") as file:
		for line in res.text.splitlines():
			counter += 1
			file.write(line+'\n')
			#print (line)
	return(1)


def main():	
	'''
	list=[]
	list=read_csv("feedlist.txt")
	for objet in list:
		print(objet)	
	'''
	# create a list of URL Feed to download
	FeedList = []
	FeedList=read_csv("feedlist.txt")

	# loop through all URLs in the list
	index=0
	for entry in FeedList:
		print("====>")
		print()
		print("Feed :")
		print(entry["url"])
		#download the feed into temp directory as feed.txt file
		query(entry["url"],index)
		index+=1	
		print()
		print()
		input('This Feed had been downloaded. Type [ Enter ] to parse it\n It may take a while. Wait until prompt comes back ! ')
		# Let s parse the file
		file_to_read="./temp/feed.txt"
		txt2=read_all_lines_until_first_word_is(file_to_read,'*****')
		save=0
		if entry["parser"]=="parser_1":
			print("PARSER 1")
			#configure the parser
			mots_ok=['.']
			mots_nok=['#']
			colonnes=[999,1]
			mot_debut_de_groupe = "Site"
			mot_fin_de_groupe = "*****"		
			#parse all lines into txt2 buffer
			result = parse(txt2,',',mots_ok,mots_nok,mot_debut_de_groupe,mot_fin_de_groupe,0,colonnes,1)
			save=1
		elif entry["parser"]=="parser_2":
			print("PARSER 2")
			#configure the parser
			mots_ok=['.']
			mots_nok=['#']
			colonnes=[999,1]
			mot_debut_de_groupe = "#########"
			mot_fin_de_groupe = "*****"		
			#parse all lines into txt2 buffer
			result = parse(txt2,',',mots_ok,mots_nok,mot_debut_de_groupe,mot_fin_de_groupe,0,colonnes,1)
			# result contains line separated by \r\n => save =1
			save=1	
		elif entry["parser"]=="parser_3":
			print("PARSER 3")
			#configure the parser
			mots_ok=['ALLWORDS']
			mots_nok=['#']
			colonnes=[999,]
			mot_debut_de_groupe = "#=comment"
			mot_fin_de_groupe = "********"		
			#parse all lines into txt2 buffer
			result0 = parse(txt2,'	',mots_ok,mots_nok,mot_debut_de_groupe,mot_fin_de_groupe,0,colonnes,1)
			# parse again the result in order to keep only domains ( words containing a dot '.' ) and deduplicate entries
			list_result=[]
			list_result=result0.split("\n");
			result=[]
			for mot in list_result:
				#print(mot)
				mot=mot.replace(";","")
				if mot.find(".") >= 0 and mot not in result:
					result.append(mot)
			#result is a list => save = 2
			save=2			
		elif entry["parser"]=="parser_4":
			print("PARSER 4")
			#configure the parser
			result = parse_words(txt2,".")	
			#result is a list => save = 2
			save=2	
		elif entry["parser"]=="parser_5":
			print("PARSER 5")
			#PARSER FOR  TOULOUSE URL & DOMAIN BLACK LIST
			#configure the parser
			mots_ok=['adult','agressif','arjel','malware','bitcoin','drogue','gambling','phishing']
			mots_nok=['#']
			colonnes=[999,1]
			mot_debut_de_groupe = "adult"
			mot_fin_de_groupe = "*****"		
			#parse all lines into txt2 buffer
			result0 = parse(txt2,';',mots_ok,mots_nok,mot_debut_de_groupe,mot_fin_de_groupe,0,colonnes,1)
			# parse again the result in order to keep only domains ( words containing a dot '.' ) and deduplicate entries
			list_result=[]
			list_result=result0.split("\n");
			result=[]
			for mot in list_result:				
				mot=mot.replace(";","")				
				if mot.find(".") >= 0:
					result.append(mot)	
					#print(mot)					
			#result is a list => save = 2
			save=2			
		else:
			#configure the parser  KEEP EVERY LINES
			print("DEFAUT PARSER PRINT ALL LINES")
			mots_ok=['ALLWORDS']
			mots_nok=['*****']
			colonnes=[999,1]
			mot_debut_de_groupe = ""
			mot_fin_de_groupe = "*****"		
			#parse all lines into txt2 buffer
			result = parse(txt2,',',mots_ok,mots_nok,mot_debut_de_groupe,mot_fin_de_groupe,0,colonnes,1)
			save=1	
		print()
		print('..... DONE => Goto Next Feed')
		print()
		#save the result		
		resulting_output="./output/"+entry["output"]
		fa = open(resulting_output, "w")		
		if save==1:		
			#some normalization before saving the result
			result=result.replace(";","")			
			lignes = result.split('\n')
			for ligne in lignes:
				if len(ligne) > 3:
					#print(ligne)
					ligne=ligne.replace("\r","")
					ligne=ligne.replace("\n","")	
					fa.write(ligne)
					fa.write("\n")
			fa.close()
		elif save==2:
			#save content of the result[]  list
			for url in result:
				#print(url)
				url=url.replace("\r","")
				url=url.replace("\n","")
				fa.write(url)
				fa.write("\n")
			fa.close()				
		
if __name__ == '__main__':
	main()
	print('===================>   ALL DONE  ! :-)')
	print()
	input('Type [ Enter ]  to Start the Web Server. When started Open your browser on http://localhost:8888')
	#cgitb.enable()
	 
	PORT = 8888
	server_address = ("localhost", PORT)

	server = http.server.HTTPServer
	handler = http.server.CGIHTTPRequestHandler
	'''
		if you are under windows :
		#handler.cgi_directories = ["/"] this will not work !!!
		BUT !!  handler.cgi_directories = ["/cgi"] will not work and all python executable files must be located in the sub directory

		handler.cgi_directories = ["./"] this will work for web content but not for CGI !!

		if you are under LINUX
		
		handler.cgi_directories = ["./"]  this will work
		
		This function define the sub directory into which all file will be executed and not only read
		
		If we don't sepecifye this cgi directory, the default will be the : cgi-bin  sub directory
	'''
	handler.cgi_directories = ["/cgi"]
	print("Starting on port :", PORT)
	print("Open your browser on http://localhost:8888")

	httpd = server(server_address, handler)
	httpd.serve_forever()	
