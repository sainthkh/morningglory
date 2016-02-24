jQuery(document).ready ($) ->
	$('.content-menu-wrap').mouseenter (e) ->
		$(this).find('.content-menu').fadeIn()
	
	$('.content-menu-wrap').mouseleave (e) ->
		$(this).find('.content-menu').fadeOut()
	
	$('.content-menu-wrap').click (e) ->
		$(this).find('.content-menu').show()