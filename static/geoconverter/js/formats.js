$(document).ready(function(){
	$('#id_files_ogrformat').change(function() {
		synchronize_webservices_export_format();
	});
	$('#id_webservices_ogrformat').change(function() {
		synchronize_files_export_format();
	});
});

function synchronize_files_export_format() {
	var files_format = $('#id_files_ogrformat').val();
	var webservices_format = $('#id_webservices_ogrformat').val();
	if (files_format != webservices_format) {
		$('#id_files_ogrformat').val(webservices_format);
	}
}

function synchronize_webservices_export_format() {
	var files_format = $('#id_files_ogrformat').val();
	var webservices_format = $('#id_webservices_ogrformat').val();
	if (files_format != webservices_format) {
		$('#id_webservices_ogrformat').val(files_format);
	}
}