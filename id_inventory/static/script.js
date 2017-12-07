$("document").ready ( function () {

	$("#menu-toggle").click( function (e) {
	    // e.preventDefault();
	    $("#wrapper").toggleClass("toggled");
	});

	$("#btn_print").click(function (e) {
	    window.print()
	});

	$('ul li.nodrop').click( function() {
	    $(this).addClass('active').siblings().removeClass('active');
	 });

	$('li ul li').click( function() {
	    $(this).addClass('active').siblings().removeClass('active');
	    if ('li.dropdown') {};
	 });

	$("#id_blood_type").focus( function() {
		$(this).empty()
	});
	    
	$('#id_print_date').datepicker({ dateFormat: 'yy-mm-dd' });
	$('#id_dateFrom').datepicker({ dateFormat: 'yy-mm-dd' });
	$('#id_dateTo').datepicker({ dateFormat: 'yy-mm-dd' });
	$('#id_ribbon_use_date').datepicker({ dateFormat: 'yy-mm-dd' });
	$('#id_rtp_date').datepicker({ dateFormat: 'yy-mm-dd' });
	$('#id_received_date').datepicker({ dateFormat: 'yy-mm-dd' });

	$("#btnToday").click( function (e) {
	    $('#id_dateFrom').datepicker({ dateFormat: 'yy-mm-dd' }).datepicker("setDate", "0");
	    $('#id_dateTo').datepicker({ dateFormat: 'yy-mm-dd' }).datepicker("setDate", "0");
	});

	var val = document.getElementsByClassName("status-value");

	for (var i = 0; i < val.length; i++) {
		if (val[i].innerHTML < 10) {
			val[i].classList.add("status-low");
		};
	};

});