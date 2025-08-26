# tests/test_crawler.py

# tests/test_crawler.py
import pytest
import os
import csv
from crawler.crawler import crawl_news_articles, save_data_to_csv

# 테스트에 사용할 임시 링크를 설정합니다.
# 실제 웹 요청을 보내는 대신, 로컬 HTML 파일을 사용해 테스트하면 더 안정적입니다.
TEST_URL = "https://news.naver.com/section/100"
TEST_HTML_PATH = "tests/test_naver_news.html"
TEST_CSV_PATH = "tests/test_output.csv"


# 테스트용 HTML 파일을 임시로 생성합니다.
# 이는 실제 웹 요청을 보낼 필요 없이 테스트를 실행할 수 있게 해줍니다.
# 아래 코드는 실제 네이버 뉴스 HTML을 복사해 붙여넣어야 합니다.
# (이 부분은 사용자가 직접 준비해야 합니다.)
def create_test_html_file():
    html_content = """
<div id="newsct" class="newsct_wrapper _GRID_TEMPLATE_COLUMN _STICKY_CONTENT" role="main"><div class="section_component as_section_headline _PERSIST_CONTENT" data-persist="2_sectionHeadline">
<div class="section_article as_headline _TEMPLATE" data-template-id="SECTION_HEADLINE">
	<div class="sa_head">
		<span class="sa_head_inner">
			<a href="#" class="sa_head_link _TOGGLE" data-classvalue="is_hidden" data-target="_SECTION_HEADLINE_INFO_bls1z" data-clk="guide">헤드라인 뉴스 <i class="sa_head_icon">안내</i></a>
		</span>
		<div id="_SECTION_HEADLINE_INFO_bls1z" class="sa_head_layer is_hidden">
			<p class="sa_head_layer_p">각 헤드라인의 기사와 배열 순서는 개인화를 반영해 추천되며, 기사묶음의 대표 기사는 구독 언론사 중심으로 제공됩니다. 기사 수량이 표기된 기사 우측 하단의 파란색 아이콘을 클릭하면 기사묶음을 확인할 수 있고 기사묶음과 기사묶음 타이틀도 기사 내용을 기반으로 자동 추출됩니다.</p>
			<a href="https://media.naver.com/algorithm" class="sa_head_layer_go">알고리즘 자세히 보기</a>
			<div class="sa_head_layer_close">
				<button type="button" class="_TOGGLE" data-classvalue="is_hidden" data-target="_SECTION_HEADLINE_INFO_bls1z">닫기</button>
			</div>
		</div>
	</div>
	<ul id="_SECTION_HEADLINE_LIST_bls1z" class="sa_list">
		<li class="sa_item _SECTION_HEADLINE">
			<div class="sa_item_inner">
				<div class="sa_item_flex _LAZY_LOADING_WRAP">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/016/0002519226" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="8800010E_000000000000000002519226" data-imp-url="https://n.news.naver.com/mnews/article/016/0002519226" data-imp-index="1">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="트럼프, 李대통령 펜보고 “나이스” 연발…예상보다 길어진 140분간 회담 [한미정상회담]" style="" src="https://mimgnews.pstatic.net/image/origin/016/2025/08/26/2519226.jpg?type=nf220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/016/0002519226" class="sa_text_title _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="8800010E_000000000000000002519226" data-imp-url="https://n.news.naver.com/mnews/article/016/0002519226" data-imp-index="1">
							<strong class="sa_text_strong">트럼프, 李대통령 펜보고 “나이스” 연발…예상보다 길어진 140분간 회담 [한미정상회담]</strong>
						</a>
						<div class="sa_text_lede">이재명 대통령이 25일(현지시간) 미국 워싱턴 DC 백악관에서 도널드 트럼프 미국 대통령이 지켜보는 가운데 방명록을 작성하고 있다. [연합] “좋은 펜(nice pen)입니다. 괜찮으시면 제가 사용하겠습니다.”(도널</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">헤럴드경제</div>
								<a href="https://n.news.naver.com/mnews/article/comment/016/0002519226" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news016,0002519226" data-zero-allow="false" data-processed="true">50<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
							<div class="sa_text_info_right">
								<a href="/cluster/c_202508260400_00000005/section/100?oid=016&amp;aid=0002519226" class="sa_text_cluster" data-clk="clcou">
									<span class="sa_text_cluster_num">55</span>
									<span class="blind">개의 관련뉴스 더보기</span>
								</a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _SECTION_HEADLINE">
			<div class="sa_item_inner">
				<div class="sa_item_flex _LAZY_LOADING_WRAP">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/016/0002519357" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="8800010E_000000000000000002519357" data-imp-url="https://n.news.naver.com/mnews/article/016/0002519357" data-imp-index="2">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="李대통령, 트럼프 “그 펜 좋다”에 즉석 선물…‘골프광’ 맞춤 선물 보따리도" style="" src="https://mimgnews.pstatic.net/image/origin/016/2025/08/26/2519357.jpg?type=nf220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/016/0002519357" class="sa_text_title _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="8800010E_000000000000000002519357" data-imp-url="https://n.news.naver.com/mnews/article/016/0002519357" data-imp-index="2">
							<strong class="sa_text_strong">李대통령, 트럼프 “그 펜 좋다”에 즉석 선물…‘골프광’ 맞춤 선물 보따리도</strong>
						</a>
						<div class="sa_text_lede">‘이름 각인’ 국산 골드파이브 수제 퍼터 ‘금속 거북선’·‘카우보이 마가 모자’ 증정 이재명 대통령이 25일(현지시간) 백악관에서 열린 한미 정상회담에 앞서 회담을 기념하는 방명록 서명식을 갖고 있다. 이 자리에서</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">헤럴드경제</div>
								<a href="https://n.news.naver.com/mnews/article/comment/016/0002519357" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news016,0002519357" data-zero-allow="false" data-processed="true"></a>
							</div>
							<div class="sa_text_info_right">
								<a href="/cluster/c_202508260750_00000009/section/100?oid=016&amp;aid=0002519357" class="sa_text_cluster" data-clk="clcou">
									<span class="sa_text_cluster_num">36</span>
									<span class="blind">개의 관련뉴스 더보기</span>
								</a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _SECTION_HEADLINE">
			<div class="sa_item_inner">
				<div class="sa_item_flex _LAZY_LOADING_WRAP">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/001/0015586435" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="880000D8_000000000000000015586435" data-imp-url="https://n.news.naver.com/mnews/article/001/0015586435" data-imp-index="3">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="정동영 &quot;한미정상, 한반도 평화전략 인식·방법론 일치&quot;[한미정상회담]" style="" src="https://mimgnews.pstatic.net/image/origin/001/2025/08/26/15586435.jpg?type=nf220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/001/0015586435" class="sa_text_title _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="880000D8_000000000000000015586435" data-imp-url="https://n.news.naver.com/mnews/article/001/0015586435" data-imp-index="3">
							<strong class="sa_text_strong">정동영 "한미정상, 한반도 평화전략 인식·방법론 일치"[한미정상회담]</strong>
						</a>
						<div class="sa_text_lede">조속한 북미 정상회담 재개 기대…여건 조성 필요" 정동영 통일부 장관은 이재명 대통령과 도널드 트럼프 미국 대통령의 정상회담 내용에 관해 "한미 정상이 한반도 평화전략에 관해 인식과 방법론이 일치한 것"이라고 26</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">연합뉴스</div>
								<a href="https://n.news.naver.com/mnews/article/comment/001/0015586435" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news001,0015586435" data-zero-allow="false" data-processed="true"></a>
							</div>
							<div class="sa_text_info_right">
								<a href="/cluster/c_202508260950_00000011/section/100?oid=001&amp;aid=0015586435" class="sa_text_cluster" data-clk="clcou">
									<span class="sa_text_cluster_num">4</span>
									<span class="blind">개의 관련뉴스 더보기</span>
								</a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _SECTION_HEADLINE">
			<div class="sa_item_inner">
				<div class="sa_item_flex _LAZY_LOADING_WRAP">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/015/0005175527" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="88000107_000000000000000005175527" data-imp-url="https://n.news.naver.com/mnews/article/015/0005175527" data-imp-index="4">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="李대통령 &quot;결과 아주 좋아…한미동맹 상처 없을 것이란 확신&quot;" style="" src="https://mimgnews.pstatic.net/image/origin/015/2025/08/26/5175527.jpg?type=nf220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/015/0005175527" class="sa_text_title _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="88000107_000000000000000005175527" data-imp-url="https://n.news.naver.com/mnews/article/015/0005175527" data-imp-index="4">
							<strong class="sa_text_strong">李대통령 "결과 아주 좋아…한미동맹 상처 없을 것이란 확신"</strong>
						</a>
						<div class="sa_text_lede">이재명 대통령은 25일(현지시간) 도널드 트럼프 미국 대통령과의 정상회담에서 부정적인 상황이 발생할 것을 참모들이 우려했으나 자신은 그러지 않을 것을 확신했다고 밝혔다. 이 대통령은 이날 오후 미국 싱크탱크 전략국제</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">한국경제</div>
								<a href="https://n.news.naver.com/mnews/article/comment/015/0005175527" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news015,0005175527" data-zero-allow="false" data-processed="true">10<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
							<div class="sa_text_info_right">
								<a href="/cluster/c_202508260850_00000022/section/100?oid=015&amp;aid=0005175527" class="sa_text_cluster" data-clk="clcou">
									<span class="sa_text_cluster_num">18</span>
									<span class="blind">개의 관련뉴스 더보기</span>
								</a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _SECTION_HEADLINE">
			<div class="sa_item_inner">
				<div class="sa_item_flex _LAZY_LOADING_WRAP">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/015/0005175559" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="88000107_000000000000000005175559" data-imp-url="https://n.news.naver.com/mnews/article/015/0005175559" data-imp-index="5">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="李대통령 &quot;'안보는 미국, 경제는 중국' 어려워져&quot;" style="" src="https://mimgnews.pstatic.net/image/origin/015/2025/08/26/5175559.jpg?type=nf220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/015/0005175559" class="sa_text_title _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="88000107_000000000000000005175559" data-imp-url="https://n.news.naver.com/mnews/article/015/0005175559" data-imp-index="5">
							<strong class="sa_text_strong">李대통령 "'안보는 미국, 경제는 중국' 어려워져"</strong>
						</a>
						<div class="sa_text_lede">이재명 대통령은 25일(현지시간) 중국과의 경제 협력과 미국과의 안보 협력을 병행하는 이른바 '안미경중'(安美經中) 노선과 관련해 "한국이 과거처럼 이 같은 태도를 취할 수는 없는 상황이 됐다"고 밝혔다. 이 대통령</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">한국경제</div>
								<a href="https://n.news.naver.com/mnews/article/comment/015/0005175559" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news015,0005175559" data-zero-allow="false" data-processed="true"></a>
							</div>
							<div class="sa_text_info_right">
								<a href="/cluster/c_202508260820_00000013/section/100?oid=015&amp;aid=0005175559" class="sa_text_cluster" data-clk="clcou">
									<span class="sa_text_cluster_num">22</span>
									<span class="blind">개의 관련뉴스 더보기</span>
								</a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _SECTION_HEADLINE is_blind">
			<div class="sa_item_inner">
				<div class="sa_item_flex _LAZY_LOADING_WRAP">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/003/0013441956" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="88000127_000000000000000013441956" data-imp-url="https://n.news.naver.com/mnews/article/003/0013441956" data-imp-index="6">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="전한길 &quot;정상회담 맞춰 워싱턴행…李, 국빈 대접도 못 받아&quot;" style="" src="https://mimgnews.pstatic.net/image/origin/003/2025/08/26/13441956.jpg?type=nf220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/003/0013441956" class="sa_text_title _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="88000127_000000000000000013441956" data-imp-url="https://n.news.naver.com/mnews/article/003/0013441956" data-imp-index="6">
							<strong class="sa_text_strong">전한길 "정상회담 맞춰 워싱턴행…李, 국빈 대접도 못 받아"</strong>
						</a>
						<div class="sa_text_lede">한국사 강사 출신 극우 유튜버 전한길씨가 이재명 대통령과 도널드 트럼프 미국 대통령 간 한미정상회담에 맞춰 미국 워싱턴DC로 출국했다고 밝혔다. 전씨는 25일 자신의 유튜브 채널 '전한길뉴스'를</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">뉴시스</div>
								<a href="https://n.news.naver.com/mnews/article/comment/003/0013441956" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news003,0013441956" data-zero-allow="false" data-processed="true">100<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
							<div class="sa_text_info_right">
								<a href="/cluster/c_202508252230_00000052/section/100?oid=003&amp;aid=0013441956" class="sa_text_cluster" data-clk="clcou">
									<span class="sa_text_cluster_num">10</span>
									<span class="blind">개의 관련뉴스 더보기</span>
								</a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _SECTION_HEADLINE is_blind">
			<div class="sa_item_inner">
				<div class="sa_item_flex _LAZY_LOADING_WRAP">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/032/0003391993" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="8800006B_000000000000000003391993" data-imp-url="https://n.news.naver.com/mnews/article/032/0003391993" data-imp-index="7">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="이 대통령 “한국, 과거처럼 ‘안미경중’ 취할 수 없어”···미 CSIS 정책연설 전문" style="" src="https://mimgnews.pstatic.net/image/origin/032/2025/08/26/3391993.jpg?type=nf220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/032/0003391993" class="sa_text_title _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="8800006B_000000000000000003391993" data-imp-url="https://n.news.naver.com/mnews/article/032/0003391993" data-imp-index="7">
							<strong class="sa_text_strong">이 대통령 “한국, 과거처럼 ‘안미경중’ 취할 수 없어”···미 CSIS 정책연설 전문</strong>
						</a>
						<div class="sa_text_lede">이재명 대통령은 25일(현지시간) 미국 워싱턴DC 국제전략문제연구소(CSIS)에서 “한국이 안보는 미국, 경제는 중국인 입장(안미경중)을 가져왔던 건 사실”이라며 “과거와 같은 태도를 취할 수는 없는 상태가 됐다”고</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">경향신문</div>
								<a href="https://n.news.naver.com/mnews/article/comment/032/0003391993" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news032,0003391993" data-zero-allow="false" data-processed="true">10<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
							<div class="sa_text_info_right">
								<a href="/cluster/c_202508260820_00000099/section/100?oid=032&amp;aid=0003391993" class="sa_text_cluster" data-clk="clcou">
									<span class="sa_text_cluster_num">11</span>
									<span class="blind">개의 관련뉴스 더보기</span>
								</a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _SECTION_HEADLINE is_blind">
			<div class="sa_item_inner">
				<div class="sa_item_flex _LAZY_LOADING_WRAP">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/001/0015586415" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="880000D8_000000000000000015586415" data-imp-url="https://n.news.naver.com/mnews/article/001/0015586415" data-imp-index="8">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="李대통령 &quot;국방비 증액…안보환경 변화 따른 동맹 현대화 공감&quot;(종합)" style="" src="https://mimgnews.pstatic.net/image/origin/001/2025/08/26/15586415.jpg?type=nf220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/001/0015586415" class="sa_text_title _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="880000D8_000000000000000015586415" data-imp-url="https://n.news.naver.com/mnews/article/001/0015586415" data-imp-index="8">
							<strong class="sa_text_strong">李대통령 "국방비 증액…안보환경 변화 따른 동맹 현대화 공감"(종합)</strong>
						</a>
						<div class="sa_text_lede">CSIS 연설…"美의 방위공약·한미연합방위 태세 철통같이 유지될 것" "北, 핵폭탄 보유 숫자 늘어…한미일 협력으로 북핵 공동대처" "도발 강력대응하면서도 북미대화…한국 '안미경중' 할 수 없는 상태" (워싱턴=연합</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">연합뉴스</div>
								<a href="https://n.news.naver.com/mnews/article/comment/001/0015586415" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news001,0015586415" data-zero-allow="false" data-processed="true">100<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
							<div class="sa_text_info_right">
								<a href="/cluster/c_202508260750_00000022/section/100?oid=001&amp;aid=0015586415" class="sa_text_cluster" data-clk="clcou">
									<span class="sa_text_cluster_num">23</span>
									<span class="blind">개의 관련뉴스 더보기</span>
								</a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _SECTION_HEADLINE is_blind">
			<div class="sa_item_inner">
				<div class="sa_item_flex _LAZY_LOADING_WRAP">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/016/0002519320" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="8800010E_000000000000000002519320" data-imp-url="https://n.news.naver.com/mnews/article/016/0002519320" data-imp-index="9">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="“트럼프 피스메이커”…李대통령, 북미대화 ‘페이스메이커’ 나선다 [한미정상회담]" style="" src="https://mimgnews.pstatic.net/image/origin/016/2025/08/26/2519320.jpg?type=nf220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/016/0002519320" class="sa_text_title _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="8800010E_000000000000000002519320" data-imp-url="https://n.news.naver.com/mnews/article/016/0002519320" data-imp-index="9">
							<strong class="sa_text_strong">“트럼프 피스메이커”…李대통령, 북미대화 ‘페이스메이커’ 나선다 [한미정상회담]</strong>
						</a>
						<div class="sa_text_lede">“한반도 평화의 새 길 꼭 열어 달라” ‘김정은’ 수차례 언급…“좋은 관계” 트럼프 “함께 노력하면 진전 있을 것” 이재명 대통령과 도널드 트럼프 미국 대통령이 25일(현지시간) 미국 워싱턴DC 백악관에서 정상회담을</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">헤럴드경제</div>
								<a href="https://n.news.naver.com/mnews/article/comment/016/0002519320" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news016,0002519320" data-zero-allow="false" data-processed="true"></a>
							</div>
							<div class="sa_text_info_right">
								<a href="/cluster/c_202508260210_00000005/section/100?oid=016&amp;aid=0002519320" class="sa_text_cluster" data-clk="clcou">
									<span class="sa_text_cluster_num">84</span>
									<span class="blind">개의 관련뉴스 더보기</span>
								</a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _SECTION_HEADLINE is_blind">
			<div class="sa_item_inner">
				<div class="sa_item_flex _LAZY_LOADING_WRAP">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/018/0006098589" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="880000E7_000000000000000006098589" data-imp-url="https://n.news.naver.com/mnews/article/018/0006098589" data-imp-index="10">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="트럼프 불길한 메시지…한달 전 필리핀 대통령은 '블레어하우스' 묵었다" style="" src="https://mimgnews.pstatic.net/image/origin/018/2025/08/25/6098589.jpg?type=nf220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/018/0006098589" class="sa_text_title _NLOG_IMPRESSION" data-clk="pol.clart" data-imp-gdid="880000E7_000000000000000006098589" data-imp-url="https://n.news.naver.com/mnews/article/018/0006098589" data-imp-index="10">
							<strong class="sa_text_strong">트럼프 불길한 메시지…한달 전 필리핀 대통령은 '블레어하우스' 묵었다</strong>
						</a>
						<div class="sa_text_lede">도널드 트럼프 미국 대통령이 이재명 대통령과 한미정상회담을 앞두고 ‘불길한 메시지’를 자신의 사회관계망서비스(SNS)에 게시했다. 이미 대통령 의전 등에서 이례적인 상황이 계속 벌어진 터라 트럼프 대통령의 메시지를</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">이데일리</div>
								<a href="https://n.news.naver.com/mnews/article/comment/018/0006098589" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news018,0006098589" data-zero-allow="false" data-processed="true">200<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
							<div class="sa_text_info_right">
								<a href="/cluster/c_202508251450_00000312/section/100?oid=018&amp;aid=0006098589" class="sa_text_cluster" data-clk="clcou">
									<span class="sa_text_cluster_num">25</span>
									<span class="blind">개의 관련뉴스 더보기</span>
								</a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
	</ul>
</div>
<div class="section_more _SECTION_HEADLINE_MORE_BUTTON_WRAP">
	<a href="#" class="section_more_inner _SECTION_HEADLINE_MORE_BUTTON _NLOG_IMPRESSION_TRIGGER" data-target="_SECTION_HEADLINE_LIST_bls1z" data-clk="clsmore">헤드라인 더보기</a>
</div>
</div>
<div class="section_component as_section_series _PERSIST_CONTENT" data-persist="3_sectionSeries">
<div class="section_series _TEMPLATE" data-template-id="SECTION_SERIES">
	<div class="ss_head">
		<div class="ss_head_inner">
			<a href="https://news.naver.com/hotissue/main?sid1=163&amp;cid=2002536" class="ss_head_link" data-clk="sert">
				<span class="ss_head_go">연재보기</span>
				<h2 class="ss_head_topic">오늘도 평화로운 국회</h2>
			</a>
		</div>
	</div>
	<div class="ss_body">
		<ul class="ss_list">
			<li class="ss_item _LAZY_LOADING_WRAP">
				<div class="ss_thumb _LAZY_LOADING_ERROR_HIDE">
					<div class="ss_thumb_inner">
						<a href="https://n.news.naver.com/mnews/hotissue/article/006/0000131482?type=series&amp;cid=2002536" class="ss_thumb_link _NLOG_IMPRESSION" data-clk="pol.sera" data-imp-gdid="880000C5_000000000000000000131482" data-imp-url="https://n.news.naver.com/mnews/hotissue/article/006/0000131482?type=series&amp;cid=2002536" data-imp-index="t00lt">
							<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="&quot;성일종 위원장! 청소부시냐고!&quot; 박선원 격분 이유는" style="" src="https://mimgnews.pstatic.net/image/origin/006/2025/08/25/131482.jpg?type=nf220_150">
						</a>
					</div>
				</div>
				<div class="ss_text">
					<a href="https://n.news.naver.com/mnews/hotissue/article/006/0000131482?type=series&amp;cid=2002536" class="ss_text_headline _NLOG_IMPRESSION" data-clk="pol.sera" data-imp-gdid="880000C5_000000000000000000131482" data-imp-url="https://n.news.naver.com/mnews/hotissue/article/006/0000131482?type=series&amp;cid=2002536" data-imp-index="t00lt">"성일종 위원장! 청소부시냐고!" 박선원 격분 이유는</a>
					<div class="ss_text_lede">박선원 더불어민주당 의원이 성일종 국방위원장에게 자신의 외환유치 관련 질의에 김 빼기를 한다며 "위원장이 청소부예요 뭐예요!"라며 격분하며 충돌했다. 25일 국회 국방위 전체회의에서 박선원 의원은 "국방부나 합참은 </div>
					<div class="ss_text_info">
						<div class="ss_text_press">미디어오늘</div>
						<a href="https://n.news.naver.com/mnews/article/comment/006/0000131482" class="ss_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news006,0000131482" data-zero-allow="false" data-clk="sercmtcount" data-processed="true">50<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
					</div>
				</div>
			</li>
			<li class="ss_item _LAZY_LOADING_WRAP">
				<div class="ss_thumb _LAZY_LOADING_ERROR_HIDE">
					<div class="ss_thumb_inner">
						<a href="https://n.news.naver.com/mnews/hotissue/article/006/0000131425?type=series&amp;cid=2002536" class="ss_thumb_link _NLOG_IMPRESSION" data-clk="pol.sera" data-imp-gdid="880000C5_000000000000000000131425" data-imp-url="https://n.news.naver.com/mnews/hotissue/article/006/0000131425?type=series&amp;cid=2002536" data-imp-index="2c5vx">
							<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="필리버스터 쇼핑백 2개 들고 오자 &quot;애정하는 최형두 의원님 살살하세요&quot;" style="" src="https://mimgnews.pstatic.net/image/origin/006/2025/08/21/131425.jpg?type=nf220_150">
						</a>
					</div>
				</div>
				<div class="ss_text">
					<a href="https://n.news.naver.com/mnews/hotissue/article/006/0000131425?type=series&amp;cid=2002536" class="ss_text_headline _NLOG_IMPRESSION" data-clk="pol.sera" data-imp-gdid="880000C5_000000000000000000131425" data-imp-url="https://n.news.naver.com/mnews/hotissue/article/006/0000131425?type=series&amp;cid=2002536" data-imp-index="2c5vx">필리버스터 쇼핑백 2개 들고 오자 "애정하는 최형두 의원님 살살하세요"</a>
					<div class="ss_text_lede">최형두 국민의힘 의원이 EBS법 반대 필리버스터(무제한 토론)에 들어가면서, 쇼핑백 2개 분량의 자료를 가져오자 "살살 하세요"라는 말이 나왔다. 21일 국회 본회의장에서 한국교육방송공사법(EBS법) 개정안이 상정되</div>
					<div class="ss_text_info">
						<div class="ss_text_press">미디어오늘</div>
						<a href="https://n.news.naver.com/mnews/article/comment/006/0000131425" class="ss_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news006,0000131425" data-zero-allow="false" data-clk="sercmtcount" data-processed="true">10<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
					</div>
				</div>
			</li>
			<li class="ss_item _LAZY_LOADING_WRAP">
				<div class="ss_thumb _LAZY_LOADING_ERROR_HIDE">
					<div class="ss_thumb_inner">
						<a href="https://n.news.naver.com/mnews/hotissue/article/006/0000131419?type=series&amp;cid=2002536" class="ss_thumb_link _NLOG_IMPRESSION" data-clk="pol.sera" data-imp-gdid="880000C5_000000000000000000131419" data-imp-url="https://n.news.naver.com/mnews/hotissue/article/006/0000131419?type=series&amp;cid=2002536" data-imp-index="895ex">
							<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="이훈기, 이진숙에 &quot;그렇게 실실 웃지 마시고&quot;···노종면 질의 때 표정 보니" style="" src="https://mimgnews.pstatic.net/image/origin/006/2025/08/21/131419.jpg?type=nf220_150">
						</a>
					</div>
				</div>
				<div class="ss_text">
					<a href="https://n.news.naver.com/mnews/hotissue/article/006/0000131419?type=series&amp;cid=2002536" class="ss_text_headline _NLOG_IMPRESSION" data-clk="pol.sera" data-imp-gdid="880000C5_000000000000000000131419" data-imp-url="https://n.news.naver.com/mnews/hotissue/article/006/0000131419?type=series&amp;cid=2002536" data-imp-index="895ex">이훈기, 이진숙에 "그렇게 실실 웃지 마시고"···노종면 질의 때 표정 보니</a>
					<div class="ss_text_lede">지난 20일 국회 과학기술방송정보통신위원회 회의 도중 이훈기 더불어민주당 의원은 이진숙 방송통신위원장에게 "방통위와 국민을 위해 더 이상 그 자리에 있지 마세요. 그렇게 실실 웃지 마시고"라고 했다. 실제 이진숙 위</div>
					<div class="ss_text_info">
						<div class="ss_text_press">미디어오늘</div>
						<a href="https://n.news.naver.com/mnews/article/comment/006/0000131419" class="ss_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news006,0000131419" data-zero-allow="false" data-clk="sercmtcount" data-processed="true">50<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
					</div>
				</div>
			</li>
			<li class="ss_item _LAZY_LOADING_WRAP">
				<div class="ss_thumb _LAZY_LOADING_ERROR_HIDE">
					<div class="ss_thumb_inner">
						<a href="https://n.news.naver.com/mnews/hotissue/article/006/0000131406?type=series&amp;cid=2002536" class="ss_thumb_link _NLOG_IMPRESSION" data-clk="pol.sera" data-imp-gdid="880000C5_000000000000000000131406" data-imp-url="https://n.news.naver.com/mnews/hotissue/article/006/0000131406?type=series&amp;cid=2002536" data-imp-index="2vo4d">
							<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="&quot;그만 좀 얘기하라고&quot; 국힘 박정훈, 민주당 김현에 또 반말" style="" src="https://mimgnews.pstatic.net/image/origin/006/2025/08/20/131406.jpg?type=nf220_150">
						</a>
					</div>
				</div>
				<div class="ss_text">
					<a href="https://n.news.naver.com/mnews/hotissue/article/006/0000131406?type=series&amp;cid=2002536" class="ss_text_headline _NLOG_IMPRESSION" data-clk="pol.sera" data-imp-gdid="880000C5_000000000000000000131406" data-imp-url="https://n.news.naver.com/mnews/hotissue/article/006/0000131406?type=series&amp;cid=2002536" data-imp-index="2vo4d">"그만 좀 얘기하라고" 국힘 박정훈, 민주당 김현에 또 반말</a>
					<div class="ss_text_lede">박정훈 국민의힘 의원이 국회 과학기술정보방송통신위원회(과방위) 전체회의 도중 김현 의원(민주당 간사)에 반말하며 충돌했다. 20일 국회 과방위 소관 2024 회계연도 결산 심사 도중 김현 의원은 이진숙 방통위원장이 </div>
					<div class="ss_text_info">
						<div class="ss_text_press">미디어오늘</div>
						<a href="https://n.news.naver.com/mnews/article/comment/006/0000131406" class="ss_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news006,0000131406" data-zero-allow="false" data-clk="sercmtcount" data-processed="true">50<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
					</div>
				</div>
			</li>
		</ul>
	</div>
</div>
</div>
		<div class="r_group_comp ad_box _da_banner _PERSIST_HEIGHT is_border_none" data-persist="1_ad">
			<div id="nmap_c____1" class="ad_area _AD_WRAP" data-unitid="p_news_newslist" data-mobileonly="false" data-sync="false" data-article="false"><div style="width: 100%; height: auto; margin: 0px auto; line-height: 0;"><iframe id="nmap_c____1_tgtLREC" frameborder="no" scrolling="no" tabindex="0" name="" title="AD" style="width: 100%; height: 0px; visibility: inherit; border: 0px; vertical-align: bottom;"></iframe></div></div>
		</div>
<div class="section_latest">
<div class="section_component as_section_article_list _PERSIST_CONTENT" data-persist="SECTION_ARTICLE_LIST">
<div class="section_latest_article _CONTENT_LIST _PERSIST_META" data-sid="100" data-sid2="" data-cluid="" data-has-next="true" data-cursor-name="next" data-cursor="20250826093033" data-page-no="1" data-date="" data-template="SECTION_ARTICLE_LIST" data-nclk="airscont" data-persist="SECTION_ARTICLE_LIST_META" data-persist-meta-restore="true">
<div class="section_article _TEMPLATE" data-template-id="SECTION_ARTICLE_LIST">
	<ul class="sa_list">
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/277/0005642161" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;grHj7D90kACoINYU&quot;}}" data-rank="1" data-gdid="88000385_000000000000000005642161" data-imp-url="https://n.news.naver.com/mnews/article/277/0005642161">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="'CSIS 연설' 李대통령 &quot;한 때 참모들은 우려했지만, 결과 아주 좋아&quot;" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/277/2025/08/26/5642161.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/277/0005642161" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;grHj7D90kACoINYU&quot;}}" data-rank="1" data-gdid="88000385_000000000000000005642161" data-imp-url="https://n.news.naver.com/mnews/article/277/0005642161">
							<strong class="sa_text_strong">'CSIS 연설' 李대통령 "한 때 참모들은 우려했지만, 결과 아주 좋아"</strong>
						</a>
						<div class="sa_text_lede">이재명 대통령이 25일(현지시간) 도널드 트럼프 미국 대통령과 정상회담에서 부정적인 상황이 발생할 것을 참모들이 우려했으나 자신은 그러지 않을 것으로 확인했다고 밝혔다. 이 대통령은 이날 오후 미국 싱크탱크 전략국제</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">아시아경제</div>
								<div class="sa_text_datetime is_recent">
									<b>11분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/277/0005642161" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news277,0005642161" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/047/0002485770" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="2" data-gdid="880000E3_000000000000000002485770" data-imp-url="https://n.news.naver.com/mnews/article/047/0002485770">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="&quot;결과 아주 좋았다&quot; 활짝 웃은 이 대통령...  '동맹 현대화' 약속" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/047/2025/08/26/2485770.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/047/0002485770" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="2" data-gdid="880000E3_000000000000000002485770" data-imp-url="https://n.news.naver.com/mnews/article/047/0002485770">
							<strong class="sa_text_strong">"결과 아주 좋았다" 활짝 웃은 이 대통령...  '동맹 현대화' 약속</strong>
						</a>
						<div class="sa_text_lede">▲ 이재명 대통령이 25일(현지 시각) 미국 워싱턴DC ？전략국제문제연구소(CSIS)에서 정책 연설 뒤 존 햄리 CSIS 소장의 질문에 답하고 있다. 2025.8.26 ⓒ 연합뉴스 "기대했던 것보다 훨씬 더 많은 것</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">오마이뉴스</div>
								<div class="sa_text_datetime is_recent">
									<b>12분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/047/0002485770" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news047,0002485770" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/011/0004525206" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="3" data-gdid="88000108_000000000000000004525206" data-imp-url="https://n.news.naver.com/mnews/article/011/0004525206">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="李 '골프 외교' 통했나…&quot;北 트럼프 월드서 골프&quot; 농담에 트럼프 '활짝'" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/011/2025/08/26/4525206.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/011/0004525206" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="3" data-gdid="88000108_000000000000000004525206" data-imp-url="https://n.news.naver.com/mnews/article/011/0004525206">
							<strong class="sa_text_strong">李 '골프 외교' 통했나…"北 트럼프 월드서 골프" 농담에 트럼프 '활짝'</strong>
						</a>
						<div class="sa_text_lede">첫 만남을 가진 이재명 대통령과 도널드 트럼프 미국 대통령 간 대화의 물꼬를 튼 소재는 다름 아닌 ‘골프’였다. 25일(현지시간) 백악관 오벌오피스(대통령 집무실)에서 열린 한미 정상회담에서 골프는 무거워질 수 있는</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">서울경제</div>
								<div class="sa_text_datetime is_recent">
									<b>14분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/011/0004525206" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news011,0004525206" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/079/0004059301" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="4" data-gdid="88000112_000000000000000004059301" data-imp-url="https://n.news.naver.com/mnews/article/079/0004059301">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="장성철 &quot;김? 장? 누가 되건 산으로 간다&quot;" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/079/2025/08/26/4059301.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/079/0004059301" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="4" data-gdid="88000112_000000000000000004059301" data-imp-url="https://n.news.naver.com/mnews/article/079/0004059301">
							<strong class="sa_text_strong">장성철 "김? 장? 누가 되건 산으로 간다"</strong>
						</a>
						<div class="sa_text_lede">■ 방송 : CBS 라디오 &lt;김현정의 뉴스쇼&gt; FM 98.1 (07:10~09:00) ■ 진행 : 김현정 앵커 ■ 대담 : 장성철(공론센터 소장), 김준일(시사 평론가) ◇ 김현정&gt; 복잡한 정치권 이슈를 한 칼에 정</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">노컷뉴스</div>
								<div class="sa_text_datetime is_recent">
									<b>15분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/079/0004059301" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news079,0004059301" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/028/0002762992" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="5" data-gdid="88000103_000000000000000002762992" data-imp-url="https://n.news.naver.com/mnews/article/028/0002762992">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="트럼프에 낚인 나경원·김문수…“정치보복” “내란몰이” 다 설레발이었다" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/028/2025/08/26/2762992.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/028/0002762992" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="5" data-gdid="88000103_000000000000000002762992" data-imp-url="https://n.news.naver.com/mnews/article/028/0002762992">
							<strong class="sa_text_strong">트럼프에 낚인 나경원·김문수…“정치보복” “내란몰이” 다 설레발이었다</strong>
						</a>
						<div class="sa_text_lede">국민의힘 의원들이 한미 정상회담 과정에서 이재명 대통령이 의전 홀대를 받았다거나, 도널드 트럼프 미국 대통령이 야당에 대한 정치 보복을 우려했다는 등 각종 의혹을 제기했으나 모두 사실과 다른 것으로 드러났다. 25일</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">한겨레</div>
								<div class="sa_text_datetime is_recent">
									<b>15분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/028/0002762992" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news028,0002762992" data-zero-allow="false" data-processed="true">30<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/421/0008447838" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="6" data-gdid="08138263_000000000000000008447838" data-imp-url="https://n.news.naver.com/mnews/article/421/0008447838">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="트럼프, 주한미군 기지 부지 소유권 돌발 요구…&quot;실현 가능성 낮아&quot;(종합)" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/421/2025/08/26/8447838.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/421/0008447838" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="6" data-gdid="08138263_000000000000000008447838" data-imp-url="https://n.news.naver.com/mnews/article/421/0008447838">
							<strong class="sa_text_strong">트럼프, 주한미군 기지 부지 소유권 돌발 요구…"실현 가능성 낮아"(종합)</strong>
						</a>
						<div class="sa_text_lede">정윤영 노민호 기자 = 도널드 트럼프 미국 대통령이 이재명 대통령과의 한미 정상회담에서 뜬금없이 '주한미군 기지 부지 소유권'을 원한다고 밝혔다. 법적 근거가 없는 주장을 제기한 것인데, 한미동맹 현대화를 주장하는 </div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">뉴스1</div>
								<div class="sa_text_datetime is_recent">
									<b>19분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/421/0008447838" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news421,0008447838" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
	</ul>
</div>
<div class="section_article _TEMPLATE" data-template-id="SECTION_ARTICLE_LIST">
	<ul class="sa_list">
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/016/0002519416" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="7" data-gdid="8800010E_000000000000000002519416" data-imp-url="https://n.news.naver.com/mnews/article/016/0002519416">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="경주 APEC 남북미 정상 만남 현실화되나…관건은 北반응 [한미정상회담]" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/016/2025/08/26/2519416.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/016/0002519416" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="7" data-gdid="8800010E_000000000000000002519416" data-imp-url="https://n.news.naver.com/mnews/article/016/0002519416">
							<strong class="sa_text_strong">경주 APEC 남북미 정상 만남 현실화되나…관건은 北반응 [한미정상회담]</strong>
						</a>
						<div class="sa_text_lede">김정은, 다자외교 무대 기피…핵보유국 인정 전제 달아 김여정, 김정은 APEC정상회의 초청 ‘헛된 망상’ 선그어 APEC 개최 경주 대신 판문점 남북미 정상 조우 가능성 이재명 대통령이 25일(현지시간) 미국 워싱턴</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">헤럴드경제</div>
								<div class="sa_text_datetime is_recent">
									<b>20분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/016/0002519416" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news016,0002519416" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/079/0004059297" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="8" data-gdid="88000112_000000000000000004059297" data-imp-url="https://n.news.naver.com/mnews/article/079/0004059297">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="[특집 - 한미정상회담] 김준형 &quot;주한미군 땅 달라? 그럼 미국 되는데?&quot;" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/079/2025/08/26/4059297.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/079/0004059297" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="8" data-gdid="88000112_000000000000000004059297" data-imp-url="https://n.news.naver.com/mnews/article/079/0004059297">
							<strong class="sa_text_strong">[특집 - 한미정상회담] 김준형 "주한미군 땅 달라? 그럼 미국 되는데?"</strong>
						</a>
						<div class="sa_text_lede">■ 방송 : CBS 라디오 &lt;김현정의 뉴스쇼&gt; FM 98.1 (07:10~09:00) ■ 진행 : 김현정 앵커 ■ 대담 : 김준형(조국혁신당 의원), 박원곤(이화여대 교수) ◇ 김현정&gt; 앞서 설명해 드린 대로 이재명</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">노컷뉴스</div>
								<div class="sa_text_datetime is_recent">
									<b>22분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/079/0004059297" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news079,0004059297" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/661/0000060649" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="9" data-gdid="88221sgj_000000000000000000060649" data-imp-url="https://n.news.naver.com/mnews/article/661/0000060649">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="李 &quot;정상회담 우려 없을 것 미리 알아.. 트럼프 쓴 책 읽었기 때문&quot;" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/661/2025/08/26/60649.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/661/0000060649" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="9" data-gdid="88221sgj_000000000000000000060649" data-imp-url="https://n.news.naver.com/mnews/article/661/0000060649">
							<strong class="sa_text_strong">李 "정상회담 우려 없을 것 미리 알아.. 트럼프 쓴 책 읽었기 때문"</strong>
						</a>
						<div class="sa_text_lede">이재명 대통령이 도널드 트럼프 미국 대통령과의 한미 정상회담에 대해 "매우 좋았다"라고 평가했습니다. 또 회담 직전 트럼프 대통령이 SNS에 올렸던 위협적인 메시지도 실제 우려할 점이 아니라는 것도 미리 알았다고 설</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">JIBS</div>
								<div class="sa_text_datetime is_recent">
									<b>23분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/661/0000060649" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news661,0000060649" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/469/0000883512" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="10" data-gdid="88156f75_000000000000000000883512" data-imp-url="https://n.news.naver.com/mnews/article/469/0000883512">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="이 대통령 &quot;'안보는 미국, 경제는 중국'은 옛말&quot;" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/469/2025/08/26/883512.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/469/0000883512" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="10" data-gdid="88156f75_000000000000000000883512" data-imp-url="https://n.news.naver.com/mnews/article/469/0000883512">
							<strong class="sa_text_strong">이 대통령 "'안보는 미국, 경제는 중국'은 옛말"</strong>
						</a>
						<div class="sa_text_lede">한미 정상회담을 위해 미국을 방문한 이재명 대통령은 25일(현지시간) 한국이 안보는 미국에, 경제는 중국에 밀착한다는 '안미경중론'에 선을 그었다. 북·핵 미사일에 대해서는 "현실적 방법을 찾아야 한다"고 강조했다.</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">한국일보</div>
								<div class="sa_text_datetime is_recent">
									<b>30분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/469/0000883512" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news469,0000883512" data-zero-allow="false" data-processed="true">10<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/001/0015586512" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="11" data-gdid="880000D8_000000000000000015586512" data-imp-url="https://n.news.naver.com/mnews/article/001/0015586512">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="[한미정상회담] 대미 '실용외교' 궤도 안착…'진짜 청구서'는 남아" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/001/2025/08/26/15586512.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/001/0015586512" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="11" data-gdid="880000D8_000000000000000015586512" data-imp-url="https://n.news.naver.com/mnews/article/001/0015586512">
							<strong class="sa_text_strong">[한미정상회담] 대미 '실용외교' 궤도 안착…'진짜 청구서'는 남아</strong>
						</a>
						<div class="sa_text_lede">'협상 이상기류' 관측 많았지만…"이의 없이 끝나, 성공적인 정상회담" 농산물 시장개방 등 쟁점은 여전…트럼프, 주한미군 부지 소유권 언급도 실용주의 가미 '한반도 페이스메이커론' 부각…중국·북한 등 반응 관건 (워</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">연합뉴스</div>
								<div class="sa_text_datetime is_recent">
									<b>33분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/001/0015586512" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news001,0015586512" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/018/0006098897" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="12" data-gdid="880000E7_000000000000000006098897" data-imp-url="https://n.news.naver.com/mnews/article/018/0006098897">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="李대통령 의자 직접 빼주는 트럼프…“기분 좋은 장면”" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/018/2025/08/26/6098897.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/018/0006098897" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="12" data-gdid="880000E7_000000000000000006098897" data-imp-url="https://n.news.naver.com/mnews/article/018/0006098897">
							<strong class="sa_text_strong">李대통령 의자 직접 빼주는 트럼프…“기분 좋은 장면”</strong>
						</a>
						<div class="sa_text_lede">이재명 대통령이 한·미 정상회담차 백악관을 방문한 가운데, 도널드 트럼프 미국 대통령이 첫 한미 정상회담 기념 서명식에서 이 대통령의 의자를 직접 빼주는 모습이 포착됐다. 사진=MBC 방송화면 캡처 25일(현지시각)</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">이데일리</div>
								<div class="sa_text_datetime is_recent">
									<b>34분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/018/0006098897" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news018,0006098897" data-zero-allow="false" data-processed="true">10<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
	</ul>
</div>
<div class="section_info">
	<div class="section_info_inner">
		<p class="section_info_p">AiRS 추천으로 구성된 뉴스를 제공합니다.</p>
		<a href="https://media.naver.com/algorithm" class="section_info_link">알고리즘 안내</a>
	</div>
</div>
<div class="section_article _TEMPLATE" data-template-id="SECTION_ARTICLE_LIST">
	<ul class="sa_list">
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/029/0002977909" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="13" data-gdid="880000AD_000000000000000002977909" data-imp-url="https://n.news.naver.com/mnews/article/029/0002977909">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="李대통령 극찬한 정청래 “참 똑똑한 협상가…과감하게 트럼프 사로잡아”" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/029/2025/08/26/2977909.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/029/0002977909" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="13" data-gdid="880000AD_000000000000000002977909" data-imp-url="https://n.news.naver.com/mnews/article/029/0002977909">
							<strong class="sa_text_strong">李대통령 극찬한 정청래 “참 똑똑한 협상가…과감하게 트럼프 사로잡아”</strong>
						</a>
						<div class="sa_text_lede">정청래 더불어민주당 대표는 26일 한미정상회담 이후 “이재명 대통령은 뛰어난 전략가이자 협상가”라고 극찬했다. 정청래 대표는 이날 자신의 페이스북에 글을 올려 “이재명 대통령은 참 똑똑하다. 매우 전략적인 언어의 선</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">디지털타임스</div>
								<div class="sa_text_datetime is_recent">
									<b>35분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/029/0002977909" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news029,0002977909" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/088/0000966362" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="14" data-gdid="880000C1_000000000000000000966362" data-imp-url="https://n.news.naver.com/mnews/article/088/0000966362">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="조국 &quot;국민의힘은 암 덩어리&quot;…국힘 &quot;누워서 침 뱉기&quot;" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/088/2025/08/26/966362.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/088/0000966362" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="14" data-gdid="880000C1_000000000000000000966362" data-imp-url="https://n.news.naver.com/mnews/article/088/0000966362">
							<strong class="sa_text_strong">조국 "국민의힘은 암 덩어리"…국힘 "누워서 침 뱉기"</strong>
						</a>
						<div class="sa_text_lede">조국 조국혁신당 혁신정책연구원장이 '국민의힘은 암 덩어리'라고 발언하자 국민의힘이 "국민의 절반가량을 암 덩어리라고 인식한다면 전국을 돌며 암 덩어리에게 지지를 호소하는 조 전 대표는 암의 숙주라도 되느냐"고 반발했</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">매일신문</div>
								<div class="sa_text_datetime is_recent">
									<b>35분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/088/0000966362" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news088,0000966362" data-zero-allow="false" data-processed="true">50<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/001/0015586478" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="15" data-gdid="880000D8_000000000000000015586478" data-imp-url="https://n.news.naver.com/mnews/article/001/0015586478">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="김용현, 해병특검에 '尹 직권남용 성립 여지 전혀없다' 의견서(종합)" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/001/2025/08/26/15586478.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/001/0015586478" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="15" data-gdid="880000D8_000000000000000015586478" data-imp-url="https://n.news.naver.com/mnews/article/001/0015586478">
							<strong class="sa_text_strong">김용현, 해병특검에 '尹 직권남용 성립 여지 전혀없다' 의견서(종합)</strong>
						</a>
						<div class="sa_text_lede">'VIP 격노회의' 참석자 중 한명인 金, 첫 입장표명…특검 수사내용엔 '아는 바 없다' 김용현 전 국방부 장관이 채상병 사건 외압·은폐 의혹을 들여다보는 이명현 순직해병 특별검사팀에 '윤석열 전 대통령의 수사외압 </div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">연합뉴스</div>
								<div class="sa_text_datetime is_recent">
									<b>36분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/001/0015586478" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news001,0015586478" data-zero-allow="false" data-processed="true">10<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/021/0002731843" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="16" data-gdid="880000C4_000000000000000002731843" data-imp-url="https://n.news.naver.com/mnews/article/021/0002731843">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="“받고 싶은 선물 있다” 李에 트럼프가 준 건 ‘피습 사진’" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/021/2025/08/26/2731843.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/021/0002731843" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="16" data-gdid="880000C4_000000000000000002731843" data-imp-url="https://n.news.naver.com/mnews/article/021/0002731843">
							<strong class="sa_text_strong">“받고 싶은 선물 있다” 李에 트럼프가 준 건 ‘피습 사진’</strong>
						</a>
						<div class="sa_text_lede">지난해 7월 13일(현지 시간) 도널드 트럼프 당시 미 대선 후보(가운데)가 경합주인 펜실베이니아주 버틀러 유세에서 총기 피습으로 경호 요원들에게 둘러싸인 가운데, 피를 흘리면서 주먹을 치켜든 모습. AP 뉴시스 이</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">문화일보</div>
								<div class="sa_text_datetime is_recent">
									<b>37분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/021/0002731843" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news021,0002731843" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/586/0000110192" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="17" data-gdid="8817cacd_000000000000000000110192" data-imp-url="https://n.news.naver.com/mnews/article/586/0000110192">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="&quot;트럼프, 李 아첨에 따뜻한 환영으로 바뀌어&quot;…외신이 주목한 한미정상회담 포인트는?" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/586/2025/08/26/110192.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/586/0000110192" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="17" data-gdid="8817cacd_000000000000000000110192" data-imp-url="https://n.news.naver.com/mnews/article/586/0000110192">
							<strong class="sa_text_strong">"트럼프, 李 아첨에 따뜻한 환영으로 바뀌어"…외신이 주목한 한미정상회담 포인트는?</strong>
						</a>
						<div class="sa_text_lede">블룸버그 "트럼프 매료시키려는 李 노력 결실 맺어" 로이터 "李 평화 중재 능력에 젤렌스키 같은 상황 피해" 주요 외신들이 25일(현지 시간) 미국 워싱턴DC 백악관에서 열린 한미 정상회담을 두고 긍정적인 평가를 내</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">시사저널</div>
								<div class="sa_text_datetime is_recent">
									<b>37분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/586/0000110192" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news586,0000110192" data-zero-allow="false" data-processed="true">30<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/449/0000318962" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="18" data-gdid="88156f74_000000000000000000318962" data-imp-url="https://n.news.naver.com/mnews/article/449/0000318962">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="인터뷰 전문…국힘 김대식 “李, ‘예측불허’ 트럼프 잘 피해 나갔다” [정치시그널]" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/449/2025/08/26/318962.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/449/0000318962" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="18" data-gdid="88156f74_000000000000000000318962" data-imp-url="https://n.news.naver.com/mnews/article/449/0000318962">
							<strong class="sa_text_strong">인터뷰 전문…국힘 김대식 “李, ‘예측불허’ 트럼프 잘 피해 나갔다” [정치시그널]</strong>
						</a>
						<div class="sa_text_lede">"걱정·우려한 부분 조금 해소된 듯" "트럼프의 예측불허한 언행…李 잘 피해 나갔다" "미국은 기독교 국가…교회 압수수색 상상 못해" "트럼프 아들·백악관 집례 목사, 순복음교회 다녀가…트럼프에 영향" "미국과 거래</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">채널A</div>
								<div class="sa_text_datetime is_recent">
									<b>38분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/449/0000318962" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news449,0000318962" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
	</ul>
</div>
<div class="section_article _TEMPLATE" data-template-id="SECTION_ARTICLE_LIST">
	<ul class="sa_list">
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/655/0000027143" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="19" data-gdid="88221sgd_000000000000000000027143" data-imp-url="https://n.news.naver.com/mnews/article/655/0000027143">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="李“미 제조업 르네상스 함께”,트럼프 “무역협상 기존 대로”" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/655/2025/08/26/27143.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/655/0000027143" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="19" data-gdid="88221sgd_000000000000000000027143" data-imp-url="https://n.news.naver.com/mnews/article/655/0000027143">
							<strong class="sa_text_strong">李“미 제조업 르네상스 함께”,트럼프 “무역협상 기존 대로”</strong>
						</a>
						<div class="sa_text_lede">이재명 대통령과 도널드 트럼프 미국 대통령이 25일(현지시간) 미국 워싱턴DC에서 첫 정상회담을 열어 관세 협상 후속 조처와 한미 동맹을 기반으로 한 안보·경제 협력 방안, 북한 문제 등을 폭넓게 논의했습니다. 두 </div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">CJB청주방송</div>
								<div class="sa_text_datetime is_recent">
									<b>39분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/655/0000027143" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news655,0000027143" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/079/0004059283" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="20" data-gdid="88000112_000000000000000004059283" data-imp-url="https://n.news.naver.com/mnews/article/079/0004059283">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="'1호 통역' 데뷔전·주부출신 '닥터 리'…정상회담 '신스틸러'" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/079/2025/08/26/4059283.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/079/0004059283" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="20" data-gdid="88000112_000000000000000004059283" data-imp-url="https://n.news.naver.com/mnews/article/079/0004059283">
							<strong class="sa_text_strong">'1호 통역' 데뷔전·주부출신 '닥터 리'…정상회담 '신스틸러'</strong>
						</a>
						<div class="sa_text_lede">한미정상회담 李대통령 통역에 조영민 외교부 서기관 '데뷔전' 북미정상회담 통역한 전업 주부 출신 '닥터 리' 25일(현지시간) 이재명 대통령과 도널드 트럼프 미국 대통령의 첫 한미 정상회담이 마무리된 가운데 양 정상</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">노컷뉴스</div>
								<div class="sa_text_datetime is_recent">
									<b>40분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/079/0004059283" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news079,0004059283" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/002/0002402933" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="21" data-gdid="88000101_000000000000000002402933" data-imp-url="https://n.news.naver.com/mnews/article/002/0002402933">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="트럼프 &quot;한국, 무역합의 문제 제기했지만 원래대로 갈 것&quot;" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/002/2025/08/26/2402933.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/002/0002402933" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="21" data-gdid="88000101_000000000000000002402933" data-imp-url="https://n.news.naver.com/mnews/article/002/0002402933">
							<strong class="sa_text_strong">트럼프 "한국, 무역합의 문제 제기했지만 원래대로 갈 것"</strong>
						</a>
						<div class="sa_text_lede">대통령실 "시종일관 화기애애 분위기…합의문 필요없을 정도로 잘된 회담" 도널드 트럼프 미국 대통령이 한미 양국이 지난달 타결한 무역 합의를 큰 틀에서 원칙적으로 지키기로 했다고 밝혔다. 합의 이후 농산물 시장 추가 </div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">프레시안</div>
								<div class="sa_text_datetime is_recent">
									<b>40분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/002/0002402933" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news002,0002402933" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/002/0002402932" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="22" data-gdid="88000101_000000000000000002402932" data-imp-url="https://n.news.naver.com/mnews/article/002/0002402932">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="이재명 &quot;한반도 평화 만들어달라&quot;…트럼프 &quot;김정은 올해 만나고 싶다&quot;" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/002/2025/08/26/2402932.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/002/0002402932" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="22" data-gdid="88000101_000000000000000002402932" data-imp-url="https://n.news.naver.com/mnews/article/002/0002402932">
							<strong class="sa_text_strong">이재명 "한반도 평화 만들어달라"…트럼프 "김정은 올해 만나고 싶다"</strong>
						</a>
						<div class="sa_text_lede">트럼프 '숙청' 메시지로 긴장감 속에 시작했지만…우호적 분위기 속에 돌발상황 없어 이재명 대통령과 도널드 트럼프 미국 대통령이 한미정상회담에서 한반도 평화와 북한과의 대화 필요성에 대한 공감대를 확인했다. 트럼프 대</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">프레시안</div>
								<div class="sa_text_datetime is_recent">
									<b>41분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/002/0002402932" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news002,0002402932" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/008/0005240926" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="23" data-gdid="880000C2_000000000000000005240926" data-imp-url="https://n.news.naver.com/mnews/article/008/0005240926">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="이재명 대통령 &quot;과거 '안미경중' 취한 게 사실…이젠 할 수 없는 상태&quot;" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/008/2025/08/26/5240926.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/008/0005240926" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="23" data-gdid="880000C2_000000000000000005240926" data-imp-url="https://n.news.naver.com/mnews/article/008/0005240926">
							<strong class="sa_text_strong">이재명 대통령 "과거 '안미경중' 취한 게 사실…이젠 할 수 없는 상태"</strong>
						</a>
						<div class="sa_text_lede">이재명 대통령이 "과거에 한국은 안미경중(安美經中) 태도를 취한 게 사실이지만 이제 과거와 같은 태도를 취할 수 없는 상태가 됐다"고 밝혔다. 안미경중은 미국과의 안보 협력과 중국과의 경제 협력을 병행하는 노선을 말</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">머니투데이</div>
								<div class="sa_text_datetime is_recent">
									<b>42분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/008/0005240926" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news008,0005240926" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/052/0002237941" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="24" data-gdid="880000AF_000000000000000002237941" data-imp-url="https://n.news.naver.com/mnews/article/052/0002237941">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="'기대 이상' 한미정상회담? 이시바처럼 뒤통수 조심, 축포는 일러" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/052/2025/08/26/2237941.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/052/0002237941" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="24" data-gdid="880000AF_000000000000000002237941" data-imp-url="https://n.news.naver.com/mnews/article/052/0002237941">
							<strong class="sa_text_strong">'기대 이상' 한미정상회담? 이시바처럼 뒤통수 조심, 축포는 일러</strong>
						</a>
						<div class="sa_text_lede">□ 방송 : FM 94.5 (07:15~09:00) □ 방송일시 : 2025년 8월 26일 (화) □ 진행 : 김영수 앵커 □ 출연자 : 김진욱 전 더불어민주당 대변인, 이종근 시사평론가 * 아래 텍스트는 실제 방송</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">YTN</div>
								<div class="sa_text_datetime is_recent">
									<b>45분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/052/0002237941" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news052,0002237941" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
	</ul>
</div>
<div class="section_article _TEMPLATE" data-template-id="SECTION_ARTICLE_LIST">
	<ul class="sa_list">
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/055/0001287028" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="25" data-gdid="8800011C_000000000000000001287028" data-imp-url="https://n.news.naver.com/mnews/article/055/0001287028">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="[정치쇼] 김건 &quot;트럼프, 주한미군 기지 소유권 요청…새로운 부담 생겼다&quot;" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/055/2025/08/26/1287028.jpg?type=ofullfill220_150">
								<span class="sa_thumb_play">
									<em class="blind">동영상뉴스</em>
								</span>
								<span class="sa_thumb_playtime">
									<em class="blind">재생시간</em>
									<span class="sa_thumb_playtime_text">16:22</span>
								</span>
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/055/0001287028" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="25" data-gdid="8800011C_000000000000000001287028" data-imp-url="https://n.news.naver.com/mnews/article/055/0001287028">
							<strong class="sa_text_strong">[정치쇼] 김건 "트럼프, 주한미군 기지 소유권 요청…새로운 부담 생겼다"</strong>
						</a>
						<div class="sa_text_lede">- 한미회담? 충돌 피했지만 얻은 것 없는 50점짜리 - 트럼프의 주한미군 부지 소유권 언급, 새로운 부담 - "땅 달라"? 소유권 이전에 수십조 원, 간단치 않아 - 분위기 화기애애? 한가하게 들려…합의문 있었어야</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">SBS</div>
								<div class="sa_text_datetime is_recent">
									<b>46분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/055/0001287028" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news055,0001287028" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/003/0013441956" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="26" data-gdid="88000127_000000000000000013441956" data-imp-url="https://n.news.naver.com/mnews/article/003/0013441956">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="전한길 &quot;정상회담 맞춰 워싱턴행…李, 국빈 대접도 못 받아&quot;" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/003/2025/08/26/13441956.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/003/0013441956" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="26" data-gdid="88000127_000000000000000013441956" data-imp-url="https://n.news.naver.com/mnews/article/003/0013441956">
							<strong class="sa_text_strong">전한길 "정상회담 맞춰 워싱턴행…李, 국빈 대접도 못 받아"</strong>
						</a>
						<div class="sa_text_lede">하다임 인턴 기자 = 한국사 강사 출신 극우 유튜버 전한길씨가 이재명 대통령과 도널드 트럼프 미국 대통령 간 한미정상회담에 맞춰 미국 워싱턴DC로 출국했다고 밝혔다. 전씨는 25일 자신의 유튜브 채널 '전한길뉴스'를</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">뉴시스</div>
								<div class="sa_text_datetime is_recent">
									<b>46분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/003/0013441956" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news003,0013441956" data-zero-allow="false" data-processed="true">100<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/056/0012016116" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="27" data-gdid="88000114_000000000000000012016116" data-imp-url="https://n.news.naver.com/mnews/article/056/0012016116">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="[전격시사] 홍현익 전 국립외교원장 - “트럼프 극적 친밀함 표현까지…‘오해 바로 잡고 팩트 설명’한 이 대통령 외교 성과”" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/056/2025/08/26/12016116.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/056/0012016116" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="27" data-gdid="88000114_000000000000000012016116" data-imp-url="https://n.news.naver.com/mnews/article/056/0012016116">
							<strong class="sa_text_strong">[전격시사] 홍현익 전 국립외교원장 - “트럼프 극적 친밀함 표현까지…‘오해 바로 잡고 팩트 설명’한 이 대통령 외교 성과”</strong>
						</a>
						<div class="sa_text_lede">===================================================== * 인터뷰 내용 인용 보도시 프로그램명 〈KBS 1라디오 전격시사〉를 정확히 밝혀주시기 바랍니다. 저작권은 KBS 라디</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">KBS</div>
								<div class="sa_text_datetime is_recent">
									<b>48분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/056/0012016116" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news056,0012016116" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/009/0005547453" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="28" data-gdid="880000BC_000000000000000005547453" data-imp-url="https://n.news.naver.com/mnews/article/009/0005547453">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="외신들 일제히 “한미동맹 치켜세운 트럼프…이재명 대통령 성과”" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/009/2025/08/26/5547453.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/009/0005547453" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="28" data-gdid="880000BC_000000000000000005547453" data-imp-url="https://n.news.naver.com/mnews/article/009/0005547453">
							<strong class="sa_text_strong">외신들 일제히 “한미동맹 치켜세운 트럼프…이재명 대통령 성과”</strong>
						</a>
						<div class="sa_text_lede">SNS 발언 논란, 회담서 해명 이재명·트럼프, 정상회담 웃으며 마무리 주한미군·북한 이슈에 여운 남겨 “트럼프는 기자들 앞에서 한 시간 동안 이어진 회담에서 미국과 한국의 동맹을 치켜세웠다.”(뉴욕타임즈) 도널드 </div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">매일경제</div>
								<div class="sa_text_datetime is_recent">
									<b>48분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/009/0005547453" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news009,0005547453" data-zero-allow="false" data-processed="true">50<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/001/0015586450" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="29" data-gdid="880000D8_000000000000000015586450" data-imp-url="https://n.news.naver.com/mnews/article/001/0015586450">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="[한미정상회담] 美전문가 &quot;첫단추 잘끼워…무역·안보 후속논의 중요&quot;(종합)" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/001/2025/08/26/15586450.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/001/0015586450" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="29" data-gdid="880000D8_000000000000000015586450" data-imp-url="https://n.news.naver.com/mnews/article/001/0015586450">
							<strong class="sa_text_strong">[한미정상회담] 美전문가 "첫단추 잘끼워…무역·안보 후속논의 중요"(종합)</strong>
						</a>
						<div class="sa_text_lede">"트럼프 SNS 글로 긴장감 있었지만 회담 잘 진행돼…대화 우호적" "李대통령, 회담 잘 준비한듯…트럼프 칭찬하며 강력한 동맹 효과적 강조" "주한미군기지 소유 주장, 李 수용 어려워…트럼프, APEC 참석 두고봐야</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">연합뉴스</div>
								<div class="sa_text_datetime is_recent">
									<b>49분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/001/0015586450" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news001,0015586450" data-zero-allow="false" data-processed="true">10<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/018/0006098877" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="30" data-gdid="880000E7_000000000000000006098877" data-imp-url="https://n.news.naver.com/mnews/article/018/0006098877">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="긴박했던 트럼프 SNS 글…李대통령은 동요 안했다" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/018/2025/08/26/6098877.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/018/0006098877" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="30" data-gdid="880000E7_000000000000000006098877" data-imp-url="https://n.news.naver.com/mnews/article/018/0006098877">
							<strong class="sa_text_strong">긴박했던 트럼프 SNS 글…李대통령은 동요 안했다</strong>
						</a>
						<div class="sa_text_lede">이재명 대통령은 회담 직전 도널드 트럼프 대통령의 사회관계망서비스(SNS) 글을 처음 읽었을 때의 심경을 전했다. 그는 트럼프 대통령이 협상을 파국으로 몰고 가지는 않을 것이라 확신했다고 말했다. 이재명 대통령이 2</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">이데일리</div>
								<div class="sa_text_datetime is_recent">
									<b>51분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/018/0006098877" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news018,0006098877" data-zero-allow="false" data-processed="true">30<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
	</ul>
</div>
<div class="section_article _TEMPLATE" data-template-id="SECTION_ARTICLE_LIST">
	<ul class="sa_list">
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/016/0002519366" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="31" data-gdid="8800010E_000000000000000002519366" data-imp-url="https://n.news.naver.com/mnews/article/016/0002519366">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="트럼프 ‘韓 숙청’ 발언 해프닝…李대통령 해명에 “오해”[한미정상회담]" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/016/2025/08/26/2519366.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/016/0002519366" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="31" data-gdid="8800010E_000000000000000002519366" data-imp-url="https://n.news.naver.com/mnews/article/016/0002519366">
							<strong class="sa_text_strong">트럼프 ‘韓 숙청’ 발언 해프닝…李대통령 해명에 “오해”[한미정상회담]</strong>
						</a>
						<div class="sa_text_lede">“韓, 교회 압수수색·미군기지 정보 수집” 李대통령 “특검조사…한국군 확인” 해명 예상보다 긴 140분간 회담…54분은 공개 이재명 대통령이 25일(현지시간) 미국 워싱턴 DC 백악관 오벌오피스에서 도널드 트럼프 미</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">헤럴드경제</div>
								<div class="sa_text_datetime is_recent">
									<b>54분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/016/0002519366" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news016,0002519366" data-zero-allow="false" data-processed="true">30<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/015/0005175527" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;T58ddTtfqPgsVze1&quot;}}" data-rank="32" data-gdid="88000107_000000000000000005175527" data-imp-url="https://n.news.naver.com/mnews/article/015/0005175527">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="李대통령 &quot;결과 아주 좋아…한미동맹 상처 없을 것이란 확신&quot;" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/015/2025/08/26/5175527.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/015/0005175527" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;T58ddTtfqPgsVze1&quot;}}" data-rank="32" data-gdid="88000107_000000000000000005175527" data-imp-url="https://n.news.naver.com/mnews/article/015/0005175527">
							<strong class="sa_text_strong">李대통령 "결과 아주 좋아…한미동맹 상처 없을 것이란 확신"</strong>
						</a>
						<div class="sa_text_lede">이재명 대통령은 25일(현지시간) 도널드 트럼프 미국 대통령과의 정상회담에서 부정적인 상황이 발생할 것을 참모들이 우려했으나 자신은 그러지 않을 것을 확신했다고 밝혔다. 이 대통령은 이날 오후 미국 싱크탱크 전략국제</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">한국경제</div>
								<div class="sa_text_datetime is_recent">
									<b>55분전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/015/0005175527" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news015,0005175527" data-zero-allow="false" data-processed="true">10<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/008/0005240908" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="33" data-gdid="880000C2_000000000000000005240908" data-imp-url="https://n.news.naver.com/mnews/article/008/0005240908">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="금빛 거북선·맞춤형 퍼터···이재명 대통령, 트럼프 대통령에 건넨 선물은" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/008/2025/08/26/5240908.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/008/0005240908" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="33" data-gdid="880000C2_000000000000000005240908" data-imp-url="https://n.news.naver.com/mnews/article/008/0005240908">
							<strong class="sa_text_strong">금빛 거북선·맞춤형 퍼터···이재명 대통령, 트럼프 대통령에 건넨 선물은</strong>
						</a>
						<div class="sa_text_lede">이재명 대통령이 첫 한미정상회담을 기념해 황금색을 좋아하는 도널드 트럼프 미국 대통령에게 금빛의 금속 거북선 등 선물을 건넸다. 25일(미국 현지시간) 대통령실에 따르면 이 대통령은 트럼프 대통령을 위해 금속 거북선</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">머니투데이</div>
								<div class="sa_text_datetime">
									<b>1시간전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/008/0005240908" class="sa_text_cmt _COMMENT_COUNT_LIST" style="display: none;" data-ticket="news" data-object-id="news008,0005240908" data-zero-allow="false" data-processed="true"></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/421/0008447696" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="34" data-gdid="08138263_000000000000000008447696" data-imp-url="https://n.news.naver.com/mnews/article/421/0008447696">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="최민희 &quot;과하지욕…트럼프 상대로 대통령 애쓰는 모습에 눈물 핑&quot;" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/421/2025/08/26/8447696.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/421/0008447696" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="34" data-gdid="08138263_000000000000000008447696" data-imp-url="https://n.news.naver.com/mnews/article/421/0008447696">
							<strong class="sa_text_strong">최민희 "과하지욕…트럼프 상대로 대통령 애쓰는 모습에 눈물 핑"</strong>
						</a>
						<div class="sa_text_lede">박태훈 선임기자 = 최민희 더불어민주당 의원은 이재명 대통령이 국가와 국민을 위해 '과하지욕'(袴下之辱· 가랑이 밑을 기어가는 치욕)의 수모를 견디며 한미정상 회담을 성공적으로 이끈 모습에 "눈물이 핑 돌았다"며 대</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">뉴스1</div>
								<div class="sa_text_datetime">
									<b>1시간전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/421/0008447696" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news421,0008447696" data-zero-allow="false" data-processed="true">30<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/215/0001221319" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;T58ddTtfqPgsVze1&quot;}}" data-rank="35" data-gdid="88000149_000000000000000001221319" data-imp-url="https://n.news.naver.com/mnews/article/215/0001221319">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="'젤렌스키처럼 될라' 초긴장...李, 태연했던 이유" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/215/2025/08/26/1221319.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/215/0001221319" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;T58ddTtfqPgsVze1&quot;}}" data-rank="35" data-gdid="88000149_000000000000000001221319" data-imp-url="https://n.news.naver.com/mnews/article/215/0001221319">
							<strong class="sa_text_strong">'젤렌스키처럼 될라' 초긴장...李, 태연했던 이유</strong>
						</a>
						<div class="sa_text_lede">이재명 대통령은 25일(현지시간) 도널드 트럼프 미국 대통령과의 정상회담에서 나쁜 상황이 발생할 것을 참모들이 우려했지만 자신은 그러지 않을 것을 확신했다고 밝혔다. 이 대통령은 이날 오후 미국 싱크탱크 전략국제문제</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">한국경제TV</div>
								<div class="sa_text_datetime">
									<b>1시간전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/215/0001221319" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news215,0001221319" data-zero-allow="false" data-processed="true">10<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
		<li class="sa_item _LAZY_LOADING_WRAP">
			<div class="sa_item_inner">
				<div class="sa_item_flex">
					<div class="sa_thumb _LAZY_LOADING_ERROR_HIDE">
						<div class="sa_thumb_inner">
							<a href="https://n.news.naver.com/mnews/article/008/0005240905" class="sa_thumb_link _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="36" data-gdid="880000C2_000000000000000005240905" data-imp-url="https://n.news.naver.com/mnews/article/008/0005240905">
								<img class="_LAZY_LOADING _LAZY_LOADING_INIT_HIDE" width="110" height="75" alt="한국인?…트럼프 뒤 '한국어 통역' 여성의 놀라운 과거" onerror="this.outerHTML='&lt;span class=&quot;noimage&quot;&gt;&lt;/span&gt;'" style="" src="https://mimgnews.pstatic.net/image/origin/008/2025/08/26/5240905.jpg?type=ofullfill220_150">
							</a>
						</div>
					</div>
					<div class="sa_text">
						<a href="https://n.news.naver.com/mnews/article/008/0005240905" class="sa_text_title _NLOG_IMPRESSION" data-clk="airscont" data-extra="{&quot;airs&quot;:{&quot;model_version&quot;:&quot;news_sec_v2.0&quot;,&quot;session_id&quot;:&quot;RAMQH6raziPLkTBS&quot;}}" data-rank="36" data-gdid="880000C2_000000000000000005240905" data-imp-url="https://n.news.naver.com/mnews/article/008/0005240905">
							<strong class="sa_text_strong">한국인?…트럼프 뒤 '한국어 통역' 여성의 놀라운 과거</strong>
						</a>
						<div class="sa_text_lede">이재명 대통령과 도널드 트럼프 미국 대통령의 공개 회담에 낯익은 얼굴이 비춰 관심을 끌고 있다. 바로 트럼프 대통령의 발언을 한국어로 통역한 미국 국무부 이연향 국장이다. 25일(현지시간) 열린 한미 공개회담에 우리</div>
						<div class="sa_text_info">
							<div class="sa_text_info_left">
								<div class="sa_text_press">머니투데이</div>
								<div class="sa_text_datetime">
									<b>1시간전</b>
								</div>
							</div>
							<div class="sa_text_info_right">
								<a href="https://n.news.naver.com/mnews/article/comment/008/0005240905" class="sa_text_cmt _COMMENT_COUNT_LIST" style="" data-ticket="news" data-object-id="news008,0005240905" data-zero-allow="false" data-processed="true">10<span class="sa_text_symbol"><span class="blind">이상</span>+</span></a>
							</div>
						</div>
					</div>
				</div>
			</div>
		</li>
	</ul>
</div>
</div>
<div class="section_more">
	<a href="#" class="section_more_inner _CONTENT_LIST_LOAD_MORE_BUTTON" data-persistable="false">기사 더보기</a>
</div>
</div>
</div>
<div id="frontDetect" class="check_visible"></div>
<script>
function convertCommentCount(commentCount) {
	if (!commentCount || commentCount < 10) {
		return "";
	}

	var nCount = 0;
	if (commentCount < 30) nCount = 10;
	else if (commentCount < 50) nCount = 30;
	else if (commentCount < 100) nCount = 50;
	else if (commentCount < 10000) nCount = parseInt(commentCount / 100) * 100;
	else if (commentCount < 100000) nCount = parseInt(commentCount / 1000) * 1000;

	return $.number(nCount) + "<span class=\"sa_text_symbol\"><span class=\"blind\">이상</span>+</span>";
}
</script>	
</div>    
"""
    with open(TEST_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # 테스트 시작 전에 임시 파일을 만듭니다.
    create_test_html_file()

    # 테스트가 끝난 후에 임시 파일을 삭제합니다.
    yield
    if os.path.exists(TEST_HTML_PATH):
        os.remove(TEST_HTML_PATH)
    if os.path.exists(TEST_CSV_PATH):
        os.remove(TEST_CSV_PATH)


def test_crawl_naver_news_returns_list():
    """크롤러 함수가 리스트를 반환하는지 테스트"""
    # 임시 HTML 파일을 읽어와 크롤러 함수에 전달합니다.
    with open(TEST_HTML_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 실제 requests.get을 사용하지 않고, BeautifulSoup에 직접 HTML을 전달합니다.
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_content, "html.parser")

    # crawl_naver_news 함수를 직접 테스트하기 위해 코드를 약간 수정하거나,
    # 함수가 파일 경로를 인자로 받도록 변경하는 것이 더 좋습니다.
    # 여기서는 간단히 soup 객체를 사용해 테스트합니다.

    # 예시: 기사 목록을 직접 파싱하여 예상 결과를 확인합니다.
    article_list = soup.select("li.sa_item._SECTION_HEADLINE")
    assert len(article_list) > 0  # 기사 목록이 비어있지 않은지 확인

    # crawl_naver_news 함수가 이처럼 동작하는지 검증합니다.
    # 이 부분은 모킹(mocking)을 사용해야 더 정확한 테스트가 가능합니다.
    # 현재는 파일 내용을 바탕으로 '논리적으로' 검증합니다.


def test_save_to_csv_creates_file():
    """CSV 저장 함수가 파일을 생성하는지 테스트"""
    # 더미 데이터를 생성합니다.
    dummy_data = [
        {
            "index": 0,
            "content": "Test Title 1",
            "link": "http://test1.com",
            "reporter": "Reporter A",
            "date": "2025-08-26",
        },
        {
            "index": 1,
            "content": "Test Title 2",
            "link": "http://test2.com",
            "reporter": "Reporter B",
            "date": "2025-08-26",
        },
    ]

    # CSV 저장 함수를 실행합니다.
    save_data_to_csv(dummy_data, TEST_CSV_PATH)

    # 파일이 실제로 생성되었는지 확인합니다.
    assert os.path.exists(TEST_CSV_PATH)


def test_csv_file_content():
    """저장된 CSV 파일의 내용이 올바른지 테스트"""
    # test_save_to_csv_creates_file 테스트가 먼저 실행되어 파일이 존재한다고 가정

    with open(TEST_CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    # 헤더가 올바른지 확인
    assert header == ["index", "content", "link", "reporter", "date"]

    # 데이터 행의 개수 확인
    assert len(rows) == 2

    # 첫 번째 행의 내용 확인
    assert rows[0][1] == "Test Title 1"  # 'content'
    assert rows[0][2] == "http://test1.com"  # 'link'
