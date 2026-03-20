# Backend Architecture (AWS Chalice + SQLModel)

## 1. 구조 설계 원칙
- **Serverless 최적화:** AWS Chalice 특성상 Cold Start를 줄이기 위해 전역 로드 최소화.
- **의존성 분리 (Separation of Concerns):** 라우터(Controller), 비즈니스 로직(Service), 데이터/ORM(Repository/CRUD) 분리.
- **공통 처리 로직 중앙화:** 예외 처리와 로깅을 미들웨어(Chalice Decorator 형식)로 공통화하여 일관된 API Spec 응답 보장.

## 2. 디렉토리 구조
```text
/backend
├── app.py                  # Chalice Application 엔트리포인트 (Blueprint 등록)
├── chalicelib/
│   ├── api/                # 블루프린트 라우터 정의 (도메인별 분리)
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── reservations.py
│   │   └── webhooks.py
│   ├── core/               # 시스템 코어 (설정, 디비 커넥션, 예외 처리기)
│   │   ├── config.py       # 환경변수(SSM/Secrets 연동) 설정
│   │   ├── db.py           # SQLModel 엔진 및 Session 관리
│   │   └── exceptions.py   # 자체 Custom Exception 클래스 정의 및 응답 포맷터
│   ├── models/             # SQLModel DB 모델 정의 (1_database_model.md 기반)
│   │   ├── base.py         # 포함: id, created_at, updated_at
│   │   ├── product.py
│   │   └── ...
│   ├── schemas/            # Pydantic 기반 Request/Response 밸리데이션 모델
│   │   ├── requests/
│   │   └── responses/
│   ├── crud/               # DB 쿼리 전담 계층 (SQLModel select/exec)
│   │   ├── crud_product.py
│   │   └── ...
│   └── services/           # 비즈니스 로직 (ex: PG결제 검증용, CRM 노티스 발송)
│       └── payment_service.py
├── requirements.txt
└── .chalice/               # Chalice 설정 파일 (config.json)
```

## 3. 역방향 검토에 따른 보완 요소 (Frontend/API 연계 고려)
- **에러 파서 보완:** `chalicelib/core/exceptions.py` 에서는 발생한 Exception을 캐치하여 무조건 API Spec의 `{ success: false, error: { code, message } }` 구조로 리턴하는 커스텀 핸들러(`@app.middleware('http')` 또는 데코레이터 패턴) 구현 필수.
- **Transaction 관리:** `crud/` 계층 내 쿼리는 다중 수정 시 무결성을 위해 `session.begin()` 등 SQLModel 기반 트랜잭션 Safe 로직 추가.
- **Dynamic Data 처리:** `models/reservation.py` 에서 `dynamic_data` 칼럼은 JSON 타입과 대응되도록 SQLModel/SQLAlchemy JSONB 타잎 명시적 지정.
