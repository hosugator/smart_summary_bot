# evaluator/evaluator.py

import pandas as pd
from rouge_score import rouge_scorer
import os
import csv

# 이 함수는 실제 모델의 추론을 모의(mock)하는 역할을 합니다.
# 실제 모델을 사용할 때는 이 함수를 모델 로직으로 대체해야 합니다.
def mock_predict_summary(text):
    """
    텍스트를 입력받아 요약문을 반환하는 모의 함수
    여기서는 간단하게 입력 텍스트의 첫 100자를 반환합니다.
    """
    # 실제 모델이 이 자리에 들어갈 예정입니다.
    # 예: summary_text = model.generate(text)
    return text[:100] + "..."

def evaluate_model(csv_file_path, output_file_path, model_inference_fn):
    """
    CSV 파일의 기사 본문과 정답지 요약문을 비교하여 모델의 성능을 평가하는 함수

    Args:
        csv_file_path (str): 기사 본문과 정답지 요약문이 포함된 CSV 파일 경로.
        output_file_path (str): 평가 결과를 저장할 CSV 파일 경로.
        model_inference_fn (function): 모델 추론을 수행하는 함수 (예: mock_predict_summary).
    """
    if not os.path.exists(csv_file_path):
        print(f"Error: The file {csv_file_path} was not found.")
        return

    try:
        df = pd.read_csv(csv_file_path)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    if 'full_content' not in df.columns or 'target_summary' not in df.columns:
        print("Error: The CSV file must contain 'full_content' and 'target_summary' columns.")
        return

    # ROUGE 스코어 계산기 초기화
    # ROUGE-1 (단어), ROUGE-2 (두 단어 묶음), ROUGE-L (가장 긴 공통 부분 문자열)을 계산합니다.
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    
    evaluation_results = []

    for index, row in df.iterrows():
        # 모델 추론
        predicted_summary = model_inference_fn(row['full_content'])
        
        # ROUGE 스코어 계산
        scores = scorer.score(row['target_summary'], predicted_summary)
        
        evaluation_results.append({
            'index': row['index'],
            'rouge1_fmeasure': scores['rouge1'].fmeasure,
            'rouge2_fmeasure': scores['rouge2'].fmeasure,
            'rougeL_fmeasure': scores['rougeL'].fmeasure,
        })
        print(f"Processing index {row['index']}: ROUGE-L Score = {scores['rougeL'].fmeasure:.4f}")

    # 평가 결과를 DataFrame으로 변환
    results_df = pd.DataFrame(evaluation_results)

    # 평균 스코어 계산
    average_scores = results_df[['rouge1_fmeasure', 'rouge2_fmeasure', 'rougeL_fmeasure']].mean().to_dict()
    average_scores = {key: f"{value:.4f}" for key, value in average_scores.items()}
    print("\nAverage ROUGE Scores:")
    for metric, score in average_scores.items():
        print(f"- {metric}: {score}")

    # 결과를 CSV 파일로 저장
    results_df.to_csv(output_file_path, index=False)
    print(f"\nEvaluation results saved to {output_file_path}")

if __name__ == "__main__":
    # 이 부분은 실제 사용에 맞게 경로를 수정해야 합니다.
    input_csv_path = 'naver_news_articles.csv'
    output_csv_path = 'evaluation_results.csv'
    
    # 평가 함수 실행
    evaluate_model(input_csv_path, output_csv_path, mock_predict_summary)