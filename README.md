# PreCTG

PreCTG는 산모·태아 전자의료기록(EMR)과 분만 초기 태아 심박동 모니터링 정보를 단계적으로 결합해 위험 신호를 설명 가능한 형태로 제시하는 임상 의사결정 지원 MVP입니다.

이 저장소는 디버그랩 팀의 「2026 K-Health 미개방 의료데이터 활용 경진대회」 아이디어 제안서에 삽입할 실행 예시를 구현합니다. 현재 단계의 모델과 합성 데이터는 기능 확인용이며, 실제 임상 성능이나 안전성을 입증하지 않습니다.

## 현재 상태

- 단계: 합성 데이터 기반 MVP 구현 완료
- 공식 활용 데이터: AIHub 「태아 심박동 모니터링 데이터」
- 데이터 접근 상태: 원본 미확보
- 개발 데이터: 공개 메타데이터와 공신력 있는 근거를 사용해 생성할 합성 테스트 데이터
- 배포: 범위 밖이며 로컬 실행을 우선함

현재 입력 검증, 합성 데이터 생성, 합성 시연용 단계 규칙, LightGBM 학습·추론, CLI와 Streamlit 사용자 흐름이 동작합니다. 승인된 임상 규칙과 실제 데이터 성능 검증은 포함하지 않습니다.

## 개발 환경

Python 3.11 이상 환경에서 다음 순서로 준비합니다.

```powershell
python --version  # Python 3.11 이상인지 확인
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

시스템 기본 Python이 3.10 이하라면 먼저 Python 3.11 이상을 선택한 뒤 가상환경을 만듭니다. Python 버전이 맞지 않으면 고정된 NumPy 등 의존성을 설치할 수 없습니다.

주요 명령은 다음과 같습니다.

```powershell
prectg status
prectg generate --rows 50000 --output data/synthetic/prectg-synthetic.csv
prectg train --data data/synthetic/prectg-synthetic.csv --output models/prectg-demo.joblib
prectg predict --input data/fixtures/minimal-synthetic-input.json --model models/prectg-demo.joblib
prectg predict-batch --input data/synthetic/prectg-synthetic.csv --model models/prectg-demo.joblib --output outputs/batch-result.csv
python scripts/benchmark.py
python -m pytest
ruff check .
ruff format --check .
streamlit run app/streamlit_app.py
```

화면 데모는 모델 파일이 없어도 첫 분석 때 로컬 합성 데이터로 실제 LightGBM 모델을 준비합니다. 인터넷이나 외부 API를 사용하지 않습니다. 생성 데이터, 모델과 결과 파일은 Git에서 제외되며 위 명령으로 다시 만들 수 있습니다.

## 디렉토리 구조

```text
app/                 Streamlit 데모와 로컬 UI 자산
configs/             특성 시점과 합성 데이터 생성 설정
data/fixtures/       자동 테스트용 소형 합성 사례
scripts/             생성·학습·추론 명령 진입점
src/prectg/          스키마, 규칙, 특성, 모델과 통합 엔진
tests/               단위·계약·통합 테스트
docs/                제품·데이터·아키텍처 명세와 근거
agents/project/      PreCTG 전용 에이전트 지침
```

## 문서

프로젝트의 범위와 결정은 [프로젝트 문서 안내](docs/README.md)에서 시작합니다.

- [제품 명세](docs/product-spec.md): 대회, 기획안, 팀, 목표, 범위와 완료 조건
- [데이터 명세](docs/data-spec.md): 공식 데이터 구조, 누수 경계와 합성 데이터 계획
- [아키텍처 및 구현 계획](docs/architecture-and-delivery.md): 기술 스택, 처리 흐름, 단계별 구현과 RiskGate 활용
- [MVP 구현 및 수용 계획](docs/mvp-delivery-plan.md): 3단계 사용자 흐름, 화면별 UX·UI와 높은 완료 기준선
- [근거 자료 목록](docs/source-register.md): 외부 자료, 용도와 검증 상태
- [모델 카드](docs/model-card.md): 합성 모델의 목적, 입력, 검증과 한계
- [데모 및 인수 안내](docs/demo-and-handover.md): 발표 흐름, 벤치마크와 실제 데이터 전환 지점
- [완료 감사와 팀 확인표](docs/completion-audit.md): Gate별 기술 완료 증거와 별도의 팀 인수 항목

## 중요 제한

PreCTG 결과는 의료진의 진단이나 처치를 대체하지 않습니다. 합성 데이터로 얻은 정확도, F1 점수, AUC 등의 값은 실제 임상 성능으로 제시하지 않습니다. 실제 데이터 분석과 성능 검증은 대회 본선에서 승인된 의료데이터안심존 환경을 사용할 때 별도로 수행합니다.
