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
from models import *


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
PARENT_KEY = ndb.Key('Entity', "pupil_root")

class LessonPage(webapp2.RequestHandler):
  def get(self):
     # pupil_query = Pupil.query(ancestor=PARENT_KEY.order(-Pupil.level))
      pupil_query = Pupil.query(ancestor=PARENT_KEY).order(-Pupil.name)
      template = jinja_env.get_template("templates/pupil.html")
      self.response.out.write(template.render({"pupil_query": pupil_query}))

class InsertPupilAction(webapp2.RequestHandler):
    def post(self):
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

            new_pupil = Pupil(parent=PARENT_KEY,
                              name = self.request.get("pupilName"),
                              class_name = self.request.get("className"),
                              level = self.request.get("level"),
                              avatar = avatar_image)
            new_pupil.put()
        self.redirect(self.request.referer)

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

application = webapp2.WSGIApplication([
    ('/', LessonPage),
    ('/insertpupil', InsertPupilAction),
    ('/deletepupil', DeletePupilAction),
    ('/img', Thumbnailer),
], debug=True)
