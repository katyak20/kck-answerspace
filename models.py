
from google.appengine.ext import ndb
from google.appengine.api import images

import jinja2
import webapp2


class Pupil(ndb.Model):
    name = ndb.StringProperty()
    class_name = ndb.StringProperty()
    username = ndb.StringProperty()
    level = ndb.StringProperty()
    avatar = ndb.BlobProperty()

class Lesson(ndb.Model):
    topic = ndb.StringProperty()
    criteria = ndb.StringProperty()
    class_name = ndb.StringProperty()
    teacher_key = ndb.KeyProperty()
    resource = ndb.BlobProperty()

class Question(ndb.Model):
    question_number = ndb.IntegerProperty()
    lesson_key = ndb.KeyProperty(kind=Lesson)
    question_level = ndb.StringProperty()
    question_body = ndb.StringProperty()
    question_instructions = ndb.StringProperty()

class Teacher(ndb.Model):
    name = ndb.StringProperty()
    school_class =ndb.StringProperty()


