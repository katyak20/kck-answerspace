from google.appengine.api import users
from google.appengine.ext import ndb
from models import Student, Assignment, GradeEntry
import utils
import webapp2


class InsertAssignmentAction(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    urlsafe_entity_key = self.request.get('assignment_entity_key')
    if len(urlsafe_entity_key) > 0:
# Edit
        assignment_key = ndb.Key(urlsafe=urlsafe_entity_key)
        assignment = assignment_key.get()
    else:
# Add
        assignment = Assignment(parent=utils.get_parent_key(user))
    assignment.name = self.request.get('assignment_name')
    assignment.put()
    self.redirect("/?active_assignment=" + assignment.key.urlsafe())