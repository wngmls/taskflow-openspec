## Context

Tailwind CSS CDN 환경에서 다크모드를 구현한다. Tailwind의 `darkMode: 'class'` 전략을 사용해 `<html>` 태그에 `dark` 클래스를 토글하는 방식으로 구현한다.

## Goals / Non-Goals

**Goals:**
- 모든 화면 다크/라이트 전환
- localStorage 설정 유지
- OS 기본값 존중 (저장값 없을 때)
- 헤더 토글 버튼 (☀️ / 🌙)

**Non-Goals:**
- 시스템 테마 변경 감지 실시간 반영 (페이지 로드 시 1회만 체크)
- 컴포넌트별 테마 분리

## Decisions

### D1: Tailwind class 전략
`<html class="dark">` 토글 방식. CDN 환경에서 `tailwind.config` 설정이 불가하므로 inline config 주입:
```html
<script>tailwind.config = { darkMode: 'class' }</script>
```
이 스크립트를 `tailwind.config` 이후, body 이전에 삽입.

### D2: theme.js 공통 모듈
모든 페이지가 공유하는 `/js/theme.js`:
- 페이지 로드 시 저장된 테마 또는 OS 기본값 즉시 적용 (FOUC 방지를 위해 `<head>` 최상단)
- `toggleTheme()` 함수 export

### D3: 토글 버튼 위치
헤더 우측 로그아웃 버튼 옆. 로그인/회원가입 화면은 카드 우상단 절대 위치.

### D4: 다크 색상 팔레트
| 요소 | 라이트 | 다크 |
|------|--------|------|
| 배경 | `bg-gray-50` | `dark:bg-gray-900` |
| 카드/패널 | `bg-white` | `dark:bg-gray-800` |
| 텍스트 주 | `text-gray-800` | `dark:text-gray-100` |
| 텍스트 부 | `text-gray-500` | `dark:text-gray-400` |
| 보더 | `border-gray-200` | `dark:border-gray-700` |
| 입력 필드 | `bg-white border-gray-300` | `dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100` |
| 칸반 TODO | `bg-amber-50` | `dark:bg-amber-900/20` |
| 칸반 DOING | `bg-blue-50` | `dark:bg-blue-900/20` |
| 칸반 DONE | `bg-green-50` | `dark:bg-green-900/20` |

## Risks / Trade-offs

- [FOUC] 다크모드 적용 전 잠깐 라이트 화면 보임 → Mitigation: `theme.js`를 `<head>` 최상단에 인라인으로 삽입
- [Tailwind CDN purge] `dark:` 클래스가 purge되지 않음 → CDN은 전체 클래스 포함이므로 문제없음
