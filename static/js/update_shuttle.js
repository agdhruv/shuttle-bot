$("#shuttle-form").on('submit', function (e) {
	e.preventDefault();

	
	var $this = $(this);
	var origin = $this.attr('data-origin');
	var phone = $this.find('div.guard-phone input[type=text]').val().trim();
	var weekdays = $this.find('#weekdays').val().trim();
	var fridays = $this.find('#fridays').val().trim();
	var holidays = $this.find('#holidays').val().trim();

	var updatedSchedule = {
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
			$("#shuttle-form button[type=submit]").attr('disabled', 'disabled');
		},
		success: function (data) {
			$("#shuttle-form button[type=submit]").removeAttr('disabled');
			M.toast({html: 'Data saved!'});
		}
	});
});