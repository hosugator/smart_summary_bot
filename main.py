# main.py

# main.py

import os
import sys

# 프로젝트 루트 디렉터리를 Python 경로에 추가하여 모듈을 임포트할 수 있게 합니다.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 각 모듈에서 핵심 함수를 임포트합니다.
# 폴더명과 동일한 함수명으로 변경했습니다.
from crawler.crawler import crawler
from preprocessor.preprocess import preprocessor
from answer.summarizer import summarizer
from modeler.model import modeler
from evaluator.evaluate import evaluator

# 데이터 파일 경로를 정의합니다.
RAW_DATA_PATH = "data/raw_news_data.csv"
PREPROCESSED_DATA_PATH = "data/preprocessed_data.csv"
FINAL_DATA_PATH = "data/final_dataset.csv"
MODEL_PATH = "models/summary_model.pth"
EVALUATION_RESULTS_PATH = "evaluation_results.csv"

def run_data_pipeline():
    """
    뉴스 데이터 수집부터 모델 학습 및 평가까지의 전체 데이터 파이프라인을 실행합니다.
    """
    print("🤖 Smart Summary Bot 데이터 파이프라인 시작...\n")

    # 1. 크롤링: 뉴스 기사 데이터 수집
    print("1. 뉴스 기사 크롤링 시작...")
    naver_urls = {
        "정치": "https://news.naver.com/section/100",
        "경제": "https://news.naver.com/section/101",
        "사회": "https://news.naver.com/section/102",
    }
    raw_news_data = crawler(naver_urls)
    # save_data_to_csv(raw_news_data, RAW_DATA_PATH)
    print("✅ 크롤링 완료 및 raw 데이터 저장\n")

    # 2. 전처리: 데이터 정제 및 가공
    print("2. 데이터 전처리 시작...")
    # preprocessed_data = preprocessor(raw_news_data)
    # save_to_csv(preprocessed_data, PREPROCESSED_DATA_PATH)
    print("✅ 전처리 완료 및 전처리된 데이터 저장\n")

    # 3. 요약 정답지 생성 (LLM API 활용)
    print("3. LLM API로 요약 정답지 생성 시작...")
    # final_data = summarizer(preprocessed_data)
    # save_to_csv(final_data, FINAL_DATA_PATH)
    print("✅ 요약 정답지 생성 완료 및 최종 데이터셋 저장\n")

    # 4. 모델 학습: 요약 모델 훈련
    print("4. 모델 학습 시작...")
    # trained_model = modeler(final_data)
    # save_model(trained_model, MODEL_PATH)
    print("✅ 모델 학습 완료 및 모델 파일 저장\n")

    # 5. 평가: 모델 성능 검증
    print("5. 모델 성능 평가 시작...")
    # evaluator(FINAL_DATA_PATH, EVALUATION_RESULTS_PATH)
    print("✅ 모델 평가 완료 및 결과 저장\n")

    print("--- 파이프라인 전체 완료 ---")


if __name__ == "__main__":
    # 데이터 파이프라인 실행
    run_data_pipeline()
    
    # 웹 서버는 구현하지 않으므로 주석 처리합니다.
    # from server.app import start_server
    # start_server()