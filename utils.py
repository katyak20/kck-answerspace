from google.appengine.ext import ndb
from models import Lesson, Question, Pupil, Teacher

def get_parent_key(user):
  return ndb.Key("Entity", user.email().lower())

def get_lessons(user):
  lessons = Question.query(ancestor=get_parent_key(user)).fetch()
  lessons_map = {}
  for lesson in lessons:
    lessons_map[lesson.key] = lesson
  return lessons, lessons_map

def get_questions(user,  Lesson):
  questions = Question.query(ancestor=get_parent_key(user)).order(Question.question_order).fetch()
  questions_map = {}
  for question in questions:
    questions_map[question.key] = question
  return questions, questions_map

def get_pupils(user):
  pupils = Pupil.query(ancestor=get_parent_key(user)).order(Pupil.username).fetch()
  pupils_map = {}
  levels = []
  for pupil in pupils:
    pupils_map[pupil.key] = pupil
    if pupil.levels not in levels:
      levels.append(pupil.level)
  return pupils, pupils_map, sorted(levels)


def remove_all_pupils(user):
  """ Removes all grades for the given student. """
  pupil_query = Pupil.query(ancestor=get_parent_key(user))
  for pupil in pupil_query:
    pupil.key.delete()