$(document).ready(function(){
	
	$('.expander-content').hide();
	
	$('.expander-icon, .expander-title').click(function(){
		var expander_icon = $(this).parent().children('.expander-icon');
		var expander_content = $(this).parent().children('.expander-content');
		
		if (expander_icon.hasClass("expanded")) {
			expander_icon.removeClass("expanded")
			expander_icon.addClass("collapsed");
			expander_content.hide("slow");
		} else if (expander_icon.hasClass("collapsed")) {
			expander_icon.removeClass("collapsed")
			expander_icon.addClass("expanded");
			expander_content.show("slow");
		}
	});
	
	$('.expander-icon, .expander-title').hover(
			function() {
				var expander_icon = $(this).parent().children('.expander-icon');
				var expander_title = $(this).parent().children('.expander-title');
				
				expander_icon.addClass('expander-hover');
				expander_title.addClass('expander-hover');
			},
			function() {
				var expander_icon = $(this).parent().children('.expander-icon');
				var expander_title = $(this).parent().children('.expander-title');
				
				expander_icon.removeClass('expander-hover');
				expander_title.removeClass('expander-hover');
			}
	);
	
});