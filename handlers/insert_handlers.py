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
from models import  *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

jinja_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

#GENERIC_KEY used to group Pupils into an entity group


def get_parent_key(user):
    return ndb.Key("Entity", user.email().lower())

class InsertSingleQuestionAction(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    urlsafe_lesson_key =self.request.get('lesson_key')

    lesson_key=ndb.Key(urlsafe=self.request.get('lesson_key'))
    question_number = 2
    question_level = self.request.get("questionLevel")
    question_body = self.request.get("questionBody")
    question_instructions = self.request.get("questionInstructions")

    new_question_entry = Question(parent=lesson_key,
                                  question_number = question_number,
                                  lesson_key = lesson_key,
                                  question_level = question_level,
                                  question_body = question_body,
                                  question_instructions = question_instructions
                                  )
    new_question_entry.put()
    logging.info("URL safe = " + lesson_key.urlsafe())

    self.redirect(self.request.referer)

class InsertLessonAction(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if self.request.get("key"):
            logging.info("URL safe = " + self.request.get("key"))
            lesson_key = ndb.Key(urlsafe=self.request.get("key"))
            logging.info("Sring rep of REAL key" + str(lesson_key))
            lesson = lesson_key.get()
            lesson.topic = self.request.get("lessonTopic")
            lesson.lesson_name = self.request.get("lessonName")
            lesson.criteria = self.request.get("lessonCriteria")
            if self.request.get("lessonResource"):
               #
               #
               #
               lesson.resource = None
            else:
                lesson.resource = None
            lesson.put()
        else:
            logging.info("URL safe = " + self.request.get("key"))

            new_lesson = Lesson(parent=get_parent_key(user),
                              topic = self.request.get("lessonTopic"),
                              lesson_name = self.request.get("lessonName"),
                              criteria = self.request.get("lessonCriteria"),
                              resource = None)
            new_lesson.put()
        self.redirect(self.request.referer)



class InsertPupilAction(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if self.request.get("key"):
            logging.info("URL safe = " + self.request.get("key"))
            pupil_key = ndb.Key(urlsafe=self.request.get("key"))
            logging.info("Sring rep of REAL key" + str(pupil_key))
            pupil = pupil_key.get()
            pupil.name = self.request.get("pupilName")
            pupil.class_name = self.request.get("className")
            pupil.level = self.request.get("level")
            if self.request.get("avatar"):
                logging.info("self.request.get(avatar " + self.request.get("avatar"))
                avatar_image = images.resize(self.request.get("avatar"), 256, 256)
                pupil.avatar = None
                pupil.avatar = avatar_image
            else:
                avatar_image = None
            pupil.put()
        else:
            logging.info("URL safe = " + self.request.get("key"))
            if self.request.get("avatar"):
                avatar_image = images.resize(self.request.get("avatar"), 256, 256)
            else:
                avatar_image = None

            new_pupil = Pupil(parent=get_parent_key(user),
                              name = self.request.get("pupilName"),
                              class_name = self.request.get("className"),
                              level = self.request.get("level"),
                              avatar = avatar_image)
            new_pupil.put()
        self.redirect(self.request.referer)