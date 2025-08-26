# crawler/crawler.py

import requests
from bs4 import BeautifulSoup
import csv
from datetime import date
import re

def get_article_details(article_url):
    """
    개별 뉴스 기사 페이지에서 뉴스사, 기자 이름, 기사 본문을 추출하는 함수
    """
    try:
        response = requests.get(article_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')

        # 뉴스사 추출
        agency_tag = soup.select_one('a.media_end_head_top_logo img')
        agency = agency_tag['alt'] if agency_tag and 'alt' in agency_tag.attrs else "No Agency"

        # 기자 이름 추출 (기자가 여러 명일 수 있으므로 모두 찾아서 합칩니다)
        reporter_tags = soup.select('em.media_end_head_journalist_name')
        reporters = ", ".join([tag.get_text(strip=True) for tag in reporter_tags])
        if not reporters:
            reporters = "No Reporter"

        # 기사 본문 추출
        content_area = soup.select_one('#dic_area')
        if content_area:
            # 불필요한 태그 제거 (테이블, 이미지 캡션 등)
            for br in content_area.find_all('br'):
                br.replace_with('\n')
            
            # 본문 내의 스팬 태그 제거 (번역 기능 등)
            for span in content_area.find_all('span'):
                span.unwrap()

            # 본문 텍스트 가져오기
            content_text = content_area.get_text(strip=True, separator='\n')
            
            # 괄호 안의 문자 제거 (예: [헤럴드경제(워싱턴DC)=서영상 기자·문혜현 기자])
            content_text = re.sub(r'\[.*?\]', '', content_text)
            
            # 문장 앞에 나오는 공백 제거
            content_text = re.sub(r'^\s+', '', content_text, flags=re.MULTILINE)
        else:
            content_text = "No Content"

        return agency, reporters, content_text.strip()

    except Exception as e:
        print(f"Error fetching article details from {article_url}: {e}")
        return "No Agency", "No Reporter", "No Content"

def crawl_news_articles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 모든 기사 아이템을 담고 있는 리스트를 찾습니다.
    article_list = soup.select('li.sa_item._SECTION_HEADLINE')
    
    news_data = []
    
    for index, article in enumerate(article_list):
        try:
            title_tag = article.select_one('strong.sa_text_strong')
            link_tag = article.select_one('a.sa_text_title')
            
            title = title_tag.get_text(strip=True) if title_tag else "No Title"
            link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "No Link"
            
            # **새로운 로직: 개별 기사 페이지에서 뉴스사, 기자, 본문 정보를 모두 가져옵니다.**
            news_agency, reporters, full_content = get_article_details(link)

            current_date = date.today().strftime('%Y-%m-%d')

            news_data.append({
                'index': index,
                'content': title,
                'link': link,
                'news_agency': news_agency,
                'reporters': reporters,
                'full_content': full_content,
                'date': current_date
            })
        except Exception as e:
            print(f"Error processing article at index {index}: {e}")
            continue

    return news_data

def crawl_multiple_sections(urls_dict):
    """
    딕셔너리 형태의 URL 목록을 받아 여러 섹션의 뉴스를 크롤링하는 함수
    """
    all_news_data = []
    
    for category, url in urls_dict.items():
        print(f"[{category}] 섹션의 뉴스를 크롤링합니다...")
        
        # 기존 함수를 사용하여 각 URL의 데이터를 가져옵니다.
        section_data = crawl_news_articles(url)
        
        # 각 뉴스 데이터에 'category' 필드를 추가합니다.
        for item in section_data:
            item['category'] = category
        
        all_news_data.extend(section_data)
        
    return all_news_data

def save_data_to_csv(data, filename='naver_news_articles.csv'):
    if not data:
        print("No data to save.")
        return
        
    # 첫 번째 데이터 항목의 키를 사용하여 CSV 헤더를 자동으로 생성합니다.
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Successfully saved data to {filename}")

if __name__ == "__main__":
    # 크롤링할 네이버 뉴스 섹션 URL을 딕셔너리로 정의합니다.
    naver_urls = {
        "정치": "https://news.naver.com/section/100",
        "경제": "https://news.naver.com/section/101",
        "사회": "https://news.naver.com/section/102",
        "생활/문화": "https://news.naver.com/section/103",
        "IT/과학": "https://news.naver.com/section/105",
        "세계": "https://news.naver.com/section/104",
        "오피니언": "https://news.naver.com/section/110"
    }
    
    # 1. 새로운 함수를 호출하여 여러 섹션의 데이터를 한 번에 가져옵니다.
    all_articles = crawl_multiple_sections(naver_urls)
    
    if all_articles:
        # 2. 모든 데이터를 하나의 CSV 파일로 저장합니다.
        save_data_to_csv(all_articles)
        print(f"총 {len(all_articles)}개의 기사를 하나의 CSV 파일로 저장했습니다.")
    else:
        print("크롤링할 기사가 없습니다. URL을 확인해 주세요.")