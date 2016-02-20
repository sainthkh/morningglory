jQuery(document).ready ($) ->
	$('#send-test-mail-btn').click (e) ->
		e.preventDefault()
		button = $(this)
		button.prop 'disabled', true
		$.ajax
			url: $('#send-test-mail').data('action')
			method: 'post'
			data: 
				slug: $('input[name=slug]').val()
				email: $('#test-email').val()
			success: (data, textStatus, jqXHR) ->
				$('#send-test-mail .alert')
					.removeClass "hidden"
					.addClass "alert-success"
					.html data.message
				button.prop 'disabled', false
			error: (jqXHR, textStatus, errorThrown) ->
				console.log('ERRORS: ' + textStatus)
	
	$('#send-mail-now-btn').click (e) ->
		e.preventDefault()
		button = $(this)
		button.prop 'disabled', true
		$.ajax
			url: $('#send-mail-now').data('action')
			method: 'post'
			data: 
				slug: $('input[name=slug]').val()
				'list-slug': $('#target-email-list').val()
			success: (data, textStatus, jqXHR) ->
				$('#send-mail-now .alert')
					.removeClass "hidden"
					.addClass "alert-success"
					.html data.message
				button.prop 'disabled', false
			error: (jqXHR, textStatus, errorThrown) ->
				console.log('ERRORS: ' + textStatus)