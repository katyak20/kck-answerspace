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
from models import Lesson, Question, Pupil, Teacher

def get_parent_key(user):
  return ndb.Key("Entity", user.email().lower())

def get_lessons(user):

  lessons = Lesson.query(ancestor=get_parent_key(user)).order(Lesson.topic)
  lessons_map = {}
  for lesson in lessons:
    lessons_map[lesson.key] = lesson.lesson_name
  return lessons, lessons_map

def get_question_entries(user, lessons_map):
  """ Gets all of the grade entries for this user.
        Replaces the assignment_key and student_key with an assignment and student. """
  question_entries = Question.query(ancestor=get_parent_key(user)).fetch() # TODO: Query for all QuestionEntries for this user, then fetch()
  for question_entry in question_entries:
    question_entry.lesson = lessons_map[question_entry.lesson_key]
  return question_entries


def get_questions(user,  Lesson):
  questions = Question.query(ancestor=get_parent_key(user)).order(Question.question_order).fetch()
  questions_map = {}
  for question in questions:
    questions_map[question.key()] = question
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