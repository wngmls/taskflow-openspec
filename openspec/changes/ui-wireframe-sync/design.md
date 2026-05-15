## Context

스토리보드 v2 와이어프레임과 초기 구현 사이에 UI 레이아웃 불일치가 발생했다. 기능 동작(API, DB)은 정상이나 시각적 요소(색상, 레이아웃, 컴포넌트 스타일)가 스펙에 정의되지 않아 임의 구현됐다. 이번 변경은 코드를 이미 수정 완료했으며, 해당 결정사항을 스펙으로 역방향 문서화(reverse-document)하는 것이 목적이다.

## Goals / Non-Goals

**Goals:**
- 스토리보드 v2 와이어프레임 기반 UI 요구사항을 스펙에 명시
- 향후 AI가 동일한 스펙으로 구현할 때 와이어프레임과 일치하는 결과 생성

**Non-Goals:**
- 새로운 기능 추가 없음
- API 또는 DB 스키마 변경 없음
- 모바일 반응형 세부 스펙 (별도 변경에서 다룰 수 있음)

## Decisions

### D1: Tailwind 유틸리티 클래스로 색상 표현
컬럼 색상은 `bg-amber-50`, `bg-blue-50`, `bg-green-50`으로, 텍스트는 각각 `text-amber-700`, `text-blue-700`, `text-green-700`으로 지정. CSS 변수나 커스텀 테마 대신 Tailwind CDN 빌드에서 바로 사용 가능한 기본 클래스 사용.

### D2: 헤더 탭은 `<a>` 태그 기반 버튼 스타일
SPA 라우팅 없이 HTML 페이지 이동이므로 `<a href>` 태그를 탭 버튼처럼 스타일링. Active 페이지는 `bg-teal-600 text-white`, 비활성은 `text-gray-600 hover:bg-gray-100`.

### D3: 인라인 입력 담당자 드롭다운은 런타임 멤버 로드
페이지 로드 시 `GET /teams/{id}/members` 호출 결과로 `<select>` 옵션을 동적 생성. 기본값은 현재 사용자(@me).

## Risks / Trade-offs

- [Tailwind CDN purge 미적용] 사용하지 않는 클래스 포함 → Mitigation: MVP 범위에서 번들 크기 허용
- [하드코딩된 색상 클래스] 테마 변경 어려움 → Mitigation: MVP 범위 외, 추후 CSS 변수로 추출 가능

## Migration Plan

이미 코드 수정 완료. 스펙 문서화만 남은 상태이므로 별도 배포 불필요.
