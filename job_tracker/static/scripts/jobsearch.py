import requests
from bs4 import BeautifulSoup

url = "https://www.simplyhired.ca/search?q=full+stack+developer&l=toronto%2C+ON"
base_url = 'https://www.simplyhired.ca'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='job-list')
job_elems = results.find_all('div', class_='SerpJob-jobCard')
# print(job_elems)

for job in job_elems:
    title_elem = job.find('a', class_='card-link')
    job_link = base_url + title_elem['href']
    title_text = title_elem.text
    company_elem = job.find('span', class_='jobposting-company').text
    location_elem = job.find('span', class_='jobposting-location').text
    description_elem = job.find('p', class_='jobposting-snippet').text
    print(title_text)
    print(job_link)
    print(company_elem)
    print(location_elem)
    print(description_elem)