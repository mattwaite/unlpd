from bs4 import BeautifulSoup
import urllib.request, re, csv

root_url = "https://scsapps.unl.edu/policereports/"

response = urllib.request.urlopen('https://scsapps.unl.edu/policereports/default.aspx')

soup = BeautifulSoup(response, 'html.parser')

uls = soup.find_all('ul')

links = uls[9].find_all('a')

with open('unlcrime.csv', 'a', encoding="utf-8") as csvfile:
    try: 
        for link in links:
            detail_url = link['href']
            report_url = root_url+detail_url
            detail = urllib.request.urlopen(report_url)
            detail_soup = BeautifulSoup(detail, 'html.parser')
            tds = detail_soup.find_all('td')
            inc = tds[3].text
            incident = inc.replace('Incident Number:', '').lstrip(' ')
            rep = tds[5].text
            reported = rep.replace('Date/Time Reported:', '').lstrip(' ')
            oc = tds[9].text
            occurred = oc.replace('Occurred Date:', '').lstrip(' ')
            building = tds[12].text
            address = tds[14].text
            campus = tds[16].text
            city = tds[18].text
            location_code = tds[20].text
            state = tds[22].text
            incident_code = tds[24].text
            synopsis = detail_soup.find(id=re.compile('.*_Synopsis$')).text
            synopsis = synopsis.replace('\n','').replace('\r','') 
            datawriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            datawriter.writerow([incident, reported, occurred, building, address, campus, city, state, location_code, incident_code, synopsis])    
    except:
        pass
