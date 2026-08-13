# 공용 에이전트 지침 안내

이 디렉토리에는 모든 프로젝트에 기본으로 적용되는 에이전트 지침이 있습니다.

이 README는 개발자가 지침의 구성과 담당 영역을 이해하기 위한 안내 문서입니다. 독립적인 에이전트 규칙이나 예외를 정의하지 않습니다. 설명이 실제 지침 파일과 다르면 해당 지침 파일을 기준으로 판단하고 이 README를 수정해야 합니다.

## 지침 목록

| 파일 | 관련 영역 | 주요 연결 문서 | 설명 |
|---|---|---|---|
| `coding.md` | 코드 구현 | `constraints.md`, `project-structure.md`, `testing.md`, `verification.md` | 구현 방식, 의존성 선택, 함수, 오류 처리, 주석, 성능과 테스트 용이성에 관한 원칙입니다. |
| `communication.md` | 사용자 소통 | `constraints.md`, `task-impact.md`, `verification.md`, `workflow.md` | 질문 기준, 작업 영향도에 따른 진행 상황 공유, 완료 보고와 권고 사항의 표현 방식을 정의합니다. |
| `constraints.md` | 범위·권한·안전 | `coding.md`, `git.md`, `workflow.md` | 사용자 승인, 비용 없는 개발과 배포 제외 기본값, 작업 범위, 안전과 외부 작업의 경계를 정의합니다. |
| `data-and-privacy.md` | 데이터·개인정보 | `constraints.md`, `testing.md`, `verification.md` | 사용자 데이터, 외부 통신, 텔레메트리, 저장·삭제, 로그와 민감정보 처리 기준을 정의합니다. |
| `documentation.md` | 사람용 프로젝트 문서 | `communication.md`, `terminology.md`, `verification.md`, `workflow.md` | `docs/` 아래의 명세, 절차서, 체크리스트와 인수인계서 등 사람이 읽는 문서의 작성·관리 기준입니다. |
| `git.md` | Git 저장소 | `constraints.md` | 작업 트리 보호, 커밋, 브랜치, 이력, 원격 저장소, 줄바꿈 경고와 ignore 규칙을 정의합니다. |
| `instruction-authoring.md` | 에이전트 지침 관리 | 루트 `AGENTS.md`, `documentation.md` | 공용·프로젝트 지침의 책임과 구조, 프로젝트 지식의 지침 승격 기준, README 유지보수 방식을 정의합니다. |
| `project-bootstrap.md` | 프로젝트 최초 초기화 | `documentation.md`, `instruction-authoring.md`, `project-structure.md` | 복사한 베이스라인을 현재 프로젝트의 문서와 전용 지침으로 한 번 초기화하는 기준을 정의합니다. |
| `project-structure.md` | 파일·디렉토리 구조 | `constraints.md`, `documentation.md`, `git.md` | 파일과 디렉토리의 배치·이름, 모듈 경계, 공유 코드와 구조 변경 원칙을 정의합니다. |
| `quality-assurance.md` | 품질 보증·인수 검토 | `quality.md`, `testing.md`, `verification.md` | 요구사항과 위험에 따른 시나리오 선정, 탐색적 검사, 결함 판단과 완료 근거를 정의합니다. |
| `quality.md` | 완료 품질 | `coding.md`, `documentation.md`, `verification.md` | 정확성, 완결성, 신뢰성, 정리 상태와 완료 조건을 정의합니다. |
| `refactoring.md` | 리팩토링 | `coding.md`, `constraints.md`, `testing.md`, `verification.md` | 동작을 보존하면서 구조를 개선하기 위한 기준선 확보, 점진적 변경과 검증 절차를 정의합니다. |
| `task-impact.md` | 작업 영향도 | `communication.md`, `verification.md`, `workflow.md` | 사소함·국소적·중대함 또는 고위험 작업을 구분하고 절차 깊이를 결정하는 공통 기준입니다. |
| `terminology.md` | 한국어 용어 | `documentation.md`, `ui/content.md` | UI와 사람용 문서에서 사용할 기본 용어, 독자별 표현과 개념 구분 기준을 정의합니다. |
| `testing.md` | 테스트 작성 | `coding.md`, `quality.md`, `verification.md` | 블랙박스·화이트박스 관점, 테스트 계층과 경계, 테스트 더블, 결정성 및 유지보수 원칙을 정의합니다. |
| `ui/` | UI·UX | `communication.md`, `terminology.md`, `verification.md` | UI 방향, 상호작용, 접근성, 문구와 검증 지침을 책임별 파일로 나눈 정책 디렉토리입니다. |
| `verification.md` | 검증 | `communication.md`, `task-impact.md`, `testing.md`, `workflow.md` | 공통 작업 영향도에 비례한 검증 수준, 명세 완료 조건, 실행 순서와 실패 판별 기준을 정의합니다. |
| `workflow.md` | 작업 진행 | `communication.md`, `constraints.md`, `task-impact.md`, `documentation.md`, `verification.md` | 작업 유형과 영향도, 명세 우선 개발, 프로젝트 지침 축적, 표준 진행 과정과 차단 요인 처리를 정의합니다. |

## 디렉토리 관계

- `agents/common/`: 모든 프로젝트에 적용되며 일반 프로젝트 작업에서는 수정하지 않는 공용 기준선
- `agents/project/`: 현재 프로젝트의 규칙과 공용 기본값에 대한 예외를 기록하는 사용자화 영역
- `docs/`: 사용자가 읽을 프로젝트 설명, 절차서, 체크리스트와 인수인계 문서

우선순위와 상속 방식은 루트 `AGENTS.md`를 기준으로 합니다.

## 적용 방식

루트 `AGENTS.md`에 지정된 핵심 지침은 모든 작업에서 읽고, 나머지 지침은 작업 영역에 따라 선택해서 읽습니다. 여러 영역이 겹치면 해당 파일을 모두 적용합니다. 구체적인 선택 기준은 루트 `AGENTS.md`의 표를 확인하세요.
