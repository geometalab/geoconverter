$(document).ready(function(){

  	$('#about-dialog-link').click(function(e) {
		$('#about-dialog').dialog({
			dialogClass: 'custom-dialog',
			modal: true,
			width: 450,
			buttons: [ {text: "Close", click: function() { $( this ).dialog( "close" ); }} ]
			});
	});
	
	$('#terms-of-service-dialog-link').click(function(e) {
		$('#terms-of-service-dialog').dialog({
			dialogClass: 'custom-dialog',
			modal: true,
			width: 750,
			buttons: [ {text: "Close", click: function() { $( this ).dialog( "close" ); }} ]
			});
	});
	
	$('#contact-dialog-link').click(function(e) {
		$('#contact-dialog').dialog({
			dialogClass: 'custom-dialog',
			modal: true,
			width: 320,
			buttons: [ {text: "Close", click: function() { $( this ).dialog( "close" ); }} ]
			});
	});
	
});