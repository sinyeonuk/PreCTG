# UI 지침 안내

이 디렉토리에는 모든 프로젝트에 적용되는 UI·UX 에이전트 지침을 책임별로 나누어 둡니다.

이 README는 개발자가 UI 지침의 구성과 담당 영역을 이해하기 위한 사람용 인덱스입니다. 독립적인 에이전트 규칙이나 예외를 정의하지 않습니다. 설명이 실제 지침 파일과 다르면 해당 지침 파일을 기준으로 판단하고 이 README를 수정해야 합니다.

## 지침 목록

| 파일 | 관련 영역 | 주요 연결 문서 | 설명 |
|---|---|---|---|
| `accessibility.md` | 접근성과 적응형 화면 | `foundations.md`, `verification.md` | 시맨틱 구조, 키보드·초점, 보조 기술, 확대, 입력 방식과 적응형 화면 원칙을 정의합니다. |
| `content.md` | UI 정보와 문구 | `agents/common/terminology.md`, `verification.md` | 정보 밀도, 데이터 표현, 사용자 관점의 문구, 목소리, 용어와 현지화를 정의합니다. |
| `foundations.md` | UI 방향과 완성도 | `interaction.md`, `accessibility.md`, `verification.md` | 사용자와 사용 환경, UI 판단 우선순위, 구현 수준, 기존 화면 조사, 디자인 방향과 컴포넌트 체계를 정의합니다. |
| `interaction.md` | 흐름과 상호작용 | `foundations.md`, `verification.md` | 사용자 흐름, 탐색 스택, 비동기 작업과 복구, 폼, 상태와 피드백을 정의합니다. |
| `verification.md` | UI 검증과 전달 | `agents/common/verification.md` | 렌더링, 비동기 복구, 접근성, 완료 후 탐색 스택, 탭, 상태와 문구의 확인 기준을 정의합니다. |

실제 적용 파일은 작업 영역에 따라 루트 `AGENTS.md`에서 선택합니다.
