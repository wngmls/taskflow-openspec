## ADDED Requirements

### Requirement: 테마 토글
시스템은 사용자가 다크모드와 라이트모드를 전환할 수 있어야 한다. 설정은 localStorage에 저장되며, 저장값이 없으면 OS의 `prefers-color-scheme`을 따른다.

#### Scenario: 다크모드 전환
- **WHEN** 사용자가 헤더의 🌙 버튼 클릭
- **THEN** 즉시 다크모드 적용(`<html class="dark">`), localStorage에 `theme=dark` 저장, 버튼이 ☀️로 변경

#### Scenario: 라이트모드 전환
- **WHEN** 사용자가 헤더의 ☀️ 버튼 클릭
- **THEN** 즉시 라이트모드 적용(`<html class="">`), localStorage에 `theme=light` 저장, 버튼이 🌙로 변경

#### Scenario: 설정 유지
- **WHEN** 다크모드 설정 후 페이지 새로고침
- **THEN** 다크모드가 유지됨 (FOUC 없이 즉시 적용)

#### Scenario: OS 기본값 적용
- **WHEN** localStorage에 theme 값이 없고 OS가 다크모드
- **THEN** 자동으로 다크모드 적용

#### Scenario: 모든 화면 적용
- **WHEN** 다크모드 활성 상태에서 어느 화면이든 로드
- **THEN** 배경, 카드, 텍스트, 입력 필드, 칸반 컬럼 등 모든 UI 요소가 다크 팔레트로 표시
