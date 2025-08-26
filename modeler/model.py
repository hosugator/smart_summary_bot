# # modeler/model.py


# TensorFlow/PyTorch 라이브러리 호환성 문제 발생 
# 비교적 호환성이 좋은 Scikit-learn 라이브러리 사용
# 텍스트 분류에 최적화(단어별)
# CPU에 최적화
import numpy as np
import pickle
import logging
import json
from datetime import datetime
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (Mac용)
plt.rcParams['font.family'] = ['Arial Unicode MS', 'AppleGothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

logger = logging.getLogger(__name__)


class M4TransformerModel:
    """M4 Mac 최적화 분류 모델 (TensorFlow 없이 RandomForest 사용)"""
    
    def __init__(self, n_estimators=200, max_depth=10):
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=5, 
            random_state=42,
            n_jobs=-1           # 모든 CPU 코어 사용
        )
        self.kmeans = None
        self.is_fitted = False
        self.config = {
            'n_estimators': n_estimators,
            'max_depth': max_depth,
            'model_type': 'RandomForest',
            'timestamp': datetime.now().isoformat()
        }
        print(f"🧠 M4 Mac 최적화 RandomForest 모델 초기화")
        print(f"   설정: {n_estimators} trees, max_depth={max_depth}")
    
    def load_embeddings(self, embeddings_path, data_path=None):
        """저장된 임베딩 데이터 로드"""
        embeddings = np.load(embeddings_path)
        logger.info(f"임베딩 로드: {embeddings.shape}")
        print(f"📊 임베딩 로드: {embeddings.shape}")
        
        metadata = None
        if data_path and os.path.exists(data_path):
            with open(data_path, 'rb') as f:
                metadata = pickle.load(f)
            logger.info(f"메타데이터 로드: {len(metadata['texts'])}개")
            print(f"📄 메타데이터 로드: {len(metadata['texts'])}개 텍스트")
        
        return embeddings, metadata
    
    def create_labels(self, embeddings, n_clusters=8):
        """K-means로 라벨 생성 (비지도 학습)"""
        print(f"🏷️  K-means 클러스터링 ({n_clusters}개 클러스터)...")
        
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = self.kmeans.fit_predict(embeddings)
        
        unique, counts = np.unique(labels, return_counts=True)
        print(f"   클러스터 분포: {dict(zip(unique, counts))}")
        logger.info(f"클러스터 분포: {dict(zip(unique, counts))}")
        
        return labels
    
    def prepare_data(self, embeddings, labels=None, test_size=0.2):
        """학습 데이터 준비"""
        # 라벨이 없으면 클러스터링으로 생성
        if labels is None:
            n_clusters = min(10, len(embeddings) // 10)
            labels = self.create_labels(embeddings, n_clusters)
        
        # 데이터 분할
        X_train, X_test, y_train, y_test = train_test_split(
            embeddings, labels, test_size=test_size, random_state=42, 
            stratify=labels
        )
        
        print(f"📚 데이터 분할: 훈련 {len(X_train)}, 테스트 {len(X_test)}")
        logger.info(f"데이터 분할: 훈련 {len(X_train)}, 테스트 {len(X_test)}")
        
        return X_train, X_test, y_train, y_test
    
    def fit(self, X, y):
        """모델 훈련 (sklearn 호환)"""
        return self.train(X, y)
    
    def train(self, X_train, y_train, X_test=None, y_test=None):
        """모델 훈련"""
        print(f"📚 모델 훈련 시작: {X_train.shape} → {len(np.unique(y_train))} 클래스")
        
        try:
            self.model.fit(X_train, y_train)
            self.is_fitted = True
            
            # 특성 중요도 확인
            importances = self.model.feature_importances_
            print(f"✅ 훈련 완료 (평균 특성 중요도: {importances.mean():.4f})")
            logger.info(f"훈련 완료 - 특성 중요도: {importances.mean():.4f}")
            
            # 훈련 정확도
            train_score = self.model.score(X_train, y_train)
            print(f"   훈련 정확도: {train_score:.4f}")
            
            # 검증 정확도 (있는 경우)
            if X_test is not None and y_test is not None:
                test_score = self.model.score(X_test, y_test)
                print(f"   검증 정확도: {test_score:.4f}")
            
        except Exception as e:
            print(f"❌ 훈련 실패: {e}")
            logger.error(f"훈련 실패: {e}")
    
    def predict(self, X):
        """예측"""
        if not self.is_fitted:
            raise ValueError("모델이 훈련되지 않았습니다.")
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """확률 예측"""  
        if not self.is_fitted:
            raise ValueError("모델이 훈련되지 않았습니다.")
        return self.model.predict_proba(X)
    
    def evaluate(self, X_test, y_test):
        """모델 평가"""
        print("\n📊 모델 평가 시작...")
        
        test_loss = None  # RandomForest는 loss가 없음
        test_accuracy = self.model.score(X_test, y_test)
        
        predictions = self.model.predict(X_test)
        report = classification_report(y_test, predictions, output_dict=True)
        
        results = {
            'test_loss': test_loss,
            'test_accuracy': float(test_accuracy),
            'classification_report': report
        }
        
        print(f"✅ 테스트 정확도: {test_accuracy:.4f}")
        print(f"   정밀도: {report['macro avg']['precision']:.4f}")
        print(f"   재현율: {report['macro avg']['recall']:.4f}")
        print(f"   F1점수: {report['macro avg']['f1-score']:.4f}")
        
        logger.info(f"테스트 정확도: {test_accuracy:.4f}")
        return results
    
    def save_model(self, save_path):
        """모델 저장"""
        # 모델 저장 (pickle 사용)
        with open(f"{save_path}_model.pkl", 'wb') as f:
            pickle.dump(self.model, f)
        
        # K-means 모델도 저장 (있는 경우)
        if self.kmeans is not None:
            with open(f"{save_path}_kmeans.pkl", 'wb') as f:
                pickle.dump(self.kmeans, f)
        
        # 설정 저장
        with open(f"{save_path}_config.json", 'w') as f:
            json.dump(self.config, f, indent=2)
        
        print(f"💾 모델 저장 완료: {save_path}")
        logger.info(f"모델 저장 완료: {save_path}")
    
    def load_model(self, save_path):
        """모델 로드"""
        # 모델 로드
        with open(f"{save_path}_model.pkl", 'rb') as f:
            self.model = pickle.load(f)
        
        # K-means 로드 (있는 경우)
        kmeans_path = f"{save_path}_kmeans.pkl"
        if os.path.exists(kmeans_path):
            with open(kmeans_path, 'rb') as f:
                self.kmeans = pickle.load(f)
        
        # 설정 로드
        with open(f"{save_path}_config.json", 'r') as f:
            self.config = json.load(f)
        
        self.is_fitted = True
        print(f"📂 모델 로드 완료: {save_path}")
        logger.info(f"모델 로드 완료: {save_path}")


class M4ModelEvaluator:
    """M4 Mac 최적화 평가기"""
    
    def __init__(self, save_plots=True):
        self.save_plots = save_plots
        self.plot_dir = "m4_model_plots"
        
        if save_plots and not os.path.exists(self.plot_dir):
            os.makedirs(self.plot_dir)
        
        print(f"📈 M4 Mac 평가기 초기화 (그래프 저장: {save_plots})")
    
    def evaluate_model(self, model, X_test, y_test):
        """전체 평가 수행"""
        # 예측
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)
        
        # 평가 지표 계산
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        print(f"✅ 정확도: {accuracy:.4f}")
        print(f"   정밀도: {report['macro avg']['precision']:.4f}")
        print(f"   재현율: {report['macro avg']['recall']:.4f}")
        print(f"   F1점수: {report['macro avg']['f1-score']:.4f}")
        
        # 시각화
        try:
            self.plot_confusion_matrix(y_test, y_pred)
            self.plot_class_distribution(y_test, y_pred)
            self.plot_metrics(report)
            
        except Exception as e:
            print(f"⚠️  시각화 오류 (무시): {e}")
        
        return {
            'accuracy': accuracy,
            'classification_report': report,
            'total_samples': len(y_test),
            'num_classes': len(np.unique(y_test))
        }
    
    def plot_confusion_matrix(self, y_true, y_pred):
        """혼동 행렬 그래프"""
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar_kws={'shrink': 0.8})
        plt.title('Confusion Matrix (M4 Mac)', fontsize=14, fontweight='bold')
        plt.xlabel('Predicted Label')
        plt.ylabel('True Label')
        
        if self.save_plots:
            plt.savefig(f"{self.plot_dir}/confusion_matrix.png", dpi=150, bbox_inches='tight')
            print(f"   💾 혼동 행렬 저장됨")
        
        plt.show()
        plt.close()
    
    def plot_class_distribution(self, y_true, y_pred):
        """클래스 분포 비교"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 실제 분포
        unique_true, counts_true = np.unique(y_true, return_counts=True)
        ax1.pie(counts_true, labels=[f'Class {i}' for i in unique_true], 
               autopct='%1.1f%%', startangle=90)
        ax1.set_title('True Label Distribution', fontweight='bold')
        
        # 예측 분포
        unique_pred, counts_pred = np.unique(y_pred, return_counts=True)
        ax2.pie(counts_pred, labels=[f'Class {i}' for i in unique_pred], 
               autopct='%1.1f%%', startangle=90)
        ax2.set_title('Predicted Label Distribution', fontweight='bold')
        
        plt.suptitle('Class Distribution Comparison (M4 Mac)', fontsize=16, fontweight='bold')
        
        if self.save_plots:
            plt.savefig(f"{self.plot_dir}/class_distribution.png", dpi=150, bbox_inches='tight')
            print(f"   💾 클래스 분포 저장됨")
        
        plt.show()
        plt.close()
    
    def plot_metrics(self, report):
        """평가 지표 막대 그래프"""
        metrics = ['precision', 'recall', 'f1-score']
        values = [report['macro avg'][metric] for metric in metrics]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(metrics, values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.8)
        
        # 값 표시
        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        
        plt.title('Model Performance Metrics (M4 Mac)', fontsize=14, fontweight='bold')
        plt.ylabel('Score')
        plt.ylim(0, 1)
        plt.grid(True, alpha=0.3)
        
        if self.save_plots:
            plt.savefig(f"{self.plot_dir}/metrics.png", dpi=150, bbox_inches='tight')
            print(f"   💾 성능 지표 저장됨")
        
        plt.show()
        plt.close()


# 사용 예시 및 테스트
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🚀 M4 모델 모듈 테스트 시작!")
    
    # 더미 임베딩 데이터 생성 (테스트용)
    print("🔧 테스트 임베딩 데이터 생성...")
    dummy_embeddings = np.random.randn(100, 512)  # 100개 샘플, 512차원
    dummy_labels = np.random.randint(0, 5, 100)   # 5개 클래스
    
    # 모델 초기화
    model = M4TransformerModel()
    
    # 데이터 준비
    X_train, X_test, y_train, y_test = model.prepare_data(
        dummy_embeddings, dummy_labels
    )
    
    # 훈련
    model.train(X_train, y_train, X_test, y_test)
    
    # 평가
    results = model.evaluate(X_test, y_test)
    print("\n📊 평가 결과:", results)
    
    # 평가기 사용
    evaluator = M4ModelEvaluator(save_plots=True)
    detailed_results = evaluator.evaluate_model(model, X_test, y_test)
    
    # 모델 저장
    model.save_model("m4_test_model")
    
    print("\n🎉 M4 모델 모듈 테스트 완료!")
    
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# import numpy as np
# import pickle
# import logging
# from sklearn.model_selection import train_test_split
# from sklearn.cluster import KMeans
# import json
# from datetime import datetime
# import os

# logger = logging.getLogger(__name__)


# class TransformerModel:
#     """임베딩 데이터로 트랜스포머 모델 학습"""
    
#     def __init__(self, embedding_dim=512, num_heads=8, ff_dim=2048, num_layers=4):
#         """모델 설정 초기화"""
#         self.embedding_dim = embedding_dim
#         self.num_heads = num_heads
#         self.ff_dim = ff_dim
#         self.num_layers = num_layers
#         self.model = None
#         self.history = None
    
#     def load_embeddings(self, embeddings_path, data_path=None):
#         """저장된 임베딩 데이터 로드"""
#         embeddings = np.load(embeddings_path)
#         logger.info(f"임베딩 로드: {embeddings.shape}")
        
#         metadata = None
#         if data_path and os.path.exists(data_path):
#             with open(data_path, 'rb') as f:
#                 metadata = pickle.load(f)
#             logger.info(f"메타데이터 로드: {len(metadata['texts'])}개")
        
#         return embeddings, metadata
    
#     def create_transformer_block(self, embed_dim, num_heads, ff_dim):
#         """트랜스포머 블록 생성"""
#         inputs = layers.Input(shape=(None, embed_dim))
        
#         # Multi-Head Attention : 문장 내 단어들 간의 관계 학습
#         attention = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
#         attention_output = attention(inputs, inputs) #self-atteintion : 자기 자신과 어텐션
#         attention_output = layers.Dropout(0.1)(attention_output)
#         out1 = layers.LayerNormalization()(inputs + attention_output)
        
#         # Feed Forward Network
#         #확장: "이 문장에 대해 여러 각도로 생각해보자" (더 많은 뉴런 활용)
#         #ReLU: "필요 없는 생각은 버리자" (음수 제거)
#         #압축: "핵심만 정리해서 결론내자" (원래 크기로)
#         # 512 > 2048 ,  ReLU 활성화 함수: 음수는 0, 양수는 그대로
#         ffn_output = layers.Dense(ff_dim, activation="relu")(out1)
#         # 2048 > 512, 활성화 함수 없이 선형 변환
#         ffn_output = layers.Dense(embed_dim)(ffn_output)
#         ffn_output = layers.Dropout(0.1)(ffn_output)
#         out2 = layers.LayerNormalization()(out1 + ffn_output)
        
#         return keras.Model(inputs=inputs, outputs=out2)
    
#     def build_model(self, num_classes):
#         """전체 모델 구성"""
#         inputs = layers.Input(shape=(1, self.embedding_dim))
        
#         # 트랜스포머 블록들
#         x = inputs
#         for _ in range(self.num_layers):
#             transformer = self.create_transformer_block(
#                 self.embedding_dim, self.num_heads, self.ff_dim
#             )
#             x = transformer(x)
        
#         # 분류 헤드
#         x = layers.GlobalAveragePooling1D()(x)
#         x = layers.Dropout(0.1)(x)
#         x = layers.Dense(512, activation="relu")(x)
#         x = layers.Dropout(0.1)(x)
#         outputs = layers.Dense(num_classes, activation="softmax")(x)
        
#         self.model = keras.Model(inputs=inputs, outputs=outputs)
        
#         # 컴파일
#         self.model.compile(
#             optimizer=keras.optimizers.Adam(learning_rate=1e-4),
#             loss="sparse_categorical_crossentropy",
#             metrics=["accuracy"]
#         )
        
#         logger.info(f"모델 구성 완료 - 파라미터: {self.model.count_params():,}개")
    
#     def prepare_data(self, embeddings, labels=None, test_size=0.2):
#         """학습 데이터 준비"""
#         # 임베딩을 (batch, 1, dim) 형태로 변환
#         X = embeddings.reshape(embeddings.shape[0], 1, embeddings.shape[1])
        
#         # 라벨이 없으면 클러스터링으로 생성
#         if labels is None:
#             n_clusters = min(10, len(X) // 10)
#             kmeans = KMeans(n_clusters=n_clusters, random_state=42)
#             labels = kmeans.fit_predict(embeddings)
#             logger.info(f"클러스터링으로 {n_clusters}개 클래스 생성")
        
#         # 데이터 분할
#         X_train, X_test, y_train, y_test = train_test_split(
#             X, labels, test_size=test_size, random_state=42, stratify=labels
#         )
        
#         logger.info(f"훈련: {X_train.shape[0]}개, 테스트: {X_test.shape[0]}개")
#         return X_train, X_test, y_train, y_test
    
#     def train(self, X_train, y_train, X_test=None, y_test=None, epochs=50, batch_size=32):
#         """모델 훈련"""
#         if self.model is None:
#             num_classes = len(np.unique(y_train))
#             self.build_model(num_classes)
        
#         # 콜백 설정
#         callbacks = [
#             keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
#             keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5)
#         ]
        
#         validation_data = (X_test, y_test) if X_test is not None else None
        
#         logger.info("모델 훈련 시작...")
#         self.history = self.model.fit(
#             X_train, y_train,
#             batch_size=batch_size,
#             epochs=epochs,
#             validation_data=validation_data,
#             callbacks=callbacks,
#             verbose=1
#         )
#         logger.info("훈련 완료")
    
#     def evaluate(self, X_test, y_test):
#         """모델 평가"""
#         test_loss, test_accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        
#         predictions = self.model.predict(X_test, verbose=0)
#         predicted_classes = np.argmax(predictions, axis=1)
        
#         from sklearn.metrics import classification_report
#         report = classification_report(y_test, predicted_classes, output_dict=True)
        
#         results = {
#             'test_loss': float(test_loss),
#             'test_accuracy': float(test_accuracy),
#             'classification_report': report
#         }
        
#         logger.info(f"테스트 정확도: {test_accuracy:.4f}")
#         return results
    
#     def save_model(self, save_path):
#         """모델 저장"""
#         self.model.save(f"{save_path}_model.h5")
        
#         config = {
#             'embedding_dim': self.embedding_dim,
#             'num_heads': self.num_heads,
#             'ff_dim': self.ff_dim,
#             'num_layers': self.num_layers,
#             'timestamp': datetime.now().isoformat()
#         }
        
#         with open(f"{save_path}_config.json", 'w') as f:
#             json.dump(config, f, indent=2)
        
#         logger.info(f"모델 저장 완료: {save_path}")


# # 사용 예시
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
    
#     # 모델 초기화
#     model = TransformerModel()
    
#     # 데이터 로드
#     embeddings, metadata = model.load_embeddings(
#         "training_embeddings_embeddings.npy",
#         "training_embeddings_data.pkl"
#     )
    
#     # 데이터 준비
#     X_train, X_test, y_train, y_test = model.prepare_data(embeddings)
    
#     # 훈련
#     model.train(X_train, y_train, X_test, y_test)
    
#     # 평가
#     results = model.evaluate(X_test, y_test)
#     print("평가 결과:", results)
    
#     # 저장
#     model.save_model("trained_transformer")
