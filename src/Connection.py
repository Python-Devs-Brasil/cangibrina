#!/usr/bin/python
#coding=utf-8

###########[PERIGO]#############
#Gambiarra fudida neste arquivo#
################################
#A gambiarra em questão é o fato de eu ter dado ctrl + c ctrl + v
#do código inteiro por causa de duas linhas.
#linha  47 e 52, linhas responsáveis por identificar o redirecionamento
#Caso haja redirecionamento vá para a linha 67

__AUTOR__	= "Fnkoc"

import sys
#sys.path.append("src/thirdparty/SocksiPy/")
#import socks
try:
	import mechanize
except:
	print"""
 [!] Please install Mechanize!

 Debian/Ubuntu => apt-get install python-mechanize
 Arch/Manjaro => pacman -S python2-mechanize
 Windows => see READEME.md"""

import urllib as u
import colors

global log
log = []

def redirect_tester(url, proxy, user_agent, verbose):
	'''====P.R.O.X.Y=========================================================='''

	if proxy:
		proxies = {"http": "http://" + proxy}		#Define endereço servidor proxy
	else:
		proxies = {}								#Para não utilizar proxy
		
	'''====A.G.E.N.T=========================================================='''

	try:
		if user_agent:
			br = mechanize.Browser()
			
			if proxy:									#Se argumento proxy estiver sendo utilizado
				br.set_proxies(proxies)					#Definir proxy
			
			UserAgent = "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0"
			header = {"User-Agent" : UserAgent}
			br.set_handle_robots(False)					#Nega ser um bot
			br.addheaders = [("User-agent", "Firefox")]	#Adiciona User-Agent
			conn = br.open(url)							#Abre url

			real = conn.geturl()						#Verifica redirecionamento
			conn = conn.code							#Verifica codigo HTTP			

		else:
			conn = u.urlopen(url, proxies=proxies).getcode()
			real = u.urlopen(url, proxies=proxies).geturl()	#Recebe a URL verdadeira

		if conn == 200:
			print(colors.green + " [+] " + colors.default + "Site is up\n code: %s\n") % (conn)

		elif conn == 403:
			print(colors.red + " [!] " + colors.default + "Forbidden: %s | %s |") % (url, conn)
			print(" Try to change your User-Agent (\"-a\")")
			sys.exit()

		elif conn == 404:
			if verbose:
				print(colors.red + " [-] " + colors.default + "HTTP Error 404: Not Found")

		else:
			print("Response Code: %s") % conn
	
		if real != url:										#Verifica se a URL especificada é a mesma que a recebida
			print(colors.red + " [!] " + colors.default + "Site is redirecting us to: \n")
			print(real)
			keep = raw_input("\nWould you like to follow the redirection?? [Y]es [N]o [A]bort\n >> ").lower()   #"lower" serve para converter a string
																												#de caps lock para caixa baixa ("A" ==> "a")
			if keep == "n":
				pass
			elif keep == "a":
				print(colors.red + " [!] " + colors.default + "Aborted\n")
				sys.exit()
			else:
				url = real
		else:
			pass

	except Exception, e:
		print e
		
		if verbose:
			print(colors.red + " [!] " + colors.default + str(e))
		sys.exit()


def tester(url, proxy, user_agent, verbose, saida):
	'''====P.R.O.X.Y=========================================================='''

	if proxy:
		proxies = {"http": "http://" + proxy}		#Define endereço servidor proxy
	else:
		proxies = {}								#Para não utilizar proxy
		
	'''====A.G.E.N.T=========================================================='''

	try:				
		if user_agent:
			br = mechanize.Browser()
			
			if proxy:									#Se argumento proxy estiver sendo utilizado
				br.set_proxies(proxies)					#Definir proxy
			
			UserAgent = "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0"
			header = {"User-Agent" : UserAgent}
			br.set_handle_robots(False)					#Nega ser um bot
			br.addheaders = [("User-agent", "Firefox")]	#Adiciona User-Agent
			conn = br.open(url)							#Abre url
			conn = conn.code							#Verifica codigo HTTP			

		else:
			conn = u.urlopen(url, proxies=proxies).getcode()

		if conn == 200:
			print(colors.green + " [+] " + colors.default + "Found: %s | %s |") % (url, conn)
			log.append(url)
			log.append(conn)

		elif conn == 301:
			print(colors.green + " [+] " + colors.default + "Redirecting: %s | %s |") % (url, conn)
		
		elif conn == 403:
			print(colors.red + " [!] " + colors.default + "Forbidden: %s | %s |") % (url, conn)
			print(" Try to change your User-Agent (\"-a\")")

		elif conn == 404:
			if verbose:
				print(colors.red + " [-] " + colors.default + "HTTP Error 404: Not Found")

		else:
			print(colors.red + " [!] " + colors.default + str(url))
			print("Response Code: %s") % conn

	except Exception, e:
		print e
		if verbose:
			print(colors.red + " [!] " + colors.default + str(e))
		pass

def result():
	for l in log:
		print colors.green + " [+] " + colors.default + str(l)
