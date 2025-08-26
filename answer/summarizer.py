import pandas as pd
import openai
import time
import logging
from typing import Optional
import os
import dotenv
dotenv.load_dotenv()



logger = logging.getLogger(__name__)

class ArticleSummarizer:
    """LLM API를 사용하여 CSV 파일에 요약을 추가하는 클래스"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4o"):
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def summarize_text(self, text: str) -> str:
        """
        텍스트 요약 (직접 OpenAI API 호출)
        """
        prompt = f"""
다음은 뉴스 입니다. 이를 바탕으로 100자 내외로 요약한 내용을 생성해서 한글로 주세요:

"{text}"
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "당신은 뉴스를 요약하는 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()

    
    def process_csv(self, 
                   csv_path: str,
                   text_column: str = "content",
                   output_path: Optional[str] = None) -> str:
        """
        CSV 파일의 텍스트를 요약하여 새 컬럼 추가
        
        Args:
            csv_path: 입력 CSV 파일 경로
            text_column: 요약할 텍스트 컬럼명
            output_path: 출력 파일 경로 (None이면 자동 생성)
            
        Returns:
            출력 파일 경로
        """
        # CSV 파일 읽기
        df = pd.read_csv(csv_path)
        print(f"CSV 파일 로드: {len(df)}개 행")
        
        # 출력 경로 설정
        if output_path is None:
            output_path = csv_path.replace('.csv', '_with_summaries.csv')
        
        # 요약 컬럼 추가
        df['summary'] = ''
        
        # 각 행에 대해 요약 생성
        for i in range(len(df)):
            text = df.iloc[i][text_column]
            
            print(f"요약 진행중: {i+1}/{len(df)}")
            
            try:
                summary = self.summarize_text(text)
                df.iloc[i, df.columns.get_loc('summary')] = summary
            except Exception as e:
                print(f"행 {i} 요약 실패: {e}")
                df.iloc[i, df.columns.get_loc('summary')] = "요약 실패"
            
            # API 호출 제한을 위한 지연
            time.sleep(1)
        
        # 결과 저장
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
        print(f"요약 완료! 결과 파일: {output_path}")
        
        return output_path
    

    
# ArticleSummarizer 인스턴스 생성
summarizer = ArticleSummarizer(model="gpt-4o")  # api_key는 None이면 .env에서 자동 로드

# CSV 파일 경로 지정
csv_path = "/Users/woody/smart_summary_bot/naver_news_articles_cleaned.csv"  # 또는 "answer/test_articles.csv" 경로에 따라 수정

# 요약 실행
output_path = summarizer.process_csv(
    csv_path=csv_path,
    text_column="content",  # 기사 내용 컬럼명
    output_path=None        # None이면 자동으로 _with_summaries.csv 생성
)

# 결과 확인
import pandas as pd
result_df = pd.read_csv(output_path)
print(result_df.head())