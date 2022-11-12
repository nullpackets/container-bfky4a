from flask import render_template
from apiflask import APIFlask
from db import get_db, close_db
import sqlalchemy
from logger import log
from datetime import datetime

app = APIFlask(__name__)
app.teardown_appcontext(close_db)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/date")
def date():
    date = str(datetime.now())
    return {"date": date}

@app.route("/about")
def about():
    """The about page"""
    return render_template("about.html")

@app.route("/health")
def health():
    log.info("Checking /health")
    db = get_db()
    health = "BAD"
    try:
        result = db.execute("SELECT NOW()")
        result = result.one()
        health = "OK"
        log.info(f"/health reported OK including database connection: {result}")
    except sqlalchemy.exc.OperationalError as e:
        msg = f"sqlalchemy.exc.OperationalError: {e}"
        log.error(msg)
    except Exception as e:
        msg = f"Error performing healthcheck: {e}"
        log.error(msg)

    return health
