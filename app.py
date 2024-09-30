import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from prometheus_client import generate_latest, Counter, Histogram
from src.couchbase import CouchDBClient
from flask import Flask, request, render_template, make_response
from flask_restx import Api, Resource, fields, Namespace
import logging
import time


app = Flask(__name__)

env_path = "./src/.env"
load_dotenv(env_path)
REQUEST_COUNT = Counter('app_request_count', 'Application Request Count', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Application Request Latency',
                            ['method', 'endpoint', 'http_status'])

# api = Api(app, version='1.0', title='PyAcademy API',
#           description='CRUD operations for Courses')
#
# ns_course = Namespace('courses', description='Course operations')
# api.add_namespace(ns_course, path='/pyuniversity')
api = Api(app)
ns_course = api.namespace("/pyuniversity", "CRUD operations for Courses")

courseInsert = api.model(
    "CourseInsert",
    {
        "courseName": fields.String(required=True, description="Course Name"),
        "courseId": fields.String(required=True, description="Course's Unique ID"),
        "duration": fields.Integer(required=True, description="Course Price"),
        "description": fields.String(required=False, description="Description of course"),
        "author": fields.String(required=True, description="Course Author"),
        "url": fields.String(required=True, description="Url of the Course")
    },
)

course = api.model(
    "Course",
    {
        "id": fields.String(required=True, description="Course's system generated Id"),
        "courseName": fields.String(required=True, description="Course Name"),
        "courseId": fields.String(required=True, description="Course's Unique ID"),
        "duration": fields.Integer(required=True, description="Course Price"),
        "description": fields.String(required=False, description="Description of course"),
        "author": fields.String(required=True, description="Course Author"),
        "url": fields.String(required=True, description="Url of the Course"),
        "createdAt": fields.String(required=True, description="Time course is created")
    },
)


@ns_course.route("/courses")
class Courses(Resource):
    # tag::post[]
    @ns_course.doc(
        "Create Course",
        responses={201: "Created", 500: "Unexpected Error"},
    )
    @ns_course.expect(courseInsert, validate=True)
    @ns_course.marshal_with(course)
    def post(self):
        status = None
        start_time = time.time()
        try:
            logger.info("Creating Course")
            data = request.json
            data["createdAt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            doc_id, rev = cb.insert(data)
            logger.info(f"Created Course with ID: {doc_id}")
            logger.info(f"Created Course with Rev: {rev}")
            data["id"] = doc_id
            data["_rev"] = rev

            logger.info("Created Course Successfully")
            status = 201
            return data, 201
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            status = 500
            return {"error": str(e)}, 500
        finally:
            REQUEST_LATENCY.labels('POST', '/courses', status).observe(time.time() - start_time)


@ns_course.route("/home")
class CourseHome(Resource):
    @ns_course.doc(
        "Home Page",
        reponses={200: "Success", 404: "Not Found", 500: "Unexpected Error"},
    )
    def get(self):
        status = None
        try:
            logger.info("Rendering the Home Page")
            headers = {'Content-Type': 'text/html'}
            status = 200
            return make_response(render_template('home.html'), 200, headers)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            status = 500
            return f"Unexpected error: {e}", 500
        finally:
            REQUEST_COUNT.labels('GET', '/home', status).inc()

    def post(self):
        status = None
        start_time = time.time()
        try:
            logger.info("Searching for the requested course")
            courseName = request.form['courseName']
            logger.info(courseName)
            data = cb.query_course_by_partial_name(courseName)
            # remove duplicates check by id
            headers = {'Content-Type': 'text/html'}
            result = len(data)
            if result == 0:
                status = 404
            else:
                status = 200
            return make_response(render_template('result.html', data=data, result=result), 200, headers)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            status = 500
            return f"Unexpected error: {e}", 500
        finally:
            REQUEST_COUNT.labels('POST', '/home', status).inc()
            REQUEST_LATENCY.labels('POST', '/home', status).observe(time.time() - start_time)


@app.route("/metrics")
def metrics():
    logger.info("Getting Metrics")
    return generate_latest()


db_info = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5984"),  # CouchDB default port
    "username": os.getenv("USERNAME"),
    "password": os.getenv("PASSWORD"),
    "database": os.getenv("DATABASE")
}

format = '%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s'
logging.basicConfig(filename="./logs/audit.log", filemode='a', format=format, datefmt='%H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.info(db_info.values())
cb = CouchDBClient(**db_info)
cb.connect()

cb.create_view("courses", "by_name", "function(doc) { emit(doc.courseName, doc); }", "_count")
cb.create_view("courses", "by_author", "function(doc) { emit(doc.author, doc); }", "_count")

# Create new view for partial matching
partial_match_map = """
function(doc) {
  if (doc.courseName) {
    var words = doc.courseName.toLowerCase().split(/\\s+/);
    for (var i = 0; i < words.length; i++) {
      for (var j = 1; j <= words[i].length; j++) {
        emit(words[i].substr(0, j), null);
      }
    }
  }
}
"""
cb.create_view("courses", "by_partial_name", partial_match_map, "_sum")

logger.info("Connected to CouchDB")
logger.info("DB Info: " + str(cb.db))

if __name__ == "__main__":
    logger.debug("Application Started ...")
    app.run(debug=True, port=3500, host='0.0.0.0')
