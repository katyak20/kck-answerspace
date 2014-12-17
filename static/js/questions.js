/** namespace. */
var rh = rh || {};
rh.mq = rh.mq || {};

/** Tracks the editing state */
rh.mq.editing = false;

rh.mq.attachEventHandlers = function() {
    $('#insert-question-modal').on('shown.bs.modal', function(){
        $('input[name=QuestionLevel]').focus();
    });
}

rh.mq.enableButtons = function() {
  $('#toggle-edit').click( function() {
    if (rh.mq.editing) {
        rh.mq.editing = false;
        $('.edit-actions').addClass('hidden');
        $(this).html('Edit');
    } else {
        rh.mq.editing = true;
        $('.edit-actions').removeClass('hidden');
        $(this).html('Done');
    }
   });

  $('#add-question').click( function() {
      $("#insert-question-modal input[name=key]").val("").prop("disabled", true);
      $('#insert-question-modal .modal-title').html('Add a question');
      $('#insert-question-modal button[type=submit]').html('Add question');
      $("#insert-question-modal input[name=questionLevel]").val("");
      $("#insert-question-modal input[name=questionBody]").val("");
      $("#insert-question-modal input[name=questionInstructions]").val("");
  });

   $('.edit-question').click( function() {
      $('#insert-question-modal .modal-title').html('Edit this question');
      $('#insert-question-modal button[type=submit]').html('Edit question');
      level = $(this).find(".questionLevel").html();
      body = $(this).find(".questionBody").html();
      instructions= $(this).find(".questionInstructions").html();
      entityKey = $(this).find(".entity-key").html();
      console.log("Entity key " + entityKey);
      $("#insert-question-modal input[name=key]").val(entityKey).prop("disabled", false);

      $("#insert-question-modal input[name=questionLevel]").val(level);
      $("#insert-question-modal input[name=questionBody]").val(body);
      $("#insert-question-modal input[name=questionInstructions]").val(instructions);


      console.log("passed modalStaff");

  });

  $(".delete-question").click(function() {
      entityKey = $(this).find(".entity-key").html();
      console.log("delete Modal" + entityKey);
      $("#delete-question-modal input[name=key]").val(entityKey).prop("disabled", false);
  });



};
/** main */

$(document).ready( function() {
    rh.mq.enableButtons();
    rh.mq.attachEventHandlers();
});