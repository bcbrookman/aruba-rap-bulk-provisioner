// Search submission API Call
$('#search-form').submit(function(e) {
    var query = $('#search').val();
    console.log('Search submitted with query "' + query + '"');
    $.ajax({
		"url": "/api/search?query=" + encodeURI(query),
		"method": "GET",
	})
	.done(function(response) {
	    console.log(response);
	    $('#serial').text(response.serialNumber);
	    $('#mac').text(response.mac);
	    $('#model').text(response.partNumber);
	    $('#image').text(response.additionalData.lastBootVersion);
	    $('#folder').text(response.additionalData.folder);
	    $('#apName').text(response.additionalData.deviceName);
	    $('#fullName').text(response.additionalData.deviceFullName);
	    $('#description').text(response.additionalData.deviceDescription);
	    $('#results').removeClass("hidden");
    });
    e.preventDefault();
});