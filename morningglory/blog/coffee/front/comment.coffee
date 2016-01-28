jQuery(document).ready ($) ->
	getCookie = (name) ->
		cookieValue = null;
		if document.cookie and document.cookie != '' 
			cookies = document.cookie.split(';')
			for i in [0..cookies.length-1]
				cookie = $.trim(cookies[i])
				# Does this cookie string begin with the name we want?
				if cookie.substring(0, name.length + 1) is (name + '=') 
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
					break
		return cookieValue
	
	csrftoken = getCookie('csrftoken');
	csrfSafeMethod = (method) -> (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method)) # these HTTP methods do not require CSRF protection
	
	$.ajaxSetup(
		beforeSend: (xhr, settings) ->
			if not csrfSafeMethod(settings.type) and not this.crossDomain
				xhr.setRequestHeader("X-CSRFToken", csrftoken)
		)
		
	$('.comment-form').submit (e) ->
		e.preventDefault()
		$.ajax(
			method: "post"
			url: $('.comment-form').attr('action') + '/ajax'
			data :
				name : $('#name').val()
				email : $('#email').val()
				website : $('#website').val()
				comment : $('#comment').val()
			success : (data) ->
				if data.success
					$('.comments').append(data.html)
				else 
					$('#comment-error').text(data.msg).removeClass("hidden")
		)