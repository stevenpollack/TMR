# import libraries
import requests, re, csv
from bs4 import BeautifulSoup

url = "https://www.health.nsw.gov.au/news/Pages/2020-nsw-health.aspx"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

div = soup.find(id="cbqwpctl00_m_g_f2149fe4_b7d8_4713_96c6_995863b69f70")
a_tags = div.findChildren(name='a', string=re.compile('statistics'))
links = [a.get('href') for a in a_tags]

verbose = False
table = []

with open('nsw_stats.csv', 'w', newline='', encoding='utf-8') as csvfile:
  csvfile.flush()
  writer = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  
  for link in links:
    nsw_page = BeautifulSoup(requests.get(link).text, 'html.parser')
    pubdate = re.search('(2020)(\d\d)(\d\d)', link)
    pubdate = "-".join([pubdate.group(i) for i in [1,2,3]])
    pubdate = [link, pubdate]
    if verbose:
      print(pubdate)
      print(nsw_page.find('table', class_="moh-rteTable-6").find_all('tr')[1:])
    
    for row in nsw_page.find('table', class_="moh-rteTable-6").find_all('tr')[1:]:
      row_data = pubdate + [td.get_text().strip() for td in row.find_all('td')]
      table.append(row_data)
      writer.writerow(row_data)
    
  #writer.writerows(table)
print(table)
csvfile.close()