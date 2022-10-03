from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_page_count(keyword):
    options = Options()
    #options.add_argument("headless")
    
    base_url = "https://kr.indeed.com/jobs?q="
    url = f"{base_url}{keyword}"
    
    browser = webdriver.Chrome(executable_path='./chromedriver', options= options)
    browser.get(url)
    
    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("ul", class_ ="pagination-list")
    
    if pagination == None:
        return 1
    
    pages = pagination.find_all("li", recursive=False)
    count = len(pages)
    
    last_pagination = pages[count-1]
    
    # 10페이지 까지 탐색하도록 수정해야함
    if last_pagination.find("a", ['aria-label'] == "다음"): 
        return count
    else:
        return count
    
def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    print("Found", pages, "pages")
    results = []
    for page in range(pages):
        options = Options()
        #options.add_argument("headless")
        
        base_url = "https://kr.indeed.com/jobs"
        url = f"{base_url}?q={keyword}&start={page*10}"

        browser = webdriver.Chrome(executable_path='./chromedriver', options=options)
        print("Requesting", url)
        browser.get(url)
        
        # browser status code 있는지 확인
        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_ = "jobsearch-ResultsList")
        jobs = job_list.find_all('li', recursive=False)

        for job in jobs:
            #mosiac-zone에는 직업이 담겨있지않음
            zone = job.find("div", class_ = "mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find("span", class_ = "companyName")
                location = job.find("div", class_ = "companyLocation")
                job_data = {
                    'link' : f"https://kr.indeed.com{link}",
                    'company' : company.string,
                    'location' : location.string,
                    'position' : title
                }
                
                if job_data['company'] != None:
                    job_data['company'] = job_data['company'].replace(",", " ")
        
                if job_data['location'] != None:
                    job_data['location'] = job_data['location'].replace(",", " ")
        
                if job_data['position'] != None:
                    job_data['position'] = job_data['position'].replace(",", " ")
                    
                results.append(job_data)
                
    return results