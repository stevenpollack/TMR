# import libraries
import requests, re, csv
from bs4 import BeautifulSoup

# scrape the URLs to all health.NSW.gov.au press releases:
url = "https://www.health.nsw.gov.au/news/Pages/2020-nsw-health.aspx"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

div = soup.find(id="cbqwpctl00_m_g_f2149fe4_b7d8_4713_96c6_995863b69f70")
a_tags = div.findChildren(name='a', string=re.compile('statistics'))
links = [a.get('href') for a in a_tags]

verbose = False
table = []

# 1. search each URL for key phrases.
# 2. if we get any hits, save the <p> with the first relevant phrase, save the newsdate, and then save the url
# 3. write the results to a table

regexp = re.compile("""(Intensive Care Unit)|(ventilator)|(COVID-19 cases being treated by NSW Health)""", re.I)
relevant_ps = []
for link in links:
  link_text = requests.get(link).text
  html = BeautifulSoup(link_text, 'html.parser')
  p_tags = html.findAll('p', string=regexp)
  
  # break early
  if not p_tags:
    continue
  
  relevant_text = "".join([p_tag.get_text(strip=True) for p_tag in p_tags])

  newsdate = html.find('div', class_='newsdate').get_text(strip=True)

  table.append([link, newsdate, relevant_text])


with open('nsw_icu_stats.csv', 'w', newline='', encoding='utf-8') as csvfile:
  csvfile.flush()
  writer = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  writer.writerows(table)
  csvfile.close()
