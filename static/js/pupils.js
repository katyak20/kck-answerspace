/** namespace. */
var rh = rh || {};
rh.mq = rh.mq || {};

/** Tracks the editing state */
rh.mq.editing = false;

rh.mq.attachEventHandlers = function() {
    $('#insert-pupil-modal').on('shown.bs.modal', function(){
        $('input[name=name]').focus();
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

  $('#add-pupil').click( function() {
        $("#insert-pupil-modal input[name=key]").val("").prop("disabled", true);
      $('#insert-pupil-modal .modal-title').html('Add a pupil');
      $('#insert-pupil-modal button[type=submit]').html('Add pupil');
      $("#insert-pupil-modal input[name=pupilName]").val("");
      $("#insert-pupil-modal input[name=className]").val("");
      $("#insert-pupil-modal input[name=level]").val("");
      $("#insert-pupil-modal input[name=avatar]").val("");
  });

   $('.edit-pupil').click( function() {
      $('#insert-pupil-modal .modal-title').html('Edit this pupil');
      $('#insert-pupil-modal button[type=submit]').html('Edit pupil');
      pupilName = $(this).find(".pupilName").html();
      className = $(this).find(".className").html();
      level = $(this).find(".level").html();
     // avatar = $(this).find(".avatar").html();
      entityKey = $(this).find(".entity-key").html();
      console.log("Enttity key " + entityKey);
     // console.log("passed modalStaff");
      $("#insert-pupil-modal input[name=key]").val(entityKey).prop("disabled", false);
      console.log("passed modalStaff");
      $("#insert-pupil-modal input[name=pupilName]").val(pupilName);
      $("#insert-pupil-modal input[name=className]").val(className);
      $("#insert-pupil-modal input[name=level]").val(level);
      //$("#insert-pupil-modal input[name=avatar]").val(avatar);

      console.log("passed modalStaff");

  });

  $(".delete-pupil").click(function() {
      entityKey = $(this).find(".entity-key").html();
      console.log("delete Modal" + entityKey);
      $("#delete-pupil-modal input[name=key]").val(entityKey).prop("disabled", false);
  });



};
/** main */

$(document).ready( function() {
    rh.mq.enableButtons();
    rh.mq.attachEventHandlers();
});
