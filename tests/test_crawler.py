# tests/test_crawler.py
import pytest
import os
import csv
import requests_mock
from crawler.crawler import crawl_news_articles, crawl_multiple_sections, save_data_to_csv
from bs4 import BeautifulSoup
from datetime import date

# 테스트에 사용할 임시 파일 경로를 정의합니다.
TEST_CSV_PATH = "tests/test_output.csv"

# 테스트용 더미 HTML 응답을 정의합니다.
# 실제 네이버 뉴스 페이지의 HTML 구조와 유사하게 작성합니다.
MOCK_HTML_POLITICS = """
<div id="newsct" class="newsct_wrapper">
    <div class="section_component">
        <ul id="_SECTION_HEADLINE_LIST" class="sa_list">
            <li class="sa_item _SECTION_HEADLINE">
                <div class="sa_text">
                    <a href="http://mock-url/pol1" class="sa_text_title"><strong class="sa_text_strong">정치 뉴스 제목 1</strong></a>
                    <div class="sa_text_info"><div class="sa_text_info_left"><div class="sa_text_press">정치부 기자 A</div></div></div>
                </div>
            </li>
            <li class="sa_item _SECTION_HEADLINE">
                <div class="sa_text">
                    <a href="http://mock-url/pol2" class="sa_text_title"><strong class="sa_text_strong">정치 뉴스 제목 2</strong></a>
                    <div class="sa_text_info"><div class="sa_text_info_left"><div class="sa_text_press">정치부 기자 B</div></div></div>
                </div>
            </li>
        </ul>
    </div>
</div>
"""

MOCK_HTML_ECONOMY = """
<div id="newsct" class="newsct_wrapper">
    <div class="section_component">
        <ul id="_SECTION_HEADLINE_LIST" class="sa_list">
            <li class="sa_item _SECTION_HEADLINE">
                <div class="sa_text">
                    <a href="http://mock-url/eco1" class="sa_text_title"><strong class="sa_text_strong">경제 뉴스 제목 1</strong></a>
                    <div class="sa_text_info"><div class="sa_text_info_left"><div class="sa_text_press">경제부 기자 C</div></div></div>
                </div>
            </li>
        </ul>
    </div>
</div>
"""

MOCK_HTML_WORLD = """
<div id="newsct" class="newsct_wrapper">
    <div class="section_component">
        <ul id="_SECTION_HEADLINE_LIST" class="sa_list">
            <li class="sa_item _SECTION_HEADLINE">
                <div class="sa_text">
                    <a href="http://mock-url/world1" class="sa_text_title"><strong class="sa_text_strong">세계 뉴스 제목 1</strong></a>
                    <div class="sa_text_info"><div class="sa_text_info_left"><div class="sa_text_press">외신 기자 A</div></div></div>
                </div>
            </li>
            <li class="sa_item _SECTION_HEADLINE">
                <div class="sa_text">
                    <a href="http://mock-url/world2" class="sa_text_title"><strong class="sa_text_strong">세계 뉴스 제목 2</strong></a>
                    <div class="sa_text_info"><div class="sa_text_info_left"><div class="sa_text_press">외신 기자 B</div></div></div>
                </div>
            </li>
            <li class="sa_item _SECTION_HEADLINE">
                <div class="sa_text">
                    <a href="http://mock-url/world3" class="sa_text_title"><strong class="sa_text_strong">세계 뉴스 제목 3</strong></a>
                    <div class="sa_text_info"><div class="sa_text_info_left"><div class="sa_text_press">외신 기자 C</div></div></div>
                </div>
            </li>
        </ul>
    </div>
</div>
"""

MOCK_HTML_IT = """
<div id="newsct" class="newsct_wrapper">
    <div class="section_component">
        <ul id="_SECTION_HEADLINE_LIST" class="sa_list">
            <li class="sa_item _SECTION_HEADLINE">
                <div class="sa_text">
                    <a href="http://mock-url/it1" class="sa_text_title"><strong class="sa_text_strong">IT 뉴스 제목 1</strong></a>
                    <div class="sa_text_info"><div class="sa_text_info_left"><div class="sa_text_press">IT 기자 D</div></div></div>
                </div>
            </li>
        </ul>
    </div>
</div>
"""

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # 테스트가 끝난 후에 임시 파일을 삭제합니다.
    yield
    if os.path.exists(TEST_CSV_PATH):
        os.remove(TEST_CSV_PATH)

def test_crawl_multiple_sections_returns_correct_data():
    """
    여러 섹션의 뉴스를 크롤링하는 함수가 올바른 데이터를 반환하는지 테스트
    """
    with requests_mock.Mocker() as m:
        # 가짜 URL 응답을 설정합니다.
        m.get("https://news.naver.com/section/100", text=MOCK_HTML_POLITICS)
        m.get("https://news.naver.com/section/101", text=MOCK_HTML_ECONOMY)
        m.get("https://news.naver.com/section/105", text=MOCK_HTML_IT)
        m.get("https://news.naver.com/section/104", text=MOCK_HTML_WORLD)

        # 테스트에 사용할 URL 딕셔너리를 정의합니다.
        test_urls = {
            "정치": "https://news.naver.com/section/100",
            "경제": "https://news.naver.com/section/101",
            "IT/과학": "https://news.naver.com/section/105",
            "세계": "https://news.naver.com/section/104"
        }

        # 함수를 실행하여 결과를 가져옵니다.
        articles = crawl_multiple_sections(test_urls)

        # 1. 반환된 데이터의 총 개수가 올바른지 확인합니다. (정치 2개 + 경제 1개 + IT 1개 + 세계 3개 = 총 7개)
        assert len(articles) == 7

        # 2. 각 기사에 'category' 필드가 올바르게 추가되었는지 확인합니다.
        politics_articles = [a for a in articles if a['category'] == '정치']
        economy_articles = [a for a in articles if a['category'] == '경제']
        it_articles = [a for a in articles if a['category'] == 'IT/과학']
        world_articles = [a for a in articles if a['category'] == '세계']

        assert len(politics_articles) == 2
        assert len(economy_articles) == 1
        assert len(it_articles) == 1
        assert len(world_articles) == 3
        
        # 3. 데이터의 내용이 올바른지 일부를 검증합니다.
        assert politics_articles[0]['content'] == '정치 뉴스 제목 1'
        assert economy_articles[0]['content'] == '경제 뉴스 제목 1'
        assert it_articles[0]['content'] == 'IT 뉴스 제목 1'
        assert world_articles[0]['content'] == '세계 뉴스 제목 1'


def test_save_data_to_csv_creates_file_with_category():
    """
    수정된 CSV 저장 함수가 'category' 필드를 포함하여 파일을 생성하는지 테스트
    """
    dummy_data = [
        {'index': 0, 'content': '정치 뉴스', 'link': 'http://test.com/pol', 'reporter': '기자A', 'date': date.today().strftime('%Y-%m-%d'), 'category': '정치'},
        {'index': 1, 'content': '경제 뉴스', 'link': 'http://test.com/eco', 'reporter': '기자B', 'date': date.today().strftime('%Y-%m-%d'), 'category': '경제'}
    ]
    
    save_data_to_csv(dummy_data, TEST_CSV_PATH)
    
    assert os.path.exists(TEST_CSV_PATH)
    
    with open(TEST_CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        rows = list(reader)
        
    # 헤더에 'category' 필드가 포함되었는지 확인
    assert 'category' in header
    assert rows[0]['category'] == '정치'
    assert rows[1]['category'] == '경제'