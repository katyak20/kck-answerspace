import os
import urllib
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images

import jinja2
import webapp2
import logging
import json

from handlers import insert_handlers
from models import *
import utils



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

jinja_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
autoescape=True)


def get_parent_key(user):
    return ndb.Key("Entity", user.email().lower())

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

#GENERIC_KEY used to group Pupils into an entity group


class PupilPage(webapp2.RequestHandler):
  def get(self):
      user = users.get_current_user()
     # pupil_query = Pupil.query(ancestor=PARENT_KEY.order(-Pupil.level))
      pupil_query = Pupil.query(ancestor=get_parent_key(user)).order(-Pupil.name)
      template = jinja_env.get_template("templates/pupil.html")
      self.response.out.write(template.render({"pupil_query": pupil_query,
                                              'user_email': user.email()}))


class CurrentLessonPage(webapp2.RequestHandler):
  def get(self):
      user = users.get_current_user()
      classes = utils.get_classes(user)
      lessons, lessons_map = utils.get_lessons(user)
      template = jinja_env.get_template("templates/index.html")
      self.response.out.write(template.render({'lessons': lessons,
                                             'user_email': user.email(),
                                             'user_name': user.nickname(),
                                             'classes': classes,
                                             'logout_url': users.create_logout_url("/")}))

class QuestionPage(webapp2.RequestHandler):
  def get(self):
      user = users.get_current_user()
      lesson_badge_data = {}
      questions = Question.query(ancestor=get_parent_key(user)).order(Question.question_number)
      lessons, lessons_map = utils.get_lessons(user)
      question_entries = utils.get_question_entries(user, lessons_map)
      for lesson in lessons:
        lesson_badge_data[lesson.key] = [0, 0]  # Accumulator for [Total Count, Total Score]
      for question in questions:
        lesson_badge_data[question.lesson_key][0] += 1
      for lesson in lessons:
        metadata = lesson_badge_data[lesson.key]
        if metadata[0] > 0:
          metadata.append(metadata[1] / metadata[0])  # Average = Total Score / Total Count
        else:
          metadata.append("na")  # Average is NA
      template = jinja_env.get_template("templates/questions.html")
      self.response.out.write(template.render({'user_email': user.email(),
                                               'questions': questions,
                                               'question_entries': question_entries,
                                               "lessons":lessons,
                                               'active_lesson': self.request.get('active_lesson'),
                                               'lesson_badge_data':lesson_badge_data}))

class LessonsPage(webapp2.RequestHandler):
  def get(self):
      user = users.get_current_user()
      lessons_query = Lesson.query(ancestor=get_parent_key(user)).order(Lesson.topic)
      template = jinja_env.get_template("templates/lessons.html")
      self.response.out.write(template.render({'user_email': user.email(),
                                              "lessons_query":lessons_query}))


class Thumbnailer(webapp2.RequestHandler):
    def get(self):
        if self.request.get("img_id"):
            logging.info("From Thumbnailer" + self.request.get("img_id"))
            pupil_key =ndb.Key(urlsafe=self.request.get("img_id"))
            pupil = pupil_key.get()
            if pupil.avatar:
                img = images.Image(image_data=pupil.avatar)
                img.im_feeling_lucky()
                thumbnail = img.execute_transforms(output_encoding=images.JPEG)

                self.response.headers['Content-Type'] = 'image/jpeg'
                self.response.out.write(thumbnail)
                return

        # Either "id" wasn't provided, or there was no image with that ID
        # in the datastore.
        self.error(404)

class DeletePupilAction(webapp2.RequestHandler):
    def post(self):
        logging.info("From DELETE URL safe = " + self.request.get("key"))
        pupil_key = ndb.Key(urlsafe=self.request.get("key"))
        pupil_key.delete()
        self.redirect(self.request.referer)



class DeleteLessonAction(webapp2.RequestHandler):
    def post(self):
        logging.info("From DELETE URL safe = " + self.request.get("key"))
        lesson_key = ndb.Key(urlsafe=self.request.get("key"))
        lesson_key.delete()
        self.redirect(self.request.referer)

class CurrentLessonAction(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        classes = utils.get_classes(user)
        lessons, lessons_map = utils.get_lessons(user)
        logging.info(" Current LESSON" + self.request.get("lesson"))
        lesson_key=ndb.Key(urlsafe=self.request.get("lesson"))
        questions_for_lesson_query = Question.query(ancestor=lesson_key)
        template = jinja_env.get_template("templates/index.html")
        self.response.out.write(template.render({'lessons': lessons,
                                             'user_email': user.email(),
                                             'user_name': user.nickname(),
                                             'classes': classes,
                                             'logout_url': users.create_logout_url("/"),
                                             'questions_for_lesson': questions_for_lesson_query}))

class CurrentLessonJsonData(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "application/json"
        logging.info(" Current LESSON" + self.request.get("lessonKey"))
        lesson_key= ndb.Key(urlsafe=self.request.get("lessonKey"))
        questions_for_lesson_query = Question.query(ancestor=lesson_key)
        questions_map = []
        for question_entry in questions_for_lesson_query:
            questions_map.append({'question_key':question_entry.key.urlsafe(), 'body':question_entry.question_body, 'instructions':question_entry.question_instructions})
        response = {"questions": "HEllo"}
        self.response.out.write((json.dumps(questions_map)))


class ServerTime(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "application/json"
        #self.response.headers.add_header("Access-Control-Allow-Origin", "*")

        response = {"message": "Hello AJAX!"}
        self.response.out.write(json.dumps(response))

application = webapp2.WSGIApplication([
    ('/', CurrentLessonPage),
    ('/pupils', PupilPage),
    ('/questions', QuestionPage),
    ('/lessons', LessonsPage),
    ('/insertpupil', insert_handlers.InsertPupilAction),
    ('/insertquestion', insert_handlers.InsertSingleQuestionAction),
    ('/deletepupil', DeletePupilAction),
    ('/insertlesson', insert_handlers.InsertLessonAction),
    ('/deletelesson', DeleteLessonAction),
    ('/get_questions_for_the_lesson', CurrentLessonJsonData),
    ('/img', Thumbnailer),
], debug=True)
