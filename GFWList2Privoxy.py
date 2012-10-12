#!/usr/bin/env python

import urllib2
import base64

PROXY = '127.0.0.1:7070'

def fetch_data_from_web():
	
	url = r'http://autoproxy-gfwlist.googlecode.com/svn/trunk/gfwlist.txt'
	print 'Fetching data from %s, it might take a few minutes, please wait...' % url
	
	base64Data = urllib2.urlopen(url).read()
	gfwData = base64.b64decode(base64Data)
	
	gfwtxt = open('gfwlist.txt', 'w')
	gfwtxt.write(gfwData)
	gfwtxt.close()
	
	return gfwData.split('\n')

def fetch_data_from_file():
	try:
		with open('gfwlist.txt', 'r+') as data:
			return data.read().split('\n')
	except IOError as e:
		print 'Please download gfwlist.txt first'
		return []

def parse_data(data):
	results = []
	exceptions = []
	
	print 'Starting to convert data...'
	
	results.append('{{+forward-override{{forward-socks5 {0} .}}}}'.format(PROXY))
	exceptions.append('{+forward-override{forward .}}')
	
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
		elif item.startswith('['):
			# do nothing
			pass
		else:
			index = item.find('.*')
			if index == -1:
				index = item.find('/')
				if index == -1:
					asterisk = item.find('*')
					dot = item.find('.')
					if asterisk == -1:
						if dot == -1:
							item = ':80/*' + item.replace(',', '\.')
						else:							
							results.append(':80/.*' + item.replace(',', '\.'))
							if not item.startswith('.'):
								item = '.' + item
							results.append(item + ':80')
							item = ''
					else:
						if dot == -1:
							item = ':80/' + item
						else:
							if dot < asterisk:
								item = item[0:asterisk] + '*:80*' + item[asterisk+1:]
							else:
								pass
				else:
					item = item[0:index] + ':80' + item[index:]
			else:
				item = item[0:index] + '*:80*' + item[index+2:]
			
			if item:
				results.append(item.replace('*', '.*'))
	
	return results + exceptions
	
def generate_data():
	data = fetch_data_from_web()
	if data:
		results = parse_data(data)
	
		if len(results) > 2:
			gfwfile = open('gfwlist.action', 'w')	
			for item in results:
				gfwfile.write("%s\n" % item)
			gfwfile.close()
			print 'Generating data done.'
		else:
			print 'No data generated.'
	else:
		print 'No data can be achieved to generate gfwlist.action'
	
if __name__ == '__main__':
	generate_data()
