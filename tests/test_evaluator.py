# tests/test_evaluator.py

import pytest
import os
import pandas as pd
from evaluator.evaluator import evaluate_model, mock_predict_summary

# 테스트에 사용할 임시 파일 경로를 정의합니다.
TEST_OUTPUT_CSV_PATH = "tests/test_evaluation_results.csv"
TEST_INPUT_CSV_PATH = "tests/test_data.csv"

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """테스트 전/후에 임시 파일을 생성하고 삭제합니다."""
    # 테스트에 사용할 더미 데이터가 포함된 CSV 파일을 생성합니다.
    dummy_data = {
        'full_content': [
            '이 문장은 테스트를 위한 긴 뉴스 기사입니다. 이 기사는 모델이 요약해야 할 내용들을 담고 있습니다. 중요한 정보를 포함하고 있어 요약이 필요합니다.',
            '다른 기사입니다. 이 기사는 ROUGE 스코어 테스트를 위해 작성되었습니다. 여기서 모델이 예측한 요약이 정답과 얼마나 일치하는지 확인할 수 있습니다.',
        ],
        'target_summary': [
            '테스트를 위한 긴 뉴스 기사입니다. 요약이 필요합니다.',
            'ROUGE 스코어 테스트를 위한 기사입니다. 일치 여부 확인.',
        ],
        'index': [0, 1]
    }
    dummy_df = pd.DataFrame(dummy_data)
    dummy_df.to_csv(TEST_INPUT_CSV_PATH, index=False)
    
    yield
    
    # 테스트가 끝난 후에 생성된 파일을 삭제합니다.
    if os.path.exists(TEST_INPUT_CSV_PATH):
        os.remove(TEST_INPUT_CSV_PATH)
    if os.path.exists(TEST_OUTPUT_CSV_PATH):
        os.remove(TEST_OUTPUT_CSV_PATH)

def test_evaluate_model_creates_output_file():
    """evaluate_model 함수가 평가 결과를 CSV 파일로 생성하는지 테스트"""
    # 평가 함수 실행
    evaluate_model(TEST_INPUT_CSV_PATH, TEST_OUTPUT_CSV_PATH, mock_predict_summary)
    
    # 출력 파일이 성공적으로 생성되었는지 확인합니다.
    assert os.path.exists(TEST_OUTPUT_CSV_PATH)

def test_evaluate_model_calculates_correct_scores():
    """evaluate_model 함수가 올바른 ROUGE 스코어를 계산하는지 테스트"""
    # 평가 함수 실행
    evaluate_model(TEST_INPUT_CSV_PATH, TEST_OUTPUT_CSV_PATH, mock_predict_summary)
    
    # 생성된 결과를 읽어와서 내용이 올바른지 검증합니다.
    results_df = pd.read_csv(TEST_OUTPUT_CSV_PATH)
    
    # 예상 ROUGE 스코어를 계산합니다.
    # mock_predict_summary는 본문 앞부분을 잘라서 반환하므로, 정확한 스코어 계산이 가능합니다.
    from rouge_score import rouge_scorer
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    
    # 첫 번째 기사의 스코어
    scores_1 = scorer.score(
        '테스트를 위한 긴 뉴스 기사입니다. 요약이 필요합니다.',
        '이 문장은 테스트를 위한 긴 뉴스 기사입니다. 이 기사는 모델이 요약해야 할 내용들을 담고 있습니다. 중요한 정보를 포함하고...'
    )
    # 두 번째 기사의 스코어
    scores_2 = scorer.score(
        'ROUGE 스코어 테스트를 위한 기사입니다. 일치 여부 확인.',
        '다른 기사입니다. 이 기사는 ROUGE 스코어 테스트를 위해 작성되었습니다. 여기서 모델이 예측한 요약이 정답과 얼마나 일치하는지...'
    )
    
    # 소수점 4자리까지 비교하여 정확성 검증
    assert results_df.iloc[0]['rougeL_fmeasure'] == pytest.approx(scores_1['rougeL'].fmeasure, 0.001)
    assert results_df.iloc[1]['rougeL_fmeasure'] == pytest.approx(scores_2['rougeL'].fmeasure, 0.001)

def test_evaluator_handles_missing_columns():
    """필요한 열이 없는 경우 오류를 처리하는지 테스트"""
    # **수정된 부분: 테스트 시작 전 출력 파일이 존재하면 삭제합니다.**
    if os.path.exists(TEST_OUTPUT_CSV_PATH):
        os.remove(TEST_OUTPUT_CSV_PATH)

    # 'full_content'와 'target_summary'가 없는 더미 CSV를 생성합니다.
    dummy_df = pd.DataFrame({'content': ['기사 1', '기사 2']})
    dummy_df.to_csv(TEST_INPUT_CSV_PATH, index=False)
    
    # 함수가 오류 없이 종료되는지, 그리고 출력 파일이 생성되지 않는지 확인합니다.
    evaluate_model(TEST_INPUT_CSV_PATH, TEST_OUTPUT_CSV_PATH, mock_predict_summary)
    assert not os.path.exists(TEST_OUTPUT_CSV_PATH)