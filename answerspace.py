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

from handlers import insert_handlers
from models import *



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
      self.response.out.write(template.render({"pupil_query": pupil_query}))


class CurrentLessonPage(webapp2.RequestHandler):
  def get(self):
      user = users.get_current_user()
      template = jinja_env.get_template("templates/index.html")
      self.response.out.write(template.render())

class QuestionPage(webapp2.RequestHandler):
  def get(self):
      user = users.get_current_user()
      template = jinja_env.get_template("templates/questions.html")
      self.response.out.write(template.render())

class LessonsPage(webapp2.RequestHandler):
  def get(self):
      user = users.get_current_user()
      lessons_query = Lesson.query(ancestor=get_parent_key(user)).order(Lesson.topic)
      template = jinja_env.get_template("templates/lessons.html")
      self.response.out.write(template.render({"lessons_query":lessons_query}))


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
    ('/img', Thumbnailer),
], debug=True)
