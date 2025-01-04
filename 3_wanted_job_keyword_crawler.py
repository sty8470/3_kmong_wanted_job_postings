import requests
import time 
import random
import pandas as pd
import time
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

print()
job_keyword = input("검색하고자 하는 직무 키워드를 입력하세요: ")
print()

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Set up WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = f"https://www.wanted.co.kr/api/chaos/search/v1/position?query={job_keyword}&country=kr&years=-1&locations=all&sort=job.recommend_order&limit=1000&offset=0"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "priority": "u=1, i",
    "referer": "https://www.wanted.co.kr/search?query={job_keyword}&tab=position",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "wanted-user-agent": "user-web",
    "wanted-user-country": "KR",
    "wanted-user-language": "ko"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    job_data = response.json()['data']


jobs_list = []
counter = 1 
check_duplicates = set()

# 전체적인 페이지를 순회하면서, 필요한 부분을 파싱한다...
for data in job_data:

    detail_url = f'https://www.wanted.co.kr/wd/{data["id"]}'
    
    driver.get(detail_url)
    time.sleep(random.uniform(2, 2.8))

    # Triggering the more information dropdown if necessary
    try:
        more_dropdown_btn = driver.find_element(By.CLASS_NAME, "Button_Button__root__m1NGq.Button_Button__outlined__0HnEd.Button_Button__outlinedAssistive__JKDyz.Button_Button__outlinedSizeLarge__A_H8o.Button_Button__fullWidth__zAnDP")
        more_dropdown_btn.click()
        time.sleep(random.uniform(1.8, 2.2))
    except:
        pass

    objective_items = driver.find_elements(By.CLASS_NAME, "JobDescription_JobDescription__paragraph__Lhegj")

    # Extract job details with safety checks
    job_info = {
        "직무ID": data['id'],
        "직무": data['position'],
        "회사": data['company']['name']
    }

    # Check and add "주요업무"
    try:
        job_info["주요업무"] = [item.strip().replace('●', '').replace('■','').replace('•','').replace('*','').strip() for item in objective_items[0].text.split('\n')[1:]] if len(objective_items) > 0 else []
    except Exception as e:
        job_info["주요업무"] = []
        print(f"Error retrieving 주요업무: {e}")

    # Check and add "자격요건"
    try:
        job_info["자격요건"] = [item.strip().replace('●', '').replace('■','').replace('•','').replace('*','').strip()  for item in objective_items[1].text.split('\n')[1:]] if len(objective_items) > 1 else []
    except Exception as e:
        job_info["자격요건"] = []
        print(f"Error retrieving 자격요건: {e}")

    # Check and add "우대사항"
    try:
        job_info["우대사항"] = [item.strip().replace('●', '').replace('■','').replace('•','').replace('*','').strip()  for item in objective_items[2].text.split('\n')[1:]] if len(objective_items) > 2 else []
    except Exception as e:
        job_info["우대사항"] = []
        print(f"Error retrieving 우대사항: {e}")

    # Check and add "혜택 및 복지"
    try:
        job_info["혜택 및 복지"] = [item.strip().replace('●', '').replace('■','').replace('•','').replace('*','').strip()  for item in objective_items[3].text.split('\n')[1:]] if len(objective_items) > 3 else []
    except Exception as e:
        job_info["혜택 및 복지"] = []
        print(f"Error retrieving 혜택 및 복지: {e}")

    # Include reward information
    job_info["채용보상금"] = data['reward_total']

    print()
    print()
    print(f'{counter} / {len(job_data)}')
    print()
    print()
    print("처음 크롤링한 JD입니다: ")
    print()
    # Print job information to check
    print(job_info)
    print()
    jobs_list.append(job_info)
    counter += 1 

    time.sleep(3)

# Creating a DataFrame
df = pd.DataFrame(jobs_list)

# Saving the DataFrame to a CSV file
df.to_csv(f'원티드_{job_keyword}_직무상세정보.csv', index=False)

# Close the browser
driver.quit()