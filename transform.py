# Vignan Reddy Thmmu
# CS - 418, Intro to Data Science 
# University of Illinois at Chicago 
import csv
import urllib.request
from bs4 import BeautifulSoup as bs

sourse = urllib.request.urlopen("https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions").read() #Extracting the data from the wikipidiea (https://stackoverflow.com/questions/15814625/scraping-wiki-page-in-beautiful-soup)
soup = bs(sourse, 'lxml')

tbody = soup('table', {"class": "wikitable sortable"})[1].find_all('tr')  #Extracting the superbowl table 


firstRow = tbody
x= 1

headersList= ["Game","Year","Winning team","Score","Losing team","Venue"]  #Getting the headers for the table 

#Creating lists to the save the data in it to get the appropriate format 
myList =  []
myList1 = []
myList2 = []
myList3 = []
myList4 = []
myList5 = []

for x in range(1,54):
	if 	firstRow[x].find_all('td')[4].find("span",{"class": "sorttext"}).text.rstrip('!') == "To be determined (TBD)":
		break;
	else:
		myList.append(firstRow[x].find('td').a.text)
		myList1.append(firstRow[x].find_all('td')[1].find("span",{"style": "white-space:nowrap"}).text.split(",")[1].strip())
		myList2.append(firstRow[x].find_all('td')[2].find("span",{"style": "display:none;"}).text.rstrip('!'))
		myList3.append(firstRow[x].find_all('td')[3].find("span",{"class": "sorttext"}).text)
		myList4.append(firstRow[x].find_all('td')[4].find("span",{"class": "sortkey"}).text.rstrip('!'))
		myList5.append(firstRow[x].find_all('td')[5].find("span",{"style": "display:none;"}).text.rstrip('!'))
			
myTable = [list(i) for i in zip(myList, myList1, myList2, myList3, myList4, myList5)]	

f = open('transformed.csv', 'w' , newline = '')
writer = csv.writer(f)
writer.writerow(headersList)
writer.writerows(myTable)


