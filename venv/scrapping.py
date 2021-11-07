import requests
from bs4 import BeautifulSoup
import pandas as pd
from random import randint
from time import sleep


def extract(page):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    url = f'https://uk.indeed.com/jobs?q=java+developer&l=London%2C+Greater+London&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    job_divs = soup.find_all('a', class_='result')
    for job in job_divs:
        title = job.find('h2').text.strip()
        company = job.find('span', class_='companyName').text.strip()
        location = job.find('div', class_='companyLocation').text.strip()
        summary = job.find('div', class_='job-snippet').text.strip()
        linkFirst = 'https://uk.indeed.com'
        linkSecond = job['href']
        link = linkFirst + linkSecond
        try:
            salary = job.find('div', class_='salary-snippet').text.strip()
        except:
            salary = ''

        jobDictionary = {
            'title': title,
            'company': company,
            'salary': salary,
            'summary': summary,
            'location': location,
            'link': link
        }
        jobList.append(jobDictionary)
    return


jobList = []


def findMaxPage(soup):
    pageNumberSplit1 = soup.find(
        'div', {'id': 'searchCountPages'}).text.strip().split("of")
    pageNumberSplit2 = pageNumberSplit1[1].split(" ")
    pageNumberSplit3 = pageNumberSplit2[1].replace(',', '')
    pageNumberFinal = round(float(pageNumberSplit3)/15)
    return pageNumberFinal


a = extract(0)
# print(findMaxPage(a))
for i in range(0, findMaxPage(a), 10):
    c = extract(0)
    transform(c)
    sleep(randint(1, 20))

df = pd.json_normalize(jobList)

df.to_csv('results.csv')

# print(len(jobList))
