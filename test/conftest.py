import os
import pytest

@pytest.fixture(scope="session", autouse=True)
def set_env_variables():
    # 환경 변수 설정
    os.environ['HEADLESS_MODE'] = 'False'
    yield
    # 테스트 후 환경 변수 정리
    del os.environ['HEADLESS_MODE']