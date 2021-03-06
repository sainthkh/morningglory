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