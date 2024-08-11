from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
driver = webdriver.Chrome(service= Service())

url = "https://www.koreabaseball.com/Player/Search.aspx"
driver.get(url)
teams = ['HT', 'LG', 'SS', 'OB', 'KT', 'SK', "NC", 'HH', 'LT', 'WO']  # 필요한 팀들의 value 값을 배열에 저장
team_mapping = {
    'KIA': "KIA",
    '삼성': 'SAMSUNG',
    '두산': 'DOOSAN',
    '한화': 'HANWHA',
    'LG': 'LG',
    'SSG': 'SSG',
    'NC': 'NC',
    'KT': 'KT',
    '롯데': 'LOTTE',
    '키움': 'KIWOOM',
    '고양' : 'KIWOOM'
}
try:
    time.sleep(2)

    with open('data.txt', 'w', encoding='utf-8') as file:
        # 각 팀에 대해 반복하며 데이터 추출
        for team in teams:
            # select 요소 다시 찾기
            select_element = driver.find_element(By.ID, 'cphContents_cphContents_cphContents_ddlTeam')
            select = Select(select_element)
            
            # 팀 선택
            select.select_by_value(team)
            
            # 선택 후 페이지 로드 대기
            time.sleep(2)
            
            # 페이지네이션 처리
            for page in range(1, 6):  # 1부터 5까지 반복
                # 페이지의 전체 HTML 가져오기
                page_source = driver.page_source
                
                # BeautifulSoup을 사용하여 HTML 파싱
                soup = BeautifulSoup(page_source, 'html.parser')
                
                # <tbody> 요소 찾기
                tbody = soup.find('tbody')
                
                # 각 <tr> 요소 내에서 첫 번째, 두 번째, 세 번째 <td> 텍스트 추출
                rows = tbody.find_all('tr')
                for row in rows:
                    tds = row.find_all('td')
                    if len(tds) >= 3:
                        first_td_text = tds[0].text.strip()
                        if not first_td_text:
                            continue                        
                        second_td_text = tds[1].text.strip()
                        third_td_text = tds[2].text.strip()
                        
                        # 파일에 데이터 작성
                        file.write(f"{first_td_text}, {second_td_text}, {team_mapping[third_td_text]}\n")
                
                # 다음 페이지로 이동
                if page < 5:  # 5페이지까지 반복하므로 마지막 페이지가 아닐 경우에만 클릭
                    next_page = driver.find_element(By.CSS_SELECTOR, 'a.on + a')
                    next_page.click()
                    
                    # 페이지 이동 후 대기
                    time.sleep(2)

finally:
    driver.quit()  # 브라우저 종료