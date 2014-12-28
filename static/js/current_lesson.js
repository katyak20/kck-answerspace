/** namespace. */
var rh = rh || {};
rh.mq = rh.mq || {};

/** Tracks the editing state */
rh.mq.editing = false;
rh.mq.currentLessonKey = null;


rh.mq.selectListener = function() {
$('#lessonKey').change( function() {
      var lessonValue = $('#lessonKey').val();
      $.getJSON("/get_questions_for_the_lesson",{"lessonKey":lessonValue}).done(function(json) {
          $("#json-container").append( JSON.stringify(json));
          $("#json-container").append(lessonValue);

      }).fail(function(jqxhr, textStatus, error) {
          $("#json-container").append("GET JSON Request Failed: " + textStatus + ", " + error);
          $("#json-container").append(lessonValue);
      });
  });
};

$(document).ready( function() {

    rh.mq.selectListener();
});