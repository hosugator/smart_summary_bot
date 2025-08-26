# # embedder/embed.py
# embed.py - M4 Mac 최적화 임베딩 모듈 (TensorFlow 없음)

import pandas as pd
import numpy as np
import pickle
import logging
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA

logger = logging.getLogger(__name__)


class M4SummaryEmbedder:
    """M4 Mac 최적화 임베더 (TensorFlow 없음)"""
    #대신  TF-IDF + PCA 방식 사용
    #기존의 TF-IDF의 경우 어휘 수 만큼 차원을 생성하기 때문 > 너무 많은 차원을 생성하게 됨.
    # 앞의 TF-IDF를 기반으로 한 중요도에 의거하여 중요도가 높은 어휘들만 압축하고 차원을 축소함.
    
    def __init__(self, embedding_dim=512):
        self.embedding_dim = embedding_dim
        self.vectorizer = None
        self.pca = None
        print(f"🍎 M4 Mac 최적화 임베더 초기화 (차원: {embedding_dim})")
    
    def load_csv(self, csv_path):
        """CSV 파일 로드"""
        df = pd.read_csv(csv_path)
        logger.info(f"CSV 로드: {df.shape[0]}행, {df.shape[1]}열")
        print(f"📄 CSV 로드: {df.shape[0]}행, {df.shape[1]}열")
        return df
    
    def extract_summaries(self, df, summary_column='summary'):
        """DataFrame에서 summary 컬럼 추출"""
        summaries = df[summary_column].fillna('').astype(str)
        summaries = summaries[summaries.str.strip() != '']  # 빈 문자열 제거
        
        logger.info(f"유효한 요약 텍스트: {len(summaries)}개")
        print(f"📝 유효한 요약 텍스트: {len(summaries)}개")
        return summaries.tolist()
    
    def create_embeddings(self, texts, batch_size=32):
        """텍스트를 임베딩으로 변환"""
        print(f"📊 {len(texts)}개 텍스트 임베딩 시작...")
        
        # TF-IDF 벡터화 (한국어 최적화)
        self.vectorizer = TfidfVectorizer(
            max_features=3000,      # 특성 수 증가
            ngram_range=(1, 3),     # 3-gram까지 사용
            min_df=1,               # 최소 빈도 낮춤
            max_df=0.9,             # 최대 빈도 높임
            analyzer='word',
            token_pattern=r'\b\w+\b'
        )
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            print(f"   TF-IDF 매트릭스: {tfidf_matrix.shape}")
            logger.info(f"TF-IDF 매트릭스: {tfidf_matrix.shape}")
        except Exception as e:
            print(f"   TF-IDF 오류: {e}")
            logger.error(f"TF-IDF 오류: {e}")
            return None
        
        # PCA 차원 축소
        n_components = min(self.embedding_dim, tfidf_matrix.shape[1], len(texts))
        print(f"   PCA 차원: {tfidf_matrix.shape[1]} → {n_components}")
        
        self.pca = PCA(n_components=n_components, random_state=42)
        
        try:
            embeddings = self.pca.fit_transform(tfidf_matrix.toarray())
            
            # 차원 패딩 (512차원 맞추기)
            if embeddings.shape[1] < self.embedding_dim:
                padding = np.zeros((embeddings.shape[0], self.embedding_dim - embeddings.shape[1]))
                embeddings = np.hstack([embeddings, padding])
                print(f"   패딩 적용: {embeddings.shape}")
            
            print(f"✅ 임베딩 완료: {embeddings.shape}")
            print(f"   범위: {embeddings.min():.3f} ~ {embeddings.max():.3f}")
            logger.info(f"임베딩 완료: {embeddings.shape}")
            
            return embeddings
            
        except Exception as e:
            print(f"   PCA 오류: {e}")
            logger.error(f"PCA 오류: {e}")
            return None
    
    def save_embeddings(self, embeddings, texts, original_df, output_path):
        """임베딩 결과 저장"""
        # 1. NumPy 배열 저장 (모델 학습용)
        np.save(f"{output_path}_embeddings.npy", embeddings)
        
        # 2. 전체 데이터 Pickle 저장
        data = {
            'embeddings': embeddings,
            'texts': texts,
            'original_data': original_df,
            'embedding_dim': embeddings.shape[1],
            'timestamp': datetime.now().isoformat()
        }
        
        with open(f"{output_path}_data.pkl", 'wb') as f:
            pickle.dump(data, f)
        
        logger.info(f"저장 완료: {output_path}_embeddings.npy, {output_path}_data.pkl")
        print(f"💾 저장 완료: {output_path}_embeddings.npy, {output_path}_data.pkl")
    
    def fit_transform(self, texts):
        """간단한 인터페이스: 텍스트 → 임베딩"""
        return self.create_embeddings(texts)
    
    def process_csv_to_embeddings(self, csv_path, summary_column='summary', output_path=None):
        """CSV → 임베딩 전체 프로세스"""
        try:
            # 1. 데이터 로드
            df = self.load_csv(csv_path)
            summaries = self.extract_summaries(df, summary_column)
            
            # 2. 임베딩 생성
            embeddings = self.create_embeddings(summaries)
            
            if embeddings is None:
                return {'success': False, 'error': '임베딩 생성 실패'}
            
            # 3. 결과 저장
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"m4_embeddings_{timestamp}"
            
            self.save_embeddings(embeddings, summaries, df, output_path)
            
            return {
                'success': True,
                'total_texts': len(summaries),
                'embedding_shape': embeddings.shape,
                'output_path': output_path
            }
            
        except Exception as e:
            logger.error(f"처리 실패: {e}")
            print(f"❌ 처리 실패: {e}")
            return {'success': False, 'error': str(e)}


def create_dummy_csv(filename="test_summary.csv", num_rows=100):
    """테스트용 더미 데이터 생성"""
    print("🔧 테스트 데이터 생성 중...")
    
    # 다양한 주제의 더미 데이터
    topics = [
        "AI 인공지능 기술 발전 머신러닝 딥러닝 자연어처리",
        "경제 금융 투자 주식 부동산 시장 동향 분석",
        "정치 선거 정책 국정 외교 국제관계 정부",
        "사회 문화 교육 복지 환경 기후변화 지속가능",
        "과학 기술 연구 개발 혁신 발견 실험",
        "스포츠 축구 야구 농구 올림픽 경기 선수",
        "엔터테인먼트 영화 드라마 음악 연예 문화",
        "건강 의료 질병 치료 예방 백신 병원",
        "여행 관광 문화 음식 축제 지역 명소",
        "IT 스마트폰 컴퓨터 소프트웨어 앱 디지털"
    ]
    
    dummy_data = {
        'url': [f'https://news-example.com/article_{i}' for i in range(num_rows)],
        'title': [f'{topics[i % len(topics)].split()[0]} 관련 뉴스 {i}' for i in range(num_rows)],
        'summary': [
            f'{topics[i % len(topics)]}에 대한 요약입니다. '
            f'최근 동향과 전망을 분석한 기사 {i}번입니다. '
            f'전문가들은 향후 발전 가능성에 대해 긍정적으로 평가하고 있습니다.'
            for i in range(num_rows)
        ]
    }
    
    df = pd.DataFrame(dummy_data)
    df.to_csv(filename, index=False, encoding='utf-8')
    
    print(f"✅ 테스트 데이터 생성 완료: {filename} ({num_rows}행, {len(topics)}개 주제)")
    return filename


# 사용 예시 및 테스트
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🚀 M4 임베딩 모듈 테스트 시작!")
    
    # 테스트 데이터 생성
    csv_file = create_dummy_csv("m4_test.csv", 50)
    
    # 임베더 사용
    embedder = M4SummaryEmbedder(embedding_dim=512)
    
    result = embedder.process_csv_to_embeddings(
        csv_path=csv_file,
        summary_column="summary",
        output_path="m4_test_embeddings"
    )
    
    print("\n📊 결과:", result)
    
    if result['success']:
        print("🎉 M4 임베딩 모듈 테스트 성공!")
    else:
        print("❌ M4 임베딩 모듈 테스트 실패!")
