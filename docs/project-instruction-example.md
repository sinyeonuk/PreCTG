# 프로젝트 전용 지침 예시

이 문서는 `agents/project/`에 처음 지침을 추가하는 개발자에게 최소 구조와 책임 분리 방식을 보여주는 비규범적 예시입니다.

아래 예시는 실제 에이전트 지침이 아니며, 프로젝트에서 확인되지 않은 기술·명령·디렉토리를 그대로 복사하면 안 됩니다.

## 언제 파일을 추가하는가

프로젝트 전용 지침은 다음 조건을 모두 충족하는 정보가 있을 때 추가합니다.

- 현재 프로젝트에만 적용됩니다.
- 코드, 구성, 유지 문서 또는 사용자 결정으로 확인할 수 있습니다.
- 이후 작업에서도 반복적으로 에이전트의 판단에 영향을 줍니다.
- 실행 가능한 규칙, 제약, 명령 또는 책임 경계로 표현할 수 있습니다.

하나의 짧은 파일로 시작하고, 서로 다른 책임이 충분히 커졌을 때만 `development.md`, `architecture.md`, `ui.md`처럼 분리합니다.

## 지침 파일 예시

다음은 `agents/project/development.md`의 예시입니다.

```md
# Development

This document defines the confirmed development environment, commands, and generated-file boundaries for this project.

## Supported Environment

- Use the runtime version declared in `.tool-versions`.
- Use the package manager selected by the committed lockfile.

## Commands

- Run `example test command` for the maintained test suite.
- Run `example lint command` for source linting.

## Generated Files

- Do not edit `example/generated/` directly.
- Run `example generation command` after changing its source schema.
```

명령은 실제 프로젝트의 실행 가능한 구성에 있는 값으로 교체해야 합니다. 공용 지침을 반복해서 복사하지 말고, 프로젝트 차이와 확인된 구체화만 기록합니다.

## 공용 기본값 예외 예시

공용 규칙을 의도적으로 재정의할 때는 대상 기본값, 범위와 이유를 함께 씁니다.

```md
## Documentation Language Exception

The common documentation language default in `documentation.md` is overridden for `docs/public/`.

- Write files under `docs/public/` in English because they are published for an international developer audience.
```

권한, 안전, 정직성 경계처럼 프로젝트 지침이 약화할 수 없는 공용 제약에는 예외를 만들 수 없습니다.

## 인덱스 등록 예시

지침 파일을 추가한 뒤 `agents/project/README.md`에 실제 프로젝트 목적, 기준선 정보와 지침을 등록합니다.

```md
## 기준선 정보

- 버전: `0.1.0`
- 출처: 조직의 기준선 저장소와 가져온 커밋 또는 릴리스

## 지침 목록

| 파일 | 관련 영역 | 공용 지침과의 관계 | 설명 |
|---|---|---|---|
| `development.md` | 개발 환경과 명령 | 공용 워크플로 구체화 | 지원 환경, 검사 명령과 생성 파일 경계를 정의합니다. |
```

