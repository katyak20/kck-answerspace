/** namespace. */
var rh = rh || {};
rh.mq = rh.mq || {};

/** Tracks the editing state */
rh.mq.editing = false;
rh.mq.currentLessonKey = null;


  $('#lessonKey').change( function() {
      currentLessonForm.submit();
  });
