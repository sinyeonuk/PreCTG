# PreCTG 근거 자료 목록

이 문서는 PreCTG 명세와 향후 합성 데이터 생성에 사용하는 외부 출처, 사용 목적과 검증 상태를 관리합니다.

## 1. 출처 사용 원칙

- 대회 규정과 데이터 스키마는 공식 운영기관 페이지를 1차 출처로 사용한다.
- 임상 정의와 임계값은 전문기관 가이드라인 또는 동료평가 원문을 우선한다.
- 검색 결과 요약은 후보 탐색에만 사용하고 생성 규칙의 최종 근거로 사용하지 않는다.
- 외부 수치를 채택할 때 대상 인구, 측정 시점, 단위와 PreCTG 적용 한계를 함께 기록한다.
- 접근 제한 자료는 확인 가능한 공개 범위만 인용하고 보이지 않는 내용을 추정하지 않는다.

## 2. 현재 등록 출처

| ID | 출처 | 상태 | 현재 사용 목적 |
|---|---|---|---|
| `COMP-001` | [2026 K-Health 미개방 의료데이터 활용 경진대회](https://daker.ai/public/hackathons/2026-k-health-unreleased-data-utilization-competit) | 확인 | 일정, 제출 형식, 평가 항목, 안심존·반출·폐쇄망 제약 |
| `DATA-001` | [AIHub 태아 심박동 모니터링 데이터](https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=71366) | 확인 | 공식 데이터명, 공개 스키마, 코드, 건수와 집계 분포 |
| `PLAN-001` | `C:/Users/sinyeonuk/Downloads/기획안.pdf` | 확인 | 디버그랩 아이디어의 시의성·실현성·참신성·파급성 및 단계형 조기경보 방향 |
| `CLIN-001` | [ACOG Clinical Practice Guideline No. 10: Intrapartum Fetal Heart Rate Monitoring](https://www.acog.org/clinical/clinical-guidance/clinical-practice-guideline/articles/2025/10/intrapartum-fetal-heart-rate-monitoring-interpretation-and-management) | 부분 확인 | 최신 FHR 용어·3단계 범주와 관리 체계의 후보 기준; 전문은 접근 제한이 있어 상세 규칙 채택 전 원문 확인 필요 |
| `CLIN-002` | [ACOG Quality-Improvement Strategies for Safe Reduction of Primary Cesarean Birth](https://www.acog.org/clinical/clinical-guidance/committee-statement/articles/2025/04/quality-improvement-strategies-for-safe-reduction-of-primary-cesarean-birth) | 확인 | FHR 판독 변이와 표준 용어·교육 필요성의 배경 근거 |
| `CLIN-003` | [NICHD 2008 Electronic Fetal Monitoring Workshop historical report](https://www.nichd.nih.gov/sites/default/files/publications/pubs/documents/ppb_council_2008_historical.pdf) | 후보 | 3단계 FHR 분류의 역사적 원전 후보; 상세 규칙 사용 전 전문 검토 필요 |

## 3. 추가 확보가 필요한 근거

다음 항목은 구현 전에 원문과 적용 가능성을 확인해야 한다.

- ACOG/NICHD 기준의 baseline, variability, acceleration과 각 deceleration 정의
- Category I, II, III의 완전한 판정 조건과 충돌 우선순위
- 산모 고혈압, 임신성 당뇨, 전자간증, FGR, 태반 합병증과 응급 위험 사이의 방향·범위
- 한국 산모 연령, 임신 주수, 다태임신 및 주요 위험요인 분포
- AIHub 데이터 설명서에 있는 레코드 단위, 반복 측정 구조, `Emergency`, `CA`, `Abnormality`의 작성 시점과 정의
- 데이터안심존의 실제 Python·LightGBM 버전과 패키지·모델 반입 절차

## 4. 근거 채택 상태

- `후보`: 검색 또는 참고자료에서 발견했지만 원문과 적용 범위를 검토하지 않음
- `부분 확인`: 공식 자료의 공개 범위는 확인했으나 필요한 상세 정보가 접근 제한 또는 불완전함
- `확인`: 현재 문서에 사용한 사실을 공식 원문에서 확인함
- `승인`: 사용 범위에 맞는 검토를 완료함. 임상 규칙은 임상 검토 권한이 있는 검토자의 확인까지 필요하고, 합성 전용 가정은 팀 검토로 승인할 수 있음
- `기각`: 대상 인구, 시점, 정의 또는 품질이 맞지 않아 사용하지 않음

현재 등록된 임상 출처 중 구체적인 임상 계수나 임계값에 `승인`된 자료는 없다. 해당 값은 추가 조사와 적절한 검토 후 실행 구성에 반영한다. 기능 시연에 필요한 값은 `scope=synthetic_demo`로 분리하고 임상 승인 상태를 공유하지 않는다.
