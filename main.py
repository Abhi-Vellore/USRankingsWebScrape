from bs4 import BeautifulSoup
import requests
import csv
import re

csv_file = open('university_rankings.csv', 'w')
writer = csv.writer(csv_file)
url = 'https://www.usnews.com/best-colleges/rankings/national-universities'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    "Upgrade-Insecure-Requests": "1", "DNT": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate"}
result = requests.get(url, headers=headers)
src = result.content
# We use beautiful soup to parse the website
soup = BeautifulSoup(src, 'lxml')

internal_fields = [
    'School Type',
    'Year Founded',
    'Religious Affiliation',
    'Academic Calendar',
    'Setting',
    'Phone',
    'School Website'
]


def add_inner_info(link):
    url2 = 'https://www.usnews.com/best-colleges/' + link
    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 '
                      'Safari/537.36',
        "Upgrade-Insecure-Requests": "1", "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate"}
    result2 = requests.get(url2, headers=headers2)
    src2 = result2.content
    # Create an internal beautiful soup object to parse through this webpage
    soup2 = BeautifulSoup(src2, 'lxml')

    row.append(soup2.find('div', attrs={'class': "mb5"}).text)
    for field in internal_fields:
        element = soup2.find(text=field)
        parent = element.parent.parent
        if field == 'School Website':
            row.append(parent.a['href'] if parent.a else None)
        else:
            row.append(parent.find_all('p')[-1].text)


i = 0
for college in soup.find_all('a', attrs={'class': 'RankList__RankLink-sc-2xewen-3 jHTFDg has-badge'}):
    row = []
    name = soup.find_all('a', attrs={'class': 'Anchor-byh49a-0 DetailCardColleges__StyledAnchor-cecerc-8 PlBer efWQzA '
                                             'card-name'})
    row.append(int(re.findall('\d+', college.text)[0]))
    row.append(name[i].text)
    website = name[i].get('href')
    add_inner_info(website)
    i += 1
    writer.writerow(row)

