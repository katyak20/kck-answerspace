/** namespace. */
var rh = rh || {};
rh.mq = rh.mq || {};

/** Tracks the editing state */
rh.mq.editing = false;
rh.mq.currentLessonKey = null;


rh.mq.selectListener = function() {
$('#lessonKey').change( function() {
      var lessonValue = $('#lessonKey').val();
      $.getJSON("/get_questions_for_the_lesson", {'lessonKey': lessonValue}).done(function(json) {

          $('#json-container').append(JSON.stringify(json));

         })
         .fail(function(jqxhr, textStatus, error) {
           console.log("GET JSON Request Failed: " + textStatus + ", " + error);
         });
  });
};

$(document).ready( function() {

    rh.mq.selectListener();
});