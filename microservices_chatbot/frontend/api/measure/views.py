import time
import datetime
from functools import wraps

from quart import Blueprint, render_template, request
from flask_login import login_required, current_user
from frontend.api.measure import GET_POSTS_BY_USER_ID_COMMAND
from frontend.api import get_logs, post_request

measurements = Blueprint("measurements", __name__)


def counter(num=1, length=3):
    number = '0' * length + str(num)
    number = number[len(number)-length:]
    return number


def results(name):
    try:
        logs = [float(log["took"]) for log in get_logs()["logs"] if log.get("name") == name]
        return f"{min(logs):.3f} | {max(logs):.3f} | {sum(logs) / len(logs):.3f}"
    except ValueError:
        return f"0.000 | 0.000 | 0.000"


def measure_endpoint(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        start = time.time()
        get_logs()['count'] += 1
        c = counter(num=get_logs()["count"], length=6)
        result = await f(*args, **kwargs)
        took = round(time.time() - start, 3)
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        get_logs()["logs"].append({"tag": c, "name": f.__name__, "took": took, "date": date, "mean": results(f.__name__)})
        return result
    return decorated_function


@measurements.route("/stats")
@login_required
@measure_endpoint
async def stats():
    logs = get_logs().get("logs")
    logs.reverse()
    logs = logs[:-1 if len(logs) <= 20 else 20]
    return await render_template("stats.html", logs=logs)


@measurements.route("/history")
@login_required
@measure_endpoint
async def history():
    response = post_request(query=GET_POSTS_BY_USER_ID_COMMAND.replace("ID", current_user.id))
    posts = response.json().get('data').get('posts')
    return await render_template("history.html", posts=posts)
