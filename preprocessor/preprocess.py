# preprocessor/preprocess.py - 최종 수정 버전

import pandas as pd
import re
import nltk
import numpy as np
import requests
from bs4 import BeautifulSoup
from typing import Union
import warnings
warnings.filterwarnings('ignore')

# 한국어 형태소 분석기 (optional)
try:
    from konlpy.tag import Okt  
    HAS_KONLPY = True
    okt = Okt()
except ImportError:
    print("KoNLPy not available, Korean processing will be limited")
    HAS_KONLPY = False

# 기본 한국어 불용어 리스트 (필요시 확장 가능)
KOREAN_STOPWORDS = set([
    "그리고", "그러나", "하지만", "또한", "이것", "저것", "그것",
    "저희", "우리", "너희", "당신", "에서", "으로", "에게",
    "한다", "했다", "하는", "있다", "없다", "것", "수", "등"
])

# NLTK 리소스 다운로드 함수
def ensure_nltk_data():
    """NLTK 데이터 확인 및 다운로드"""
    required_data = [
        ('tokenizers/punkt', 'punkt'),
        ('corpora/wordnet', 'wordnet'),
        ('corpora/stopwords', 'stopwords')
    ]
    
    for data_path, name in required_data:
        try:
            nltk.data.find(data_path)
        except LookupError:
            print(f"Downloading {name}...")
            nltk.download(name, quiet=True)

ensure_nltk_data()

# 형태소 분석기 초기화
try:
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer

    stop_words_en = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
except:
    print("NLTK 초기화 중 오류 발생")

# 언어 감지 라이브러리
try:
    from langdetect import detect, LangDetectError
    HAS_LANGDETECT = True
except ImportError:
    print("langdetect not available, will use simple heuristics")
    HAS_LANGDETECT = False
    LangDetectError = Exception

def detect_language_safe(text):
    """안전한 언어 감지"""
    if not text or len(text.strip()) < 3:
        return 'en'
        
    if not HAS_LANGDETECT:
        # 간단한 한국어 감지 (한글 유니코드 범위)
        korean_chars = sum(1 for c in text if '\uac00' <= c <= '\ud7a3')
        return 'ko' if korean_chars > len(text) * 0.1 else 'en'
    
    try:
        return detect(text)
    except:
        # 폴백: 한글 문자 비율로 판단
        korean_chars = sum(1 for c in text if '\uac00' <= c <= '\ud7a3')
        return 'ko' if korean_chars > 0 else 'en'

def clean_text(text: str) -> str:
    """텍스트 기본 정리"""
    if not text or pd.isna(text):
        return ""
    
    text = str(text)
    text = re.sub(r'\s+', ' ', text)           # 연속 공백 정리
    text = re.sub(r'http\S+', '', text)        # 링크 제거
    text = re.sub(r'[^\w\sㄱ-ㅎㅏ-ㅣ가-힣]', '', text)  # 특수문자 제거 (한글+영문만 남김)
    return text.strip()

def tokenize_korean_safe(input_text):
    """안전한 한국어 토큰화"""
    if not HAS_KONLPY:
        # KoNLPy가 없는 경우 간단한 분할
        words = str(input_text).split()
        return [w for w in words if len(w) > 1 and w not in KOREAN_STOPWORDS]
    
    try:
        # 매우 엄격한 입력 검증
        if input_text is None:
            return []
        if pd.isna(input_text):
            return []
        if callable(input_text):
            print(f"ERROR: Function object passed to tokenize_korean_safe: {input_text}")
            return []
        if hasattr(input_text, '__call__'):
            print(f"ERROR: Callable object passed to tokenize_korean_safe: {input_text}")
            return []
            
        # 안전한 문자열 변환
        text_str = str(input_text).strip()
        
        if not text_str:
            return []
        if len(text_str) < 2:
            return []
            
        # KoNLPy 호출 전 한번 더 검증
        if not isinstance(text_str, str):
            print(f"ERROR: Not a string after conversion: {type(text_str)}")
            return []
            
        # 실제 KoNLPy 호출
        morphs_result = okt.morphs(text_str)
        
        # 결과 검증
        if not isinstance(morphs_result, list):
            print(f"ERROR: Unexpected morphs result type: {type(morphs_result)}")
            return []
            
        filtered_tokens = [w for w in morphs_result if len(w) > 1 and w not in KOREAN_STOPWORDS]
        return filtered_tokens
        
    except Exception as e:
        print(f"Korean tokenization error with text '{str(input_text)[:50]}...': {e}")
        print(f"Input type: {type(input_text)}")
        # 실패 시 단순 분할
        try:
            words = str(input_text).split()
            return [w for w in words if len(w) > 1]
        except:
            return []

def tokenize_english_safe(input_text):
    """안전한 영어 토큰화"""
    try:
        # 엄격한 입력 검증
        if input_text is None or pd.isna(input_text):
            return []
        if callable(input_text) or hasattr(input_text, '__call__'):
            print(f"ERROR: Callable object passed to tokenize_english_safe: {input_text}")
            return []
            
        text_str = str(input_text).strip().lower()
        if not text_str:
            return []
            
        tokens = word_tokenize(text_str)
        filtered_tokens = [lemmatizer.lemmatize(w) for w in tokens 
                          if w.isalpha() and len(w) > 1 and w not in stop_words_en]
        return filtered_tokens
    except Exception as e:
        print(f"English tokenization error with text '{str(input_text)[:50]}...': {e}")
        # 실패 시 단순 분할
        try:
            words = str(input_text).lower().split()
            return [w for w in words if w.isalpha() and len(w) > 1]
        except:
            return []

def tokenize_and_normalize(input_text, lang: str = "en") -> list:
    """언어별 토큰화 + 불용어 제거 + 표제어 추출"""
    # 매우 엄격한 입력 검증
    if input_text is None or pd.isna(input_text):
        return []
    if callable(input_text) or hasattr(input_text, '__call__'):
        print(f"ERROR: Callable object passed to tokenize_and_normalize: {input_text}")
        return []
    
    try:
        text_str = str(input_text).strip()
    except Exception as e:
        print(f"ERROR: Cannot convert to string: {input_text}, error: {e}")
        return []
    
    if not text_str or len(text_str) < 3:
        return []

    # 언어 감지
    detected_lang = detect_language_safe(text_str)
    
    # 토큰화
    if detected_lang == "ko":
        return tokenize_korean_safe(text_str)
    else:
        return tokenize_english_safe(text_str)

def load_csv(csv_path: str) -> pd.DataFrame: 
    """CSV 파일 불러오고 전처리 - pandas apply 사용하지 않음"""
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
    
    # 수동으로 각 행 처리 (pandas apply 사용 안 함)
    processed_data = []
    
    for row_idx in range(len(df)):
        try:
            # 개별 행 데이터 가져오기 - 안전한 방식
            single_row = df.iloc[row_idx]
            raw_content = single_row['content']
            
            print(f"Processing row {row_idx}: type={type(raw_content)}, value preview='{str(raw_content)[:50]}...'")
            
            # 기본 검증
            if raw_content is None or pd.isna(raw_content):
                print(f"Skipping row {row_idx}: None or NaN")
                continue
            
            if callable(raw_content) or hasattr(raw_content, '__call__'):
                print(f"ERROR: Row {row_idx} contains callable object: {raw_content}")
                continue
            
            try:
                content_str = str(raw_content).strip()
            except Exception as str_error:
                print(f"ERROR: Cannot convert row {row_idx} to string: {str_error}")
                continue
                
            if len(content_str) < 5:  # 너무 짧은 텍스트 제외
                print(f"Skipping row {row_idx}: too short ({len(content_str)} chars)")
                continue
            
            # 텍스트 정리
            try:
                cleaned_content = clean_text(content_str)
            except Exception as clean_error:
                print(f"ERROR: Cannot clean text for row {row_idx}: {clean_error}")
                continue
                
            if not cleaned_content:
                print(f"Skipping row {row_idx}: empty after cleaning")
                continue
            
            # 토큰화 - 매우 안전하게
            try:
                token_list = tokenize_and_normalize(cleaned_content)
            except Exception as token_error:
                print(f"ERROR: Tokenization failed for row {row_idx}: {token_error}")
                continue
            
            # 최소 토큰 수 체크
            if len(token_list) < 3:
                print(f"Skipping row {row_idx}: insufficient tokens ({len(token_list)})")
                continue
            
            processed_data.append({
                'content': content_str,
                'content_clean': cleaned_content,
                'tokens': token_list
            })
            
            print(f"Successfully processed row {row_idx}: {len(token_list)} tokens")
            
        except Exception as row_error:
            print(f"ERROR processing row {row_idx}: {row_error}")
            import traceback
            traceback.print_exc()
            continue
    
    if not processed_data:
        print("No valid data after processing")
        return pd.DataFrame(columns=['content', 'content_clean', 'tokens'])
    
    result_df = pd.DataFrame(processed_data)
    
    # 중복 제거
    original_len = len(result_df)
    result_df = result_df.drop_duplicates(subset=['content_clean'])
    if original_len != len(result_df):
        print(f"Removed {original_len - len(result_df)} duplicates")
    
    print(f"CSV 전처리 완료: {len(result_df)}개 행 처리됨")
    return result_df

def load_article(url: str) -> pd.DataFrame:
    """웹 기사 URL에서 본문 크롤링 및 전처리"""
    print(f"Loading URL: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 불필요한 태그 제거
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            tag.decompose()
        
        article_text = soup.get_text(separator=' ', strip=True)
        print(f"Extracted {len(article_text)} characters from URL")
        
        if not article_text or len(article_text) < 50:
            print(f"WARN: 추출된 텍스트가 너무 짧습니다: {len(article_text)} characters")
            article_text = "No sufficient content extracted from URL"
        
        # 기본 정리
        cleaned = clean_text(article_text)
        
        # 토큰화
        tokens = tokenize_and_normalize(cleaned)
        
        # DataFrame 생성
        df = pd.DataFrame([{
            "content": article_text, 
            "content_clean": cleaned,
            "tokens": tokens
        }])
        
        print(f"URL 전처리 완료: {len(article_text)} characters extracted, {len(tokens)} tokens")
        return df
        
    except Exception as e:
        print(f"URL 크롤링 실패: {e}")
        # 빈 DataFrame 반환
        return pd.DataFrame(columns=['content', 'content_clean', 'tokens'])

def load_and_preprocess(source: Union[str, list]) -> pd.DataFrame:
    """
    입력이 CSV 경로 또는 URL일 수 있음
    - CSV: 파일 확장자가 .csv이면 CSV 로드
    - URL: http:// 또는 https://로 시작하면 기사 로드
    - 리스트: 여러 소스를 한 번에 처리
    """
    if isinstance(source, list):
        dfs = []
        for s in source:
            try:
                df = load_and_preprocess(s)
                if not df.empty:
                    dfs.append(df)
            except Exception as e:
                print(f"소스 '{s}' 처리 중 오류: {e}")
                continue
        
        if dfs:
            return pd.concat(dfs, ignore_index=True)
        else:
            return pd.DataFrame(columns=['content', 'content_clean', 'tokens'])

    if source.endswith(".csv"):
        return load_csv(source)
    elif source.startswith("http://") or source.startswith("https://"):
        return load_article(source)
    else:
        raise ValueError("지원하지 않는 입력 형식입니다. CSV 파일 경로나 기사 URL을 입력하세요.")