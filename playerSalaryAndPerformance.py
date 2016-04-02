import requests
import csv
import time
import random

tablerows = [] ## this will eventually become the array that is transformed to CSV data
services = ['fd','dk','dd'] ## the abbreviation of which ever service(s) you'd like data for
## AVAILABLE SERVICES are fd (fanduel), dk (draftkings) dd (draftday), fle (fireleague elite), and fls (fireleague standard)

def getdata(): ## pulls data from rotoguru for everyweek of the NFL season for each service selected above. Pulled data fields are: [Week, Year, GID, Name, Pos, Team, h/a, Oppt, FD Points, FD Salary, Service]
	for service in services:
		week = 1 ## counter for each service
		while week < 18: ## limits pull to regular season
			print 'on week {0} of 17 for service {1} of {2}'.format(str(week), str(services.index(service) + 1 ), str(len(services))) ## prints current status of pull to end user
			time.sleep((.1 + random.random() * .15)) ## delays to lighten the load of script on website's server
			url = 'http://rotoguru1.com/cgi-bin/fyday.pl?week={0}&game={1}&scsv=1'.format(str(week), service)
			rawhtml = requests.get(url) ## loads webpage
			rawcontent = rawhtml.content ## gets html source code as text
			startkey = '<pre>' ## using search on html content as text instead of BeautifulSoup so that script can run without needing to install any additional libraries. I also had trouble grabbing the <pre></pre> text using bs4
			endkey = '</pre>'
			splittext = rawcontent[rawcontent.find(startkey) + len(startkey) : rawcontent.find(endkey)].splitlines() ## pulls out the pre-formatted text and makes each new row an entry in a list
			for row in splittext:
				newrow = row.split(';') ## pre-formatted text is semi-colon deliminated
				if len(tablerows) == 0: ## if it's the first line (i.e. table headers), adds a header for service
					newrow.append('Service')
				else:
					newrow.append(service)
				if newrow[0] == 'Week' and len(tablerows) > 0: ## skips adding a new row if it is a new row of table headers from loading a new page
					pass
				else:
					tablerows.append(newrow) ## adds the row of data to the larger table array
			week += 1


def ListToCSV(): ## writes the tablerows array to a CSV file. This function is just a slightly altered version of a popular script from stackoverflow
	filepath = '/Users/robertgreer/Dropbox/Python Codes/DFSpull/'
	filename = 'ALL{0}DFSdata.csv'.format(str(time.strftime("%Y%m%d")))
	with open(filepath + filename, "wb") as f:
		writer = csv.writer(f)
		writer.writerows(tablerows)

def main():
	getdata()
	ListToCSV()

if __name__ == '__main__':
	main()
