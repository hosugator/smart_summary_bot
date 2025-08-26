# 파일 위치
# crawler/crawler.py

import requests
from bs4 import BeautifulSoup
import csv
from datetime import date

def crawl_news_articles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 모든 기사 아이템을 담고 있는 리스트를 찾습니다.
    # '.sa_item._SECTION_HEADLINE' 선택자를 사용하면 모든 기사 블록을 가져올 수 있습니다.
    article_list = soup.select('li.sa_item._SECTION_HEADLINE')
    
    news_data = []
    
    for index, article in enumerate(article_list):
        try:
            title_tag = article.select_one('strong.sa_text_strong')
            link_tag = article.select_one('a.sa_text_title')
            reporter_tag = article.select_one('div.sa_text_press')

            # 필요한 데이터 추출 및 오류 처리
            title = title_tag.get_text(strip=True) if title_tag else "No Title"
            link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "No Link"
            reporter = reporter_tag.get_text(strip=True) if reporter_tag else "No Reporter"
            
            # 날짜는 크롤링 시점의 날짜로 저장합니다.
            current_date = date.today().strftime('%Y-%m-%d')

            news_data.append({
                'index': index,
                'content': title,
                'link': link,
                'reporter': reporter,
                'date': current_date
            })
        except Exception as e:
            print(f"Error processing article at index {index}: {e}")
            continue

    return news_data

def save_data_to_csv(data, filename='naver_news_articles.csv'):
    if not data:
        print("No data to save.")
        return
        
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Successfully saved data to {filename}")

# if __name__ == '__main__':
#     url = "https://news.naver.com/section/100" # 정치 섹션 링크
#     articles = crawl_news_articles(url)
#     save_data_to_csv(articles)

# # 파일의 가장 아래에 다음 코드를 추가하세요.

if __name__ == "__main__":
    # 크롤링할 네이버 뉴스 섹션 URL을 지정합니다.
    # 예시: 정치 섹션
    naver_url = "https://news.naver.com/section/100"
    
    # 1. 크롤링 함수를 호출하여 데이터를 가져옵니다.
    print(f"[{naver_url}] 에서 뉴스 기사를 크롤링합니다...")
    news_articles = crawl_news_articles(naver_url)
    
    if news_articles:
        # 2. 크롤링된 데이터를 CSV 파일로 저장합니다.
        save_data_to_csv(news_articles)
        print("크롤링 및 CSV 저장이 완료되었습니다.")
    else:
        print("크롤링할 기사가 없습니다. URL을 확인해 주세요.")