# Smart Summary Bot

## 🤖 프로젝트 개요 (Project Overview)

이 프로젝트는 뉴스 기사를 자동으로 요약하고, 사용자가 요약된 내용을 웹 인터페이스를 통해 편리하게 확인할 수 있도록 지원하는 지능형 뉴스 요약 봇입니다. 각 기능이 독립적인 모듈로 구성되어 있어 효율적인 개발과 유지보수가 가능합니다.

-----

### 📂 프로젝트 구조 (Project Structure)

프로젝트는 모듈별로 깔끔하게 분리된 디렉터리 구조를 갖습니다.

```
/smart_summary_bot
├── crawler/
│   └── crawler.py        # 뉴스 기사 데이터 수집
├── preprocessor/
│   └── preprocess.py     # 데이터 전처리
├── answer/
│   └── summarizer.py     # LLM API를 활용한 요약 생성
├── embedder/
│   └── embed.py          # 텍스트 임베딩 (추가)
├── modeler/
│   └── model.py          # 모델 학습 및 저장
├── evaluator/
│   └── evaluate.py       # 모델 성능 평가
├── server/
│   └── app.py            # 웹 서버
├── web/
│   └── static/
│   └── templates/        # 웹 인터페이스
├── main.py               # 전체 워크플로우 진입점
└── requirements.txt
```

-----

### ✨ 주요 기능 (Key Features)

  * **`crawler/`**: 지정된 뉴스 웹사이트에서 기사 데이터를 수집하여 CSV 파일로 출력합니다.
  * **`preprocessor/`**: 크롤링된 CSV 파일을 모델 학습에 적합한 형태로 변환하고, 전처리된 데이터를 CSV로 저장합니다.
  * **`answer/`**: **LLM(대규모 언어 모델) API**를 활용하여 전처리된 기사 본문을 요약하고, 요약된 내용을 원본 데이터에 추가합니다.
  * **`modeler/`**: 전처리된 데이터를 기반으로 모델을 학습하고, 학습된 모델 파일을 저장합니다. 다양한 모델을 테스트할 수 있도록 코드를 유연하게 설계합니다.
  * **`evaluator/`**: 학습된 모델의 성능을 평가합니다. 모델의 추론 결과와 사람이 작성한 정답지(요약본)를 비교하여 **ROUGE 스코어**와 같은 지표를 계산하고 결과를 파일로 저장합니다.
  * **`main.py`**: 위 모든 모듈을 순차적으로 호출하여 전체 데이터 파이프라인(수집 → 전처리 → 학습 → 평가)을 실행하는 단일 진입점 역할을 합니다.
  * **`server/` & `web/`**: `server/app.py`는 **Flask**와 같은 프레임워크를 사용하여 사용자에게 요약된 뉴스를 제공하는 API를 구현합니다. `web/` 디렉터리는 사용자 인터페이스를 구성하는 HTML, CSS, JavaScript 파일을 포함합니다.

-----

### 🚀 시작하기 (Getting Started)

#### 1\. 설치 (Installation)

프로젝트에 필요한 모든 라이브러리는 `requirements.txt`에 명시되어 있습니다. 아래 명령어를 실행하여 의존성을 설치할 수 있습니다.

```sh
pip install -r requirements.txt
```

#### 2\. 실행 (Execution)

프로젝트의 전체 워크플로우를 실행하려면 `main.py` 스크립트를 실행하면 됩니다.

```sh
python main.py
```

이 스크립트는 설정에 따라 크롤링부터 모델 학습 및 평가까지의 모든 과정을 자동으로 처리합니다.

-----

### 🤝 기여 (Contribution)

이 프로젝트는 협업을 통해 더욱 발전할 수 있습니다. 각 모듈의 기능 구현에 대한 기여는 언제나 환영합니다.
