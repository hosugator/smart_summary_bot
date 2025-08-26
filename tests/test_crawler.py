# tests/test_crawler.py
import pytest
import os
import csv
import requests_mock
from crawler.crawler import crawl_news_articles, crawl_multiple_sections, save_data_to_csv, get_reporter_and_agency
from datetime import date

# 테스트에 사용할 임시 파일 경로를 정의합니다.
TEST_CSV_PATH = "tests/test_output.csv"

# 테스트용 더미 HTML 응답을 정의합니다.
MOCK_HTML_POLITICS = """
<div id="newsct" class="newsct_wrapper">
    <div class="section_component">
        <ul id="_SECTION_HEADLINE_LIST" class="sa_list">
            <li class="sa_item _SECTION_HEADLINE">
                <div class="sa_text">
                    <a href="http://mock-url/pol1" class="sa_text_title"><strong class="sa_text_strong">정치 뉴스 제목 1</strong></a>
                    <div class="sa_text_info"></div>
                </div>
            </li>
            <li class="sa_item _SECTION_HEADLINE">
                <div class="sa_text">
                    <a href="http://mock-url/pol2" class="sa_text_title"><strong class="sa_text_strong">정치 뉴스 제목 2</strong></a>
                    <div class="sa_text_info"></div>
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
                    <div class="sa_text_info"></div>
                </div>
            </li>
        </ul>
    </div>
</div>
"""

# 개별 기사 페이지에 대한 더미 HTML 응답을 정의합니다.
MOCK_ARTICLE_HTML_POL_1 = """
<div class="media_end_head go_trans">
    <div class="media_end_head_top _LAZY_LOADING_WRAP">
        <a href="#" class="media_end_head_top_logo">
            <img alt="연합뉴스" class="media_end_head_top_logo_img" src="#">
        </a>
    </div>
    <div class="media_end_head_journalist">
        <button type="button" class="media_end_head_journalist_box">
            <em class="media_end_head_journalist_name">김정수 기자</em>
            <em class="media_end_head_journalist_name">최민지 기자</em>
        </button>
    </div>
</div>
"""

MOCK_ARTICLE_HTML_POL_2 = """
<div class="media_end_head go_trans">
    <div class="media_end_head_top _LAZY_LOADING_WRAP">
        <a href="#" class="media_end_head_top_logo">
            <img alt="헤럴드경제" class="media_end_head_top_logo_img" src="#">
        </a>
    </div>
    <div class="media_end_head_journalist">
        <button type="button" class="media_end_head_journalist_box">
            <em class="media_end_head_journalist_name">이진성 기자</em>
        </button>
    </div>
</div>
"""
# 경제 뉴스 기사 모의 데이터
MOCK_ARTICLE_HTML_ECO_1 = """
<div class="media_end_head go_trans">
    <div class="media_end_head_top _LAZY_LOADING_WRAP">
        <a href="#" class="media_end_head_top_logo">
            <img alt="매일경제" class="media_end_head_top_logo_img" src="#">
        </a>
    </div>
    <div class="media_end_head_journalist">
        <button type="button" class="media_end_head_journalist_box">
            <em class="media_end_head_journalist_name">박은정 기자</em>
        </button>
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
        # 뉴스 목록 페이지에 대한 모의 응답
        m.get("https://news.naver.com/section/100", text=MOCK_HTML_POLITICS)
        m.get("https://news.naver.com/section/101", text=MOCK_HTML_ECONOMY)
        
        # 개별 기사 페이지에 대한 모의 응답 (중요!)
        m.get("http://mock-url/pol1", text=MOCK_ARTICLE_HTML_POL_1)
        m.get("http://mock-url/pol2", text=MOCK_ARTICLE_HTML_POL_2)
        m.get("http://mock-url/eco1", text=MOCK_ARTICLE_HTML_ECO_1)

        # 테스트에 사용할 URL 딕셔너리를 정의합니다.
        test_urls = {
            "정치": "https://news.naver.com/section/100",
            "경제": "https://news.naver.com/section/101"
        }

        # 함수를 실행하여 결과를 가져옵니다.
        articles = crawl_multiple_sections(test_urls)

        # 1. 반환된 데이터의 총 개수가 올바른지 확인합니다. (정치 2개 + 경제 1개 = 총 3개)
        assert len(articles) == 3

        # 2. 각 기사에 'category', 'news_agency', 'reporters' 필드가 올바르게 포함되었는지 확인합니다.
        politics_articles = [a for a in articles if a['category'] == '정치']
        economy_articles = [a for a in articles if a['category'] == '경제']

        assert len(politics_articles) == 2
        assert len(economy_articles) == 1
        
        # 3. 데이터의 내용이 올바른지 검증합니다.
        assert politics_articles[0]['content'] == '정치 뉴스 제목 1'
        assert politics_articles[0]['news_agency'] == '연합뉴스'
        assert politics_articles[0]['reporters'] == '김정수 기자, 최민지 기자'
        
        assert economy_articles[0]['content'] == '경제 뉴스 제목 1'
        assert economy_articles[0]['news_agency'] == '매일경제'
        assert economy_articles[0]['reporters'] == '박은정 기자'


def test_save_data_to_csv_creates_file_with_new_fields():
    """
    수정된 CSV 저장 함수가 'news_agency'와 'reporters' 필드를 포함하여 파일을 생성하는지 테스트
    """
    dummy_data = [
        {'index': 0, 'content': '정치 뉴스', 'link': 'http://test.com/pol', 'news_agency': '연합뉴스', 'reporters': '김철수', 'date': date.today().strftime('%Y-%m-%d'), 'category': '정치'},
        {'index': 1, 'content': '경제 뉴스', 'link': 'http://test.com/eco', 'news_agency': '매일경제', 'reporters': '박영희', 'date': date.today().strftime('%Y-%m-%d'), 'category': '경제'}
    ]
    
    save_data_to_csv(dummy_data, TEST_CSV_PATH)
    
    assert os.path.exists(TEST_CSV_PATH)
    
    with open(TEST_CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        rows = list(reader)
        
    # 헤더에 'news_agency'와 'reporters' 필드가 포함되었는지 확인
    assert 'news_agency' in header
    assert 'reporters' in header
    assert rows[0]['news_agency'] == '연합뉴스'
    assert rows[0]['reporters'] == '김철수'
    assert rows[1]['news_agency'] == '매일경제'
    assert rows[1]['reporters'] == '박영희'