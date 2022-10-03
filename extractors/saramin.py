from requests import get
from bs4 import BeautifulSoup

def extract_saramin_jobs(keyword):
  headers={'User-Agent': 'Mozilla/5.0'}
  base_url = "https://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=recently&searchword="
  
  response = get(f"{base_url}{keyword}", headers=headers)

  if response.status_code != 200:
    print("Can't request website")
  else:
    results = []
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all('div', class_ = "item_recruit")
    for job_section in jobs:
      job_title = job_section.find('h2', class_ = "job_tit")
      condition = job_section.find('div', class_ = "job_condition")
      area_corp = job_section.find('div', class_ = "area_corp")
      anchor = job_title.find('a')
      title = anchor['title']
      location = condition.find('a')
      company = area_corp.find('a')
      link = anchor['href']
      
      job_data = {
        'link': f"https://www.saramin.co.kr{link}",
        'company':company.string.strip(),
        'location':location.string,
        'position':title,
      }
      
      if job_data['company'] != None:
        job_data['company'] = job_data['company'].replace(",", " ")
        
      if job_data['location'] != None:
        job_data['location'] = job_data['location'].replace(",", " ")
        
      if job_data['position'] != None:
        job_data['position'] = job_data['position'].replace(",", " ")
                    
      results.append(job_data)
      
    return results