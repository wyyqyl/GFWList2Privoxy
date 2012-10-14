#!/usr/bin/env python

import urllib2
import base64
import os.path
import time

# socks5
# PROXY = '{+forward-override{forward-socks5 127.0.0.1:7070 .}}'
# GoAgent
PROXY = '{+forward-override{forward 127.0.0.1:8087}}'

GFWLIST = 'gfwlist.txt'
GFWACTION = 'gfwlist.action'
SecondsInWeek = 7*24*60*60
 
def fetch_data_from_web():
	
	url = r'http://autoproxy-gfwlist.googlecode.com/svn/trunk/gfwlist.txt'
	print 'Fetching data from googlecode.com, it might take a few minutes, please wait...'
	
	try:
		base64Data = urllib2.urlopen(url).read()
		gfwData = base64.b64decode(base64Data)
		
		gfwtxt = open(GFWLIST, 'w')
		gfwtxt.write(gfwData)
		gfwtxt.close()
		
		return gfwData.split('\n')
	except urllib2.URLError as error:
		print 'Failed to fetch data from googlecode.com: %s' % error.reason

def fetch_data():
	try:
		fileTime = os.path.getmtime(GFWLIST)
		currentTime = time.time()
		if currentTime - fileTime > SecondsInWeek:
			return fetch_data_from_web()
		else:
			data = open(GFWLIST, 'r+')
			return data.read().split('\n')
	
	except os.error as error:
		print '%s is not found in the current folder' % GFWLIST
		return fetch_data_from_web()
		
def parse_data(data):
	results = []
	exceptions = []
	
	print 'Starting to convert data...'
	
	results.append(PROXY)
	exceptions.append('{+forward-override{forward .}}')
	
	line = 0
	data[0] = '!' + data
	for item in data:
		item = item.replace('%2F', '/')
		if len(item) == 0:
			results.append('')
		elif item.startswith('||'):
			results.append('.' + item[2:])
		elif item.startswith('|'):
			index = item.find('/', 9)
			if index == -1:
				index = len(item)
			if item[1:6] == 'https':
				results.append(item[9:index] + ':443' + item[index:])
			elif item[1:6] == 'http:':
				results.append(item[8:index] + ':80' + item[index:])
			else:
				pass
		elif item.startswith('!'):
			results.append('#' + item[1:])
		elif item.startswith('@@||'):
			index = item.find('/')
			if index == -1:
				index = len(item)
			exceptions.append('.' + item[4:index] + ':80' + item[index:])
		elif item.startswith('/^'):
			# do nothing for now
			pass
		elif item.startswith('/'):
			results.append(':80' + item)
		else:
			
			if item.startswith('http'):
				item = item[7:]
			
			index = item.find('.*')
			if index == -1:
				index = item.find('/')
				if index == -1:
					asterisk = item.find('*')
					dot = item.find('.')
					if asterisk == -1:
						if dot == -1:
							# freenet => :80/freenet
							item = ':80/*' + item
							results.append(item.replace('*', '.*'))
						else:
							# .0rz.tw => :80/.*.\.0rz\.tw
							# .0rz.tw => .0rz.tw:80
							results.append(':80/.*' + item.replace('.', '\.'))
							if not item.startswith('.'):
								item = '.' + item
							results.append(item + ':80')
					else:
						if dot == -1:
							# search*%E9%85%B7%E5%88%91 => :80/search.*%E9%85%B7%E5%88%91
							item = ':80/' + item
							results.append(item.replace('*', '.*'))
						else:
							if dot < asterisk:
								# zh.wikipedia.org*GFW => zh.wikipedia.org.:80/.*GFW
								item = item[0:asterisk] + '.:80/*' + item[asterisk+1:]
								results.append(item.replace('*', '.*'))
							else:
								# hk*.nextmedia.com => hk.*.nextmedia.com
								results.append(item)
								results.append(item.replace('*', '.*'))
				else:
					# .google.com/moderator => .google.com:80/moderator
					item = item[0:index] + ':80' + item[index:]
					results.append(item.replace('*', '.*'))
			else:
				# .google.*great*firewall => .google.:80/?.*great.*firewall
				# .google.*/search*%E9%94%A6%E6%B6%9B => .google.:80/?.*/search.*%E9%94%A6%E6%B6%9B
				item = item[0:index+1] + ':80/?*' + item[index+2:]
				results.append(item.replace('*', '.*'))
		line += 1
	
	return results + exceptions
	
def generate_data():
	
	data = fetch_data()
	if data:
		results = parse_data(data)
	
		if len(results) > 2:
			gfwfile = open(GFWACTION, 'w')
			for item in results:
				gfwfile.write("%s\n" % item)
			gfwfile.close()
			print 'Generating data done.'
		else:
			print 'No data generated.'
	else:
		print 'No data can be achieved to generate %s' % GFWACTION
	
if __name__ == '__main__':
	generate_data()
