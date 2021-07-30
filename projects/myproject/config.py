# 위치 : C:/projects/myproject/config.py
# 내용 : 파이선 orm 라이브러리 SQLAlchemy 적용하기 위한 설정파일

import os

BASE_DIR = os.path.dirname(__file__)  # 데이터베이스 접속 주소

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))  # pybo.db 파일을 프로젝트의 루트디렉터리에 저장
SQLALCHEMY_TRACK_MODIFICATIONS = False  # SQLAlchemy 이벤트를 처리하는 옵션, 필요없으므로 비활성화
