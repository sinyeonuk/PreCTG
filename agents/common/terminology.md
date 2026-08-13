# Terminology

This document defines shared Korean terminology for user interfaces and human-facing project documentation.

## General Principles

- Treat this document as a default glossary rather than an exhaustive dictionary.
- Use one preferred term consistently for the same concept within an interface or document set.
- Follow official project and product terminology when it is clearly established.
- Choose terminology for the intended audience rather than exposing internal implementation vocabulary by default.
- Prefer natural, direct Korean over unnecessary English, awkward literal translation, or mixed-language prose.
- Preserve code, commands, file paths, literal identifiers, product names, trademarks, and technical terms when translation would reduce accuracy.
- Do not ask the user to choose routine terminology when project context, nearby content, this glossary, or natural Korean provides a clear answer.

## Choosing an Unlisted Term

When this glossary does not list a term, decide in this order:

1. Use the project's official product terminology or explicit project instruction.
2. Follow the established term used consistently by comparable UI or documentation in the same project.
3. Choose the term most natural and precise for the intended audience.
4. Prefer a Korean expression for general users when an English technical term adds no useful precision.
5. Record a project-specific term when the choice will recur or represents a product concept.

- Make a reasonable choice and proceed when the decision is low risk and easy to revise.
- Ask only when competing terms imply materially different product concepts, permissions, behavior, legal meaning, or user expectations.
- When nearby usage is inconsistent, choose the clearest suitable term for the current scope and avoid broad unrelated rewrites.

## Audience-Specific Language

- Use `디렉토리`, `저장소`, `매개변수`, and other precise development terms in developer documentation when they describe actual technical concepts.
- Use `폴더`, `정보`, `입력값`, and task-oriented language in general-user interfaces when the technical distinction is unnecessary.
- Use technical terminology in developer tools, diagnostic views, and expert workflows when it is part of the user's task.
- Explain a necessary technical term on first use when the intended reader may not know it.
- Do not simplify a term so far that it becomes inaccurate or prevents the reader from taking the correct action.

## Language Consistency

- Use one primary language within the same interface or document context unless the product intentionally provides bilingual content.
- Do not insert untranslated general words into otherwise localized prose when a natural Korean term communicates the meaning accurately.
- Translate ordinary actions, states, instructions, headings, and explanatory terms into the selected language.
- Preserve another language for proper names, product names, trademarks, code, commands, literal identifiers, user-provided content, or deliberately untranslated technical terms.
- Follow the existing project convention when deciding whether a technical term is translated, transliterated, or retained.
- Do not alternate translated and untranslated forms merely for variety.
- When bilingual presentation is intentional, apply it consistently with a documented audience and purpose rather than mixing languages opportunistically within sentences.

## Standard Korean Terms

These defaults apply to Korean UI and human-facing documentation unless a project-specific convention requires otherwise.

| Preferred | Avoid or distinguish | Audience or usage |
|---|---|---|
| 프론트엔드 | 프런트엔드, 프론트 엔드 | 프론트엔드 개발 영역 |
| 백엔드 | 백 엔드 | 백엔드 개발 영역 |
| 디렉토리 | 디렉터리 | 개발자 문서의 파일 시스템 구조 |
| 폴더 | 디렉토리 | 일반 사용자 UI와 안내 문서 |
| 애플리케이션 | 어플리케이션 | 기술·공식 문서; 일반 UI에서는 `앱` 사용 가능 |
| 웹사이트 | 웹 사이트 | 웹 서비스와 사이트 |
| 이메일 | 이 메일, E-mail | 이메일과 이메일 주소 |
| 비밀번호 | 패스워드 | 인증 UI와 사용자 문서 |
| 사용자 | 유저 | 일반 제품 문맥; 게임 등 공식 용어가 `유저`인 경우 예외 |
| 사용자 이름 | 유저네임, username | 사용자에게 표시하거나 로그인에 사용하는 이름 |
| 아이디 | ID, 계정명 혼용 | 로그인용 아이디 |
| 식별자 | 아이디 | 내부 객체를 구분하는 identifier |
| 로그인 | 로그 인, sign in | 인증 행동 |
| 로그아웃 | 로그 아웃, sign out | 인증 종료 행동 |
| 회원가입 | 회원 가입, 사인업 | 계정 생성 행동 |
| 체크박스 | 체크 박스 | UI 컴포넌트 |
| 드롭다운 | 드롭 다운 | UI 컴포넌트 |
| 사이드바 | 사이드 바 | UI 영역 |
| 툴팁 | 툴 팁 | UI 보조 설명 |
| 팝업 | 팝 업 | 별도 팝업 문맥; 모달과 구분 |
| 대시보드 | 대쉬보드 | 정보 요약 화면 |
| 워크플로 | 워크플로우 | 작업 흐름 |
| 프레임워크 | 프레임웍 | 개발자 문서 |
| 라이브러리 | 패키지와 무분별한 혼용 | 재사용 가능한 코드 기능을 설명하는 개발 문맥 |
| 컴포넌트 | 컴퍼넌트 | UI와 소프트웨어 구성 요소 |
| 사용자 인터페이스 | 인터페이스 단독 사용 | 사용자와 시스템이 상호작용하는 UI 문맥 |
| 소프트웨어 인터페이스 | 인터페이스 단독 사용 | 모듈·API 사이의 계약을 설명하는 개발 문맥 |
| 플러그인 | 플러그 인 | 확장 기능 |
| 템플릿 | 탬플릿 | 재사용 양식 |
| 리팩토링 | 리팩터링 혼용 | 동작을 유지하는 코드 구조 개선 |
| 저장소 | 리포지토리, 레포지토리 혼용 | 일반 한국어 개발 문서; 고유 제품 용어는 유지 |
| 브랜치 | 가지 | Git 브랜치 |
| 커밋 | 커미트 | Git 커밋 |
| 병합 | 머지 혼용 | 일반 설명; 정확한 명령은 `merge` 유지 |
| 풀 리퀘스트 | 풀리퀘스트 | 처음에는 `풀 리퀘스트(PR)` 사용 가능 |
| 릴리스 | 릴리즈 | 버전 공개와 배포 단위 |
| 라이선스 | 라이센스 | 사용·배포 권한 |
| 배포 | 디플로이 | 서비스 또는 결과물 배포 |
| 빌드 | 구축 | 소프트웨어 빌드 |
| 오류 | 에러 혼용 | 일반 오류 설명과 사용자 메시지 |
| 오류 메시지 | 에러 메시지 | 오류 안내 문구 |
| 버그 | 오류 혼용 | 개발 결함을 지칭할 때 사용 |
| 문제 | 예외, 내부 오류명 | 일반 사용자에게 기술적 원인이 불필요한 경우 |
| 설정 | Configuration | 사용자가 변경하는 값 |
| 구성 | 설정 혼용 | 시스템 요소의 조합과 기술적 configuration |
| 선택 항목 | 옵션 남용 | 일반 사용자 UI에서 자연스러울 때 |
| 입력값 | 파라미터 | 일반 사용자 문맥 |
| 매개변수 | 파라미터 | 개발자 문서 |
| 정보 | 데이터 남용 | 일반 사용자 문맥에서 자연스러울 때 |
| 데이터 | 자료 혼용 | 분석·저장·처리 대상의 기술적 문맥 |
| 접근 권한 | 액세스 권한 | 권한 안내 |
| 알림 | 노티피케이션 | 사용자 알림 |
| 모달 | 팝업 혼용 | 개발·디자인 문서의 modal UI |
| 대화상자 | 모달 | 일반 사용자 안내에서 창의 역할을 설명할 때 |
| 실행 취소 | Undo, 되돌리기 혼용 | 이미 수행한 작업을 되돌리는 행동 |
| 다시 시도 | 재시도 | 일반 사용자 버튼과 안내 |
| 재시도 | 다시 시도 혼용 | 개발자 문서의 retry 동작 |
| 불러오는 중 | 로딩 중 | 일반 사용자 진행 상태 |
| 처리 중 | 프로세싱 중 | 더 구체적인 사용자 행동을 표현할 수 없을 때 |

## Concept Distinctions

### Delete and Remove

- Use `삭제` when data or an object is permanently deleted.
- Use `제거` when an item is detached from a list, relationship, selection, or view while the underlying object may remain.

### Cancel and Undo

- Use `취소` to stop an action that has not completed.
- Use `실행 취소` to reverse an action that has already completed.

### Save and Apply

- Use `저장` when values are persisted.
- Use `적용` when settings take effect in the current system or view.
- Explain the distinction when the product exposes both actions.

### Error, Problem, and Bug

- Use `오류` for a defined failure state.
- Use `문제` when a general user does not need the technical cause.
- Use `버그` for a product or implementation defect in developer-facing contexts.

### Settings and Configuration

- Use `설정` for values a user can change.
- Use `구성` for the arrangement of system elements or a technical configuration.

### Account and Object Identity

- Use `아이디` for a user-facing login identifier when the product uses that concept.
- Use `식별자` for an internal or technical identifier.
- Do not expose an internal identifier as `아이디` when users could mistake it for account information.

## Style Patterns

- Prefer `저장했습니다.` over `성공적으로 저장했습니다.` when success is already clear.
- Prefer `저장합니다.` over `저장을 진행합니다.`.
- Prefer `삭제합니다.` over `삭제를 수행합니다.`.
- Prefer `문제가 발생했습니다.` over `문제가 발생하였습니다.` in ordinary product language.
- Prefer `확인해 주세요.` over `확인 부탁드립니다.` for a direct instruction.
- Prefer `다시 시도해 주세요.` over `재시도를 진행해 주세요.` in general-user UI.
- Omit demonstratives such as `해당` when the referenced object is already clear.
- Prefer `진행 중입니다.` over `현재 진행 중에 있습니다.`.
- Avoid unnecessary `~할 수 있습니다` when a direct action or statement is clearer.

## Project-Specific Terminology

- Put recurring product names, domain concepts, roles, permission levels, and intentional deviations in a dedicated project instruction file when the project needs them.
- Explain the concept and usage boundary rather than listing a preferred word without context.
- Keep project-specific terminology consistent with actual product copy, schemas, APIs, and documentation where applicable.
- Treat project terminology as a scoped specialization of this glossary, following the precedence rules in the root `AGENTS.md`.

## Maintenance

- Add a term when inconsistent wording recurs or when a distinction affects user understanding or implementation decisions.
- Do not add every ordinary word to the glossary.
- Update affected UI and documentation within the current task's scope when establishing a preferred term.
- Do not rewrite unrelated content solely to replace an understandable existing term.
- Remove or revise a glossary entry when product terminology changes.

## Verification

- Compare new or changed terms with nearby UI, documentation, product instructions, and this glossary.
- Check that the same concept uses one term and distinct concepts are not collapsed into one label.
- Confirm audience-specific technical language remains understandable and accurate.
- Confirm Korean prose avoids unnecessary language mixing and unnatural literal translation.
