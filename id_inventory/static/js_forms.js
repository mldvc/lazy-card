$("document").ready ( function () {

    // HIDE DISABLE THE SIDEBAR
    if ( $('#add-form-wrapper').length ) {
        $("#sidebar-wrapper").css("display", "none")
    }

	// FOR FILTERING FIELD ADDING FORMS
    var funcFilterField = function() {
        var form = $("#id_department").closest("form");
        $.ajax({
            url: form.attr("filter-field-url"),
            data: form.serialize(),
            dataType: 'json',
            success: function (data) {
                if ( $('#id_course').length ) {

                    $("#id_course").empty()
                    $('#id_course').append('<option value="">---------</option>')
                    $.each( data.data1, function( k, v ) {
                        $('#id_course').append('<option value="' + v.pk + '">'+v.fields.course+'</option>')
                    });

                } else if ( $('#id_level').length ) {

                    $("#id_level").empty()
                    $('#id_level').append('<option value="">---------</option>')
                    $.each( data.data1, function( k, v ) {
                        $('#id_level').append('<option value="' + v.pk + '">'+v.fields.level+'</option>')
                    });

                } else if ( $('#id_strand').length ) {

                    $("#id_strand").empty()
                    $('#id_strand').append('<option value="">---------</option>')
                    $.each( data.data1, function( k, v ) {
                        $('#id_strand').append('<option value="' + v.pk + '">'+v.fields.strand+'</option>')
                    });

                };
            }
        });
    }
    $("#id_department").change(funcFilterField)
    $("document").ready(funcFilterField)
	// #FOR FILTERING FIELD ADDING FORMS

	// FOR ADDING FORM PLACEHOLDERS AND INTERECTIONS
	$('#id_blood_type, #id_tin, #id_sss, #id_contact_num').focus( function() {
		if ($(this).val() == "N/A") {
			$(this).val("");
		};
	});

	$('#id_blood_type, #id_tin, #id_sss, #id_contact_num').blur( function() {
		if ($(this).val() == "") {
			$(this).val("N/A");
		};
	});

	$("#id_id_type, label[for='id_id_type']").css("display", "none")
	$("#id_validity, label[for='id_validity']").css("display", "none")
	$("#id_alu_validity, label[for='id_alu_validity']").css("display", "none")

	$('#id_birth_day').attr("type", "date")

    $('#id_full_name').attr("placeholder", "First Name  Middle Initial  Surname")
	$('#id_ptn').attr("placeholder", "Name of person to contact or notify in case of emergency.")
	$('#id_ptn_cnum').attr("placeholder", "Contact number of Person to Notify.")
	$('#id_address').attr("placeholder", "Address of Person to Notify.")
	$('#id_blood_type').attr("placeholder", 'Add double quote to your blood type. e.g. "B"')
	$('#id_validity').attr("readonly","")

    $('#id_birth_day').datepicker({
        yearRange: "-100:+0",
        changeMonth: true,
        changeYear: true
    });

    // COPY TO CLIPBOARD
	$('.field-input').click( function() {
		clipboard.copy($(this).val())
        $.each( $('.field-input'), function() {
            $('.field-input').removeClass("field-copy-active")
        });
        $(this).addClass("field-copy-active")
	});

    // CONFIRMATIONS
    $('[data-toggle=confirmation]').confirmation({
      rootSelector: '[data-toggle=confirmation]',
      // other options
    });

});