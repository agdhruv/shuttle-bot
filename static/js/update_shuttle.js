$('.modal').modal();

$("#shuttle-form").on('submit', function (e) {
	e.preventDefault();
});


$('#submit-password').on('submit', function (e) {
	e.preventDefault();

	var password = $('#input-password').val().trim();

	var $form = $("#shuttle-form");
	var origin = $form.attr('data-origin');
	var phone = $form.find('div.guard-phone input[type=text]').val().trim();
	var weekdays = $form.find('#weekdays').val().trim();
	var fridays = $form.find('#fridays').val().trim();
	var holidays = $form.find('#holidays').val().trim();

	var updatedSchedule = {
		password: password,
		origin: origin,
		phone: phone,
		schedule: {
			'weekday': weekdays,
			'friday': fridays,
			'holiday': holidays
		}
	};

	$.ajax({
		type: "POST",
		url: '/save_shuttle',
		contentType: "application/json",
		dataType: 'json',
		data: JSON.stringify(updatedSchedule),
		beforeSend: function () {
			$("#menu-form button[type=submit]").attr('disabled', 'disabled');
		},
		success: function (data) {
			$("#menu-form button[type=submit]").removeAttr('disabled');
			M.toast({html: 'Data saved!'});
			$('#input-password').val('');
			$('#modal1').modal('close');
		},
		error: function (error) {
			$("#menu-form button[type=submit]").removeAttr('disabled');
			M.toast({html: error.responseJSON.error + '. Try again.'});
			$('#input-password').val('');
		}
	});
});