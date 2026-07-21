# SCM 에이전트 아키텍처

## 목적

이 에이전트는 SCM 관련 CSV 데이터를 분석해서, 사용자가 바로 읽을 수 있는 짧은 답변으로 바꿉니다.

핵심 설계는 다음과 같습니다.

- 먼저 로컬에서 계산한다
- 결과만 작게 모델에 보낸다
- 모델은 해석과 표현만 담당한다

## 설계 개념

에이전트는 세 계층으로 나뉩니다.

1. 대화 계층
   - 사용자 질문을 받는다
   - 질문을 GPT-4o mini에 보낸다
   - 대화 루프를 관리한다

2. 도구 계층
   - 날짜별 매출 조회, 주간 지표 같은 결정적 함수를 노출한다
   - 모델이 원본 CSV를 직접 읽지 않고 함수만 고르게 한다

3. 계산 계층
   - `data/`의 CSV를 읽는다
   - 행을 주간 또는 날짜 단위로 집계한다
   - 작은 결과만 돌려준다

## 구조

```text
C:\pyproject\ai
- scm_agent.py
- compute/
  - cli.py
  - scm_metrics.py
- data/
  - retail_store_sales_promotions_demand.csv
- docs/
  - scm-agent-architecture.md
- memory/
- skills/
- config/
```

## 실행 흐름

```text
사용자 질문
  -> scm_agent.py
  -> OpenAI Responses API
  -> 도구 선택
  -> compute/scm_metrics.py
  -> 작은 결과
  -> GPT-4o mini 최종 응답
```

## 시퀀스

### 날짜별 판매금액 질문

```text
사용자: "2024-12-23 일 판매금액 합산해줘"
에이전트: 날짜 추출
에이전트: sales_amount_for_date 호출
계산: 2024-12-23의 price * units_sold 합산
모델: 한 줄 표로 응답
```

### 주간 요약 질문

```text
사용자: "주간 요약 보여줘"
에이전트: weekly_metrics 호출
계산: 주간 단위로 매출, 수요, 공급 집계
모델: 주간 표로 응답
```

## 왜 이런 구조인가

- 토큰 사용량을 줄일 수 있다
- 전체 CSV를 모델에 보내지 않아도 된다
- 계산을 결정적으로 만들 수 있다
- 나중에 ChatGPT나 Claude에 붙이기 쉽다

## 개발자 메모

- `memory/`에는 의미와 기준을 남긴다
- `skills/`에는 재사용 가능한 작업 규칙을 남긴다
- `compute/`에는 결정적 계산 코드를 둔다
- `scm_agent.py`는 대화와 도구 사용을 조정한다

