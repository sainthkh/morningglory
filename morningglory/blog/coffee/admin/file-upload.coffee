jQuery(document).ready ($) ->
	$('.inputfile').change (e) ->
		files = e.target.files
		
		data = new FormData()
		
		for f in files
			data.append('files', f, f.name)
		
		target_url = $(this).data 'target-url'
		text_target_name = $(this).data 'text-target'
		
		$.ajax
			url: target_url
			type: 'POST'
			data: data
			cache: false
			dataType: 'json'
			processData: false # Don't process the files
			contentType: false # Set content type to false as jQuery will tell the server its a query string request
			success: (data, textStatus, jqXHR) ->
				text_target = $("#" + text_target_name)
				caretPos = text_target[0].selectionStart
				textAreaTxt = text_target.val()
				txtToAdd = data.filetext
				text_target.val(textAreaTxt.substring(0, caretPos) + txtToAdd + textAreaTxt.substring(caretPos) );
						
			error: (jqXHR, textStatus, errorThrown) ->
				console.log('ERRORS: ' + textStatus)