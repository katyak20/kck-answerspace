
from google.appengine.ext import ndb
from google.appengine.api import images

import jinja2
import webapp2

class Teacher(ndb.Model):
    teacher_id = ndb.StringProperty()
    teacher_name = ndb.StringProperty()

class ClassAtSchool(ndb.Model):
    class_id = ndb.StringProperty()
    class_teacher = ndb.StructuredProperty(Teacher)

class Pupil(ndb.Model):
    name = ndb.StringProperty()
    class_name = ndb.StringProperty()
    level = ndb.StringProperty()
    avatar = ndb.BlobProperty()

 # natasha = Pupil(name='Natasha', username='gorgeous', which_class = ClassAtSchool(class_id='kingfisher',class_teacher=Teacher(teacher_id='JW', teacher_name='Miss Watts')))
 # natasha.put()

class Topic_subject(ndb.Model):
    topic_subject_name=ndb.StringProperty()

class Lesson(ndb.Model):
    lesson_id = ndb.IntegerProperty()
    topic = ndb.StructuredProperty(Topic_subject)
    criteria = ndb.StringProperty()
    class_id = ndb.StructuredProperty(ClassAtSchool)

class Questions(ndb.Model):
    question_id =ndb.StringProperty()
    level = ndb.StringProperty()
    lesson_id = ndb.IntegerProperty()
    question_body = ndb.StringProperty()

class Resources(ndb.Model):
    question_id =ndb.StringProperty()
    level = ndb.IntegerProperty()
    lesson_id = ndb.IntegerProperty()
    resourse_body = ndb.StringProperty()


