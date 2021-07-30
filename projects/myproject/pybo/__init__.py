from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

# db객체를 create_app() 밖에 생성하여 다른 모듈(블루프린트)에서 불러올 수 있게함
# db객체 초기화는 create_app()에서 실행
db = SQLAlchemy()
migrate = Migrate()

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)  # config.py에 작성한 항목을 app.config 환경변수로 부르기 위함

    # ORM, 전역변수 초기화
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # 블루프린트
    from .views import main_views, question_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    return app
