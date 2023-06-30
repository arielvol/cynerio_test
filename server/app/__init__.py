from flask import Flask
from flask_restful import Api
from config import config
from .extensions import db
from .app_urls import URL_USER, URL_TASK, URL_USER_TASK, URL_TASK_REPORT, URL_TASK_CHECK_IN, URL_TASK_CHECK_OUT
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{config.get('PGUSER')}:{config.get('PGPASSWORD')}@{config.get('PGHOST')}:{config.get('PGPORT')}/{config.get('PGDATABASE')}"
    else:
        app.config.update(test_config)

    db.init_app(app)

    from .resources.user_resource import UserResource
    from .resources.task_resource import TaskResource
    from .resources.task_report_resource import TasksReportResource
    from .resources.check_in_resource import CheckInResource
    from .resources.check_out_resource import CheckoutResource

    api = Api(app)
    api.add_resource(UserResource, URL_USER)
    api.add_resource(TaskResource, URL_TASK, f'{URL_USER_TASK}/<int:user_id>')
    api.add_resource(TasksReportResource, URL_TASK_REPORT)
    api.add_resource(CheckInResource, URL_TASK_CHECK_IN)
    api.add_resource(CheckoutResource, URL_TASK_CHECK_OUT)

    return app
