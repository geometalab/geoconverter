$(document).ready(function(){
	$.ajaxSetup({
	    crossDomain: false,
	    beforeSend: function(xhr, settings) {
	    	xhr.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
	    }
	});
	
	addUploader();
	registerDownloadItemEvents();
	registerDownloads();
	
	registerWebservicesRunButton();
	
});

function getRandomConversionJobToken() {
	var chars = 'abcdefghijklmnopqurstuvwxyz';
	var random_token = 'job';
	
	random_token += (new Date()).getTime();
	
	for(var i = 0; i < 9; i++) {
		random_token += chars.substr(Math.floor(Math.random() * chars.length), 1);
	}

	return random_token;
}

function getUploaderAddDivID(job_token) {
	return 'manual-fine-uploader-' + job_token;
}

function getUploaderRunDivID(job_token) {
	return 'run-files-conversion-' + job_token;
}

function getDownloadDivID(job_token) {
	return 'download-' + job_token;
}

function getQueueDivID(job_token) {
	return 'queue-' + job_token;
}

function getDownloadQueueDivID(job_token) {
	return 'queue-' + job_token;
}

function getJobIDByDownloadDivID(download_div_id) {
	if (download_div_id.indexOf('download-') == 0) {
		return download_div_id.replace('download-', '');
	}
	return '';
}

function get_download_name() {
	var current_date = new Date();
	var current_hours = current_date.getHours();
	if (current_hours < 10) current_hours = '0' + current_hours;
	var current_minutes = current_date.getMinutes();
	if (current_minutes < 10) current_minutes = '0' + current_minutes;
	return current_hours + ':' + current_minutes;
}

function addUploader() {
	var job_token = getRandomConversionJobToken();
	
	var uploader_add_div = '';
	uploader_add_div += '<div id="' + getUploaderAddDivID(job_token) + '" style="margin-top: 25px; margin-bottom: 20px;">' + '\n';
	uploader_add_div += '    <noscript>' + '\n';
	uploader_add_div += '        <!-- put a simple form for upload here -->' + '\n';
	uploader_add_div += '    </noscript>' + '\n';
	uploader_add_div += '</div>';
	
	var uploader_run_div = '';
	uploader_run_div += '<div id="' + getUploaderRunDivID(job_token) + '" class="qq-upload-button default-border" style="margin-top: 10px;">' + '\n';
	uploader_run_div += '    Run' + '\n';
	uploader_run_div += '</div>' + '\n';
	
	$('#files-selector').html(uploader_add_div);
	$('#files-convert-run-button').html(uploader_run_div);
	
	initializeUploader(job_token);
}

function initializeUploader(job_token) {
	var uploader_add_div_id = getUploaderAddDivID(job_token);
	var uploader_run_div_id = getUploaderRunDivID(job_token);
	var queue_div_id = getQueueDivID(job_token);
	
	var manualuploader = $('#' + uploader_add_div_id).fineUploader({
      	request: {
        	endpoint: '/converter/forms/files/' + job_token + '/upload'
      	},
      	autoUpload: false,
      	text: {
        	uploadButton: 'Add'
      	},
      	retry: {
      		enableAuto: true,
      		maxAutoAttempts: 1,
      		autoAttemptDelay: 10,
      		autoRetryNote: 'Retrying...'
      	},
      	debug: false
	}).on('validate', function(event, fileData) {
		checkUploadListBorder($('#' + uploader_add_div_id + ' .qq-upload-list'), 0);
	}).on('cancel', function(event, id, filename) {
		checkUploadListBorder($('#' + uploader_add_div_id + ' .qq-upload-list'), 2);
		$.ajax({
	        url: '/converter/forms/files/' + job_token + '/remove/' + id,
	        type: 'POST',
	        data: { file_id: id },
	        success: function (response) {
	        	if (manualuploader.fineUploader('getInProgress') == 0 && $('#' + queue_div_id).length > 0) {
	        		finishConversion(job_token);
	        	}
	        }
    	});
	}).on('submit', function(event, id, filename) {
		//$(this).fineUploader('setParams', {'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()});
		
	}).on('error', function(event, id, filename, reason) {
		
	}).on('complete', function(event, id, filename, responseJSON){
		//alert('Complete!\nEvent: ' + event + '\nID: ' + id + '\nFilename: ' + filename + '\nJSON response: ' + responseJSON);
		//console.log(responseJSON);
		if (manualuploader.fineUploader('getInProgress') == 0) {
			finishConversion(job_token);
		}
	});

    $('#' + uploader_run_div_id).click(function() {
    	submitFilesForm(manualuploader, job_token);
    });
}

function finishConversion(job_token) {
	var uploader_add_div_id = getUploaderAddDivID(job_token);
	var queue_div_id = getQueueDivID(job_token);
	$.ajax({
        url: '/converter/forms/files/' + job_token + '/finish',
        type: 'POST',
        data: {},
        success: function (response) {
        	$('#' + uploader_add_div_id).remove();
        	var json_response = jQuery.parseJSON(response);
        	var job_id = json_response.job_id;
        	var successful = json_response.successful;
	    	var download_div = '';
	    	if (successful) {
		    	var download_div_id = getDownloadDivID(job_id);
		    	download_div += '<div id="' + download_div_id + '" class="qq-download-button default-border download-button">' + '\n';
		    	download_div += '    Download' + '\n';
		    	download_div += '</div>';
	    	} else {
	    		download_div += '<p>Error: Conversion failed!</p>';
	    		$('#' + queue_div_id).addClass('old-download-item');
	    	}
        	
        	$('#' + queue_div_id).append(download_div);
        	new_queue_div_id = getDownloadQueueDivID(job_id);
        	$('#' + queue_div_id).attr('id', new_queue_div_id);
        	if (successful) registerDownload(job_id);
        }
	});
}

function registerDownloads() {
	$('#download-list .download-item .qq-download-button').click(function(e){
		var download_button_div_id = $(this).closest('div').attr('id');
		var job_id = getJobIDByDownloadDivID(download_button_div_id);
    	var download_div_id = getQueueDivID(job_id);
    	openDownload(e, job_id);
    	// Detect Cancel???
    	$('#' + download_div_id).addClass('old-download-item');
    	$('#' + download_button_div_id).addClass('old-download-button');
    	$('#' + download_button_div_id).removeClass('download-button');
    });
}

function registerDownload(job_id) {
	var download_button_div_id = getDownloadDivID(job_id);
    var download_div_id = getQueueDivID(job_id);
	$('#' + download_button_div_id).click(function(e) {
    	openDownload(e, job_id);
    	$('#' + download_div_id).addClass('old-download-item');
    	$('#' + download_button_div_id).addClass('old-download-button');
    	$('#' + download_button_div_id).removeClass('download-button');
    });
}

function openDownload(e, job_id) {
	e.preventDefault();
	if ($('[id^=queue-job]').length > 0) {
		// If an upload (respectively conversion) is active the download opens in a new window.
		// This prevents messages like "Are you sure you want to leave this page?".
		window.open('/converter/download/' + job_id);
	} else {
		window.location.href = '/converter/download/' + job_id;
	}
}

function submitFilesForm(uploader, job_token) {
    var fileIDs = uploader.fineUploader('getStoredFilesIDs');
	
	if (fileIDs.length <= 0) {
		flashAddFileButton(job_token);
	} else if ($('#id_files_ogrformat').val() == '') {
		flashFileExportFormatTextBox();
	} else {
		var uploaderDivID = getUploaderAddDivID(job_token);
		var queueDivID = getQueueDivID(job_token);
		var download_name = get_download_name();
		var new_download_box = '<div id="' + queueDivID + '" class="download-item default-border">\n';
		new_download_box += '    <div class="download-name">' + download_name + '</div>';
		new_download_box += '    <div class="remove-download-item remove-download-item-icon"></div>\n';
		new_download_box += '</div>\n';
		
		$('#download-list').prepend(new_download_box);
		registerDownloadItemEvents();
		
		$('#' + queueDivID).append($('#' + uploaderDivID));
		$('#' + uploaderDivID + ' .qq-uploader .qq-upload-drop-area').remove();
		$('#' + uploaderDivID + ' .qq-uploader .qq-upload-button').remove('');
		$('#' + uploaderDivID + ' .qq-uploader .qq-upload-list').addClass('in-queue');
		$('#' + uploaderDivID + ' .qq-uploader .qq-upload-list').removeClass('default-border');
		$('#' + uploaderDivID).css('width', '325px');
		
		addUploader();
		
		var fileList = {};
		//console.log(uploader);
    	for (var i in fileIDs) {
    		fileList[fileIDs[i]] = uploader.fineUploader('getFilenameByID', fileIDs[i]);
    	}
    	
    	fileList['export_format'] = $('#id_files_ogrformat').val();
    	fileList['source_srs'] = $('#id_files_sourceSRS').val();
    	fileList['target_srs'] = $('#id_files_targetSRS').val();
    	fileList['simplify_parameter'] = $('#id_files_simplify').val();
    	fileList['download_name'] = download_name;
    	
    	$.ajax({
	        url: '/converter/forms/files/' + job_token + '/start',
	        type: 'POST',
	        data: fileList,
	        error: function (xhr) {
	        	// Löschen!
	        	//var newDoc = document.open("text/html", "replace");
				//newDoc.write(xhr.responseText);
				//newDoc.close();  
	        },  
	        success: function (response) {
	        	uploader.fineUploader('uploadStoredFiles');
	        }
    	});
    	
    	//
	
	}

}

function flashAddFileButton(job_token) {
	//$('#' + getUploaderAddDivID(job_token) + ' .qq-uploader .qq-upload-button').effect('shake', { times:3, direction:'right', distance:10 }, 300);
	$('#' + getUploaderAddDivID(job_token) + ' .qq-uploader .qq-upload-button').effect('highlight', { color:'#FF8C00' }, 1000);
}

function flashFileExportFormatTextBox() {
	$('#id_files_ogrformat').effect('highlight', { color:'#FF8C00' }, 1000);
}

function checkUploadListBorder(ul_element, min) {
	if (!ul_element.hasClass('in-queue')) {
		if (ul_element.children('li').length >= min) {
			ul_element.addClass('default-border');
		} else {
			ul_element.removeClass('default-border');
		}
	}
}

function registerDownloadItemEvents() {
	$('#download-list .download-item .remove-download-item').click(function(){
		
		var elem = $(this).closest('.download-item');

		//elem.hide("slide", { direction: "left" }, 1000);
		elem.hide('slow');
		
		$.ajax({
		  url: '/converter/remove/' + elem.attr('id'),
		})
	});
	
	$('.download-item .remove-download-item').hover(function() {
		$(this).attr('class','remove-download-item remove-download-item-icon-hover');
			}, function() {
		$(this).attr('class','remove-download-item remove-download-item-icon');
	});
}

function registerWebservicesRunButton() {
	$('#webservices-convert-run-button').click(function(e) {
		var url = $('#id_urlinput').val();
    	var export_format = $('#id_webservices_ogrformat').val();
		var source_srs = $('#id_webservices_sourceSRS').val();
    	var target_srs = $('#id_webservices_targetSRS').val();
    	var simplify_parameter = $('#id_webservices_simplify').val();
    	var download_name = get_download_name();
    	
    	if (url == '') {
    		flashWebserviceTextBox();
    	} else if (export_format == '') {
    		flashWebserviceExportFormatTextBox();
    	} else {
    		$('#id_urlinput').val('');
    		
    		runWebserviceConversion(url, export_format, source_srs, target_srs, simplify_parameter, download_name);
    	}
	});
}

function flashWebserviceTextBox() {
	$('#id_urlinput').effect('highlight', { color:'#FF8C00' }, 1000);
}

function flashWebserviceExportFormatTextBox() {
	$('#id_webservices_ogrformat').effect('highlight', { color:'#FF8C00' }, 1000);
}

function runWebserviceConversion(url, export_format, source_srs, target_srs, simplify_parameter, download_name) {
	var job_token = getRandomConversionJobToken();
		
	var queue_div_id = getQueueDivID(job_token);
	var new_download_box = '<div id="' + queue_div_id + '" class="download-item default-border">\n';
	new_download_box += '    <div class="download-name">' + download_name + '</div>';
	new_download_box += '    <div class="remove-download-item remove-download-item-icon"></div>\n';
	new_download_box += '    <img name="ajax-loader" src="static/geoconverter/img/ajax-loader.gif">\n';
	new_download_box += '</div>\n';
	$('#download-list').prepend(new_download_box);
	registerDownloadItemEvents();
	
	var webservicesData = {};
	
	webservicesData['webservice_url'] = url;
	webservicesData['export_format'] = export_format;
	webservicesData['source_srs'] = source_srs;
	webservicesData['target_srs'] = target_srs;
	webservicesData['simplify_parameter'] = simplify_parameter;
	webservicesData['download_name'] = download_name;
	
	$.ajax({
        url: '/converter/forms/webservices/' + job_token + '/convert',
        type: 'POST',
        data: webservicesData,
        error: function (xhr) {
        	$('#' + queue_div_id).children('img[name=ajax-loader]').remove();
	    	$('#' + queue_div_id).append('Error');
        },  
        success: function (response) {
	    	var json_response = jQuery.parseJSON(response);
	    	var job_id = json_response.job_id;
	    	var successful = json_response.successful;
	    	$('#' + queue_div_id).children('img[name=ajax-loader]').remove();
	    	
	    	var download_div = '';
	    	if (successful) {
		    	var download_div_id = getDownloadDivID(job_id);
		    	download_div += '<div id="' + download_div_id + '" class="qq-download-button default-border download-button">' + '\n';
		    	download_div += '    Download' + '\n';
		    	download_div += '</div>';
	    	} else {
	    		download_div += '<p>Error: Conversion failed!</p>';
	    		$('#' + queue_div_id).addClass('old-download-item');
	    	}
	    	
	    	$('#' + queue_div_id).append(download_div);
	    	new_queue_div_id = getDownloadQueueDivID(job_id);
	    	$('#' + queue_div_id).attr('id', new_queue_div_id);
	    	
	    	if (successful) registerDownload(job_id);
        }
	});
}
