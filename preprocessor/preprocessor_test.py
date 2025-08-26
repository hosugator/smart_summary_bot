# preprocessor/preprocess.py - 간소화 버전

import pandas as pd
import re
import warnings
warnings.filterwarnings('ignore')

def clean_text(text: str) -> str:
    """텍스트 기본 정리"""
    if not text or pd.isna(text):
        return ""
    
    text = str(text)
    text = re.sub(r'\s+', ' ', text)           # 연속 공백 정리
    text = re.sub(r'http\S+', '', text)        # 링크 제거
    text = re.sub(r'[^\w\sㄱ-ㅎㅏ-ㅣ가-힣]', '', text)  # 특수문자 제거 (한글+영문만 남김)
    return text.strip()

def load_csv(csv_path: str) -> pd.DataFrame: 
    """CSV 파일 불러오고 전처리"""
    print(f"Loading CSV: {csv_path}")
    
    # 다양한 인코딩으로 시도
    encodings = ['utf-8-sig', 'utf-8', 'cp949', 'euc-kr', 'latin-1']
    df = None
    
    for encoding in encodings:
        try:
            df = pd.read_csv(csv_path, encoding=encoding)
            print(f"Successfully loaded with {encoding} encoding")
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception as e:
            print(f"Error with {encoding}: {e}")
            continue
    
    if df is None:
        raise Exception("Failed to load CSV with any encoding")
    
    # content 컬럼 확인
    if 'content' not in df.columns:
        print("No 'content' column found. Available columns:", df.columns.tolist())
        df['content'] = ''
    
    print(f"Original CSV rows: {len(df)}")
    
    # 수동으로 각 행 처리
    processed_data = []
    
    for row_idx in range(len(df)):
        try:
            single_row = df.iloc[row_idx]
            raw_content = single_row['content']
            
            # 기본 검증
            if raw_content is None or pd.isna(raw_content):
                continue
            
            content_str = str(raw_content).strip()
            if len(content_str) < 5:  # 너무 짧은 텍스트 제외
                continue
            
            # 텍스트 정리
            cleaned_content = clean_text(content_str)
            if not cleaned_content:
                continue
            
            processed_data.append({
                'content': content_str,
                'content_clean': cleaned_content
            })
            
        except Exception as row_error:
            print(f"ERROR processing row {row_idx}: {row_error}")
            continue
    
    if not processed_data:
        print("No valid data after processing")
        return pd.DataFrame(columns=['content', 'content_clean'])
    
    result_df = pd.DataFrame(processed_data)
    
    # 중복 제거
    original_len = len(result_df)
    result_df = result_df.drop_duplicates(subset=['content_clean'])
    if original_len != len(result_df):
        print(f"Removed {original_len - len(result_df)} duplicates")
    
    print(f"CSV 전처리 완료: {len(result_df)}개 행 처리됨")
    return result_df

def load_and_preprocess(source: str) -> pd.DataFrame:
    """CSV 파일 로드 및 전처리"""
    if source.endswith(".csv"):
        return load_csv(source)
    else:
        raise ValueError("CSV 파일 경로를 입력하세요.")
    
    
if __name__ == "__main__":
    # 전처리할 CSV 파일 경로 지정
    csv_path = "/Users/woody/smart_summary_bot/naver_news_articles.csv"  # 파일 위치에 맞게 수정

    # 전처리 실행
    df = load_and_preprocess(csv_path)
    print(df.head())

    # 전처리 결과를 새 CSV 파일로 저장
    output_path = "/Users/woody/smart_summary_bot/naver_news_articles_cleaned.csv"
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"전처리 결과를 {output_path} 파일로 저장했습니다.")