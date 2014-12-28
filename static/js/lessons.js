/** namespace. */
var rh = rh || {};
rh.mq = rh.mq || {};

/** Tracks the editing state */
rh.mq.editing = false;

rh.mq.attachEventHandlers = function() {
    $('#insert-lesson-modal').on('shown.bs.modal', function(){
        $('input[name=LessonTopic]').focus();
    });
}

rh.mq.enableButtons = function() {
  $('#toggle-edit').click( function() {
    if (rh.mq.editing) {
        rh.mq.editing = false;
        $('.edit-actions').addClass('hidden');
        $(this).html('Lessons edits');
    } else {
        rh.mq.editing = true;
        $('.edit-actions').removeClass('hidden');
        $(this).html('Done');
    }
   });

  $('#add-lesson').click( function() {
      $("#insert-lesson-modal input[name=key]").val("").prop("disabled", true);
      $('#insert-lesson-modal .modal-title').html('Add a lesson');
      $('#insert-lesson-modal button[type=submit]').html('Add lesson');
      $("#insert-lesson-modal input[name=lessonTopic]").val("");
      $("#insert-lesson-modal input[name=lessonName]").val("");
      $("#insert-lesson-modal input[name=lessonCriteria]").val("");
      $("#insert-lesson-modal input[name=lessonResource]").val("");
  });

   $('.edit-lesson').click( function() {
      $('#insert-lesson-modal .modal-title').html('Edit this lesson');
      $('#insert-lesson-modal button[type=submit]').html('Edit lesson');
      topic = $(this).find(".lessonTopic").html();
      lessonName = $(this).find(".lessonName").html();
      criteria = $(this).find(".lessonCriteria").html();
      entityKey = $(this).find(".entity-key").html();
      console.log("Entity key " + entityKey);
      $("#insert-lesson-modal input[name=key]").val(entityKey).prop("disabled", false);

      $("#insert-lesson-modal input[name=lessonTopic]").val(topic);
       $("#insert-lesson-modal input[name=lessonName]").val(lessonName);
      $("#insert-lesson-modal input[name=lessonCriteria]").val(criteria);
      // $("#insert-lesson-modal input[name=lessonResource]").val(instructions);


      console.log("passed modalStaff");

  });

  $(".delete-lesson").click(function() {
      entityKey = $(this).find(".entity-key").html();
      console.log("delete Modal" + entityKey);
      $("#delete-lesson-modal input[name=key]").val(entityKey).prop("disabled", false);
  });



};
/** main */

$(document).ready( function() {
    console.log("HEllo JSON");
    rh.mq.enableButtons();
    rh.mq.attachEventHandlers();
});