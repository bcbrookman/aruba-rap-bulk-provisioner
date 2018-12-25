var baseURL = "https://activate.arubanetworks.com/";
var APIDir = "api/ext/";
var baseAPIURL = baseURL + APIDir;

console.log('app.js loaded');

// Search Button
$('#search-btn').click(function() {
    console.log('search button triggered');
    var query = $('#search').val();
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
});