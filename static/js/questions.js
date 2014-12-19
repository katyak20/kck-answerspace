/** namespace. */
var rh = rh || {};
rh.mq = rh.mq || {};

/** Tracks the editing state */
rh.mq.editing = false;
rh.mq.currentLessonKey = null;

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
      $("#insert-question-modal select[name=LessonName]").val("");
      $("#insert-question-modal input[name=questionBody]").val("");
      $("#insert-question-modal input[name=questionInstructions]").val("");
  });

   $('.edit-question').click( function() {
      $('#insert-question-modal .modal-title').html('Edit this question');
      $('#insert-question-modal button[type=submit]').html('Edit question');
      lessonName = $(this).find(".lessonName").html();
      level = $(this).find(".questionLevel").html();
      body = $(this).find(".questionBody").html();
      instructions= $(this).find(".questionInstructions").html();
      entityKey = $(this).find(".entity-key").html();
      console.log("Entity key " + entityKey);
      $("#insert-question-modal input[name=key]").val(entityKey).prop("disabled", false);
      $("#insert-question-modal select[name=lessonName]").val(lessonName);
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

rh.mq.updatePageTitle = function() {
	newName = $("#" + rh.mq.currentLessonKey).find(".lesson-name").html();
	if (newName) {
	    console.log(newName);
		$("#lesson-name").html(newName);
	} else {
		$("#lesson-name").html("All Lessons");
	}
};

rh.mq.updateTable = function() {
	//var table = $('#grade-entry-table').DataTable();
//	table.search(rh.mq.currentAssignmentKey).draw();
//	$("input[type=search]").val("");
};


/** main */

$(document).ready( function() {
    rh.mq.enableButtons();
    rh.mq.attachEventHandlers();
    rh.mq.currentLessonKey = $('.sidebar-link.active').attr('id');
    console.log( " HaHa" + $('.sidebar-link.active').attr('id'));

	$('.sidebar-link').click(function() {
	    rh.mq.updatePageTitle();
		// Update the sidebar
		$('.sidebar-link').removeClass('active');
		$(this).addClass('active');
		// Update the list of grades shown in the table.
		rh.mq.currentLessonKey = $(this).attr('id');

		$(".row-offcanvas").removeClass("active");
		rh.mq.updatePageTitle();
    });
});