# MyPy 사용 가이드

## 1. 설치

```bash
# Poetry를 사용하는 경우
poetry add --group dev mypy

# pip를 사용하는 경우
pip install mypy
```

## 2. 기본 사용법

### 단일 파일 체크
```bash
poetry run mypy user/interface/controllers/user_controller.py
```

### 전체 프로젝트 체크
```bash
poetry run mypy .
```

### 특정 패키지 체크
```bash
poetry run mypy user/
```

## 3. 주요 옵션

### 에러 코드 표시
```bash
poetry run mypy --show-error-codes user_controller.py
```

### 엄격 모드 (더 많은 타입 체크)
```bash
poetry run mypy --strict .
```

### 특정 디렉토리만 체크
```bash
poetry run mypy user/interface/
```

### 무시할 에러 설정
```python
# 코드에 주석으로 무시 설정
x: int = "hello"  # type: ignore
x: int = "hello"  # type: ignore[assignment]
x: int = "hello"  # type: ignore[assignment,arg-type]
```

## 4. 설정 파일

프로젝트 루트에 `pyproject.toml` 또는 `.mypy.ini` 파일을 생성하여 설정할 수 있습니다.

### pyproject.toml 설정 (추천)
```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
check_untyped_defs = true
show_error_codes = true

[[tool.mypy.overrides]]
module = ["migrations.*", "alembic.*"]
ignore_missing_imports = true
```

## 5. VS Code 통합

### settings.json에 추가
```json
{
    "python.linting.mypyEnabled": true,
    "python.linting.enabled": true,
    "mypy-type-checker.args": [
        "--show-error-codes",
        "--config-file",
        "pyproject.toml"
    ]
}
```

## 6. 일반적인 사용 패턴

### 개발 중 지속적으로 체크
```bash
# 파일 변경 시 자동 체크
poetry run mypy --watch user/
```

### CI/CD 파이프라인에 추가
```yaml
# .github/workflows/ci.yml 예시
- name: Run type checking
  run: poetry run mypy .
```

## 7. 주요 에러 타입

### 타입 불일치
```python
x: int = "hello"  # 에러: Incompatible types
```

### 타입 누락
```python
def func(x):  # 에러: Function is missing a type annotation
    return x
```

### None 체크
```python
x: str | None = None
len(x)  # 에러: Argument 1 to "len" has incompatible type
```

## 8. 타입 힌트 작성 팁

### 기본 타입
```python
x: int = 5
name: str = "hello"
items: list[int] = [1, 2, 3]
```

### 선택적 타입 (Optional)
```python
from typing import Optional

value: Optional[str] = None
# 또는 (Python 3.10+)
value: str | None = None
```

### 함수 타입
```python
def add(a: int, b: int) -> int:
    return a + b
```

### 튜플 타입
```python
result: tuple[int, str] = (1, "hello")
```

## 9. 실제 사용 예시

```bash
# 프로젝트 전체 타입 체크
poetry run mypy .

# 특정 모듈만 체크
poetry run mypy user/application/

# 에러 코드와 함께 상세 출력
poetry run mypy --show-error-codes --pretty user/

# 무시할 에러 목록 확인
poetry run mypy --show-error-codes user/ | grep "ignore"
```

## 10. 트러블슈팅

### 외부 라이브러리 타입 에러 무시
```toml
[[tool.mypy.overrides]]
module = ["some_library.*"]
ignore_missing_imports = true
```

### 특정 라인 무시
```python
x: int = "hello"  # type: ignore[assignment]
```

### 전체 함수 무시
```python
@typing.no_type_check
def legacy_function():
    ...
```

## 11. Best Practices

1. **점진적 도입**: 기존 프로젝트에는 `disallow_untyped_defs = false`로 시작
2. **에러 코드 활용**: `--show-error-codes`로 구체적인 에러 파악
3. **CI/CD 통합**: 자동화된 타입 체크로 코드 품질 유지
4. **타입 스텁 사용**: 외부 라이브러리용 타입 정보 제공

