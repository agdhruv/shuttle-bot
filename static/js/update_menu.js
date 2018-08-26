$('body').on('click', 'div.weekday div.input-field i', function () {
	$(this).closest('div.input-field').remove();
});

$('body').on('click', 'div.weekday a.add-item', function () {
	var html = '<div class="input-field">\
					<input type="text" value="">\
					<i class="material-icons">clear</i>\
				</div>';
	$(html).insertBefore($(this));
});

$("#menu-form").on('submit', function (e) {
	e.preventDefault();

	var $this = $(this);
	var days = ['everyday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
	var meal = $this.attr('data-meal');
	var timings = $this.find('.timings input[type=text]').val();
	var updated_menu = {
		meal: meal,
		timings: timings,
		menu: {}
	}

	days.forEach(function (day) {
		var inputs = $('div.' + day + ' input[type=text]');
		var items = [];

		for (var i = 0; i < inputs.length; i++) {
			items.push($(inputs[i]).val());
		}

		updated_menu.menu[day] = items;
	});

	$.ajax({
		type: "POST",
		url: '/save_menu',
		contentType: "application/json",
		dataType: 'json',
		data: JSON.stringify(updated_menu),
		beforeSend: function () {
			$("#menu-form button[type=submit]").attr('disabled', 'disabled');
		},
		success: function (data) {
			$("#menu-form button[type=submit]").removeAttr('disabled');
			M.toast({html: 'Data saved!'});
		}
	});

	
});