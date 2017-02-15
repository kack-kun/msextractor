#!/usr/bin/python
import sys
import urllib2
import re
import os
from bs4 import BeautifulSoup
from os.path import join


homepage = "http://mangastream.com"
directory = "http://mangastream.com/manga"
path = os.path.join(os.path.expandvars("%userprofile%"),"Desktop")

def url(url):
	return BeautifulSoup(urllib2.urlopen(url), 'html.parser')

def chkdir(chkdir = False,chkfile = False):
	if chkdir:
		chkdir = os.path.isdir(chkdir)
	if chkfile:
		chkfile = os.path.exists(chkfile)
	return [chkdir,chkfile]

def clean():
	try:
		os.system('cls')
	except:
		try:
			os.system('clear')
		except:
			print "Erro ao Limpar!"

def progress(count, total):
	bar_len = 40
	percent = float(count) / float(total)
	hashes = '#' * int(round(percent * bar_len))
	spaces = ' ' * (bar_len - len(hashes))
	sys.stdout.write("\rBaixando: [{0}] {1}% {2}/{3}".format(hashes + spaces, int(round(percent * 100)), int(count), int(total)))
	sys.stdout.flush()
			
def download(download_name,download_url,download_limit = False,download_current = False,downl = 0):
	if download_current is False:
		download_current = str(re.sub(r'[^\w]', '',str(download_url.split('/')[5])+str(download_url.split('/')[6])))
	if str(download_url.split('/')[6]) != "tip" and str(re.sub(r'[^\w]', '',str(download_url.split('/')[5])+str(download_url.split('/')[6]))) == download_current:
		download_name = re.sub(r'[^\w]', '', download_name)
		try:
			download_urls = url(download_url)
		except:
			print 'Falha ao baixar a Imagem!'
		else:
			pathh = "{0}".format(os.path.join(os.path.expandvars("%userprofile%"),"Desktop", download_name))
			if not os.path.exists(pathh):
				os.makedirs(pathh)
			if download_limit is False:
				download_limit = (re.search('Last\sPage\s\((.*?)\)', str(download_urls))).group(1)
			download_find = download_urls.find_all('div',attrs={'class': 'page'})
			download_search_next = str(re.search('<a href="(.*?)">', str(download_find)).group(1))
			download_search_img = str(re.search('src="(.*?)"/>', str(download_find)).group(1))
			
			progress(downl, download_limit)
			resource = urllib2.urlopen(download_search_img)
			nname = "{0}{1}".format((downl+1),os.path.splitext(os.path.basename(download_search_img))[1])
			try: 
				file = open(join(pathh, nname),'wb')
			except:
				print 'Falha ao criar a Pasta!'
			else:
				file.write(resource.read())
				file.close()
			download(download_name,download_search_next,download_limit,download_current,(downl+1))
			
	else:
		progress(downl, download_limit)
		print "\nFeito!\n"
		option = raw_input("Continuar?! [s our n] ")
	
		if option is "y":
			clean()
			intro()
		if option is "n":
			try:
				sys.exit()
			except:
				os.system('exit')
	
		
def intro():
	clean()
	intro = "MANGASTREAM (c) - MSextractor criado por kack-kun\n----------------------------------------------------------------------\n"
	try:
		realase_url = url(homepage)
	except:
		realase_final = 0x1
	else:
		realase_final = {}
		realase_n = 1
		for realase_item in realase_url.find_all('div',attrs={'class': 'col-sm-4'}):
			for realase_ul in realase_item.find_all('li'):
				realase_string = realase_ul.find_all("a")[0]
				realase_search = re.search('<i(.*?)/i>(\s?)', str(realase_string))
				realase_remove = re.sub('<i(.*?)/i>(\s?)', '', str(realase_string))
				
				realase_link = str(realase_string['href'])
				realase_categoria = re.search("</span>(.*)<strong>", realase_remove).group(1)
				realase_capitulo = re.search("<strong>(.*)</strong>", realase_remove).group(1)
				
				if realase_search is not None:
					realase_news = True
				else:
					realase_news = False
				realase_final[realase_n] = [realase_categoria+realase_capitulo,realase_link,realase_news]
				realase_n = int(realase_n) + int(1)
		realase = realase_final
	print intro
	n = 1
	for i in list(realase):
		if realase[i][2]:
			if n is 1:
				print 'Novos Capitulos:\n'
				n = int(n) + int(1)
			print '\t#'+str(i)+' '+realase[i][0]
		else:
			if n is 2:
				print '\nAntigos da Semana:\n'
				n = int(n) + int(1)
			print '#'+str(i)+' '+realase[i][0]
	print "\n----------------------------------------------------------------------\nEscolha usando seu numero como opcao para interagir\n\nO que deseja fazer...?"
	option = raw_input("#")
	if option:
		if option.isdigit():
			if realase[int(option)]:
				download(realase[int(option)][0],realase[int(option)][1])
			else:
				print 'Opcao nao existe!'
		else:
			print 'Em breve, quem sabe adiciono mais opcoes!'
	else:
		intro()

if chkdir(path)[0]:
	intro()
else:
	print "Pasta nao Existe!"
