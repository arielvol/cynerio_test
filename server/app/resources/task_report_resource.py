from flask_restful import Resource
from app.models.user import User
from app.models.task import Task
from constants import MSG_NO_TASKS_TO_REPORT

class TasksReportResource(Resource):
    def get(self):
        tasks = Task.query.all()
        report = {}

        for task in tasks:
            user = User.query.filter_by(id=task.user_id).first()
            total_time = 0

            for event in task.events:
                if event.checkout_time:
                    time_diff = event.checkout_time - event.checkin_time
                    total_time += time_diff.total_seconds()

            if (total_time > 0):
                hours, remainder = divmod(total_time, 3600)
                minutes, seconds = divmod(remainder, 60)

                time_info = { "hours": hours, "minutes": minutes, "seconds": seconds }

                if user.name in report:
                    report[user.name][task.name] = time_info
                else:
                    report[user.name] = {task.name: time_info}

        if not report:
            return {'message': MSG_NO_TASKS_TO_REPORT}, 404

        return report, 200
