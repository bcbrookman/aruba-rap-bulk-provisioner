// Search submission API Call
$('#search-form').submit(function(e) {
    $('#results').removeClass("hidden"); // Show results card
    $('#result-info').addClass("hidden"); // Hide any previous results
    $('#result-loader').removeClass("hidden"); // Show loading spinner
    var query = $('#search').val();
    console.log('Search submitted with query "' + query + '"');
    $.ajax({
		"url": "/api/search?query=" + encodeURI(query),
		"method": "GET",
	})
	.done(function(response) {
	    $('#serial').text(response.serialNumber);
	    $('#mac').text(response.mac);
	    $('#model').text(response.partNumber);
	    $('#image').text(response.additionalData.lastBootVersion);
	    $('#folder').text(response.additionalData.folder);
	    $('#apName').text(response.additionalData.deviceName);
	    $('#fullName').text(response.additionalData.deviceFullName);
	    $('#description').text(response.additionalData.deviceDescription);
	    $('#result-loader').addClass("hidden"); // Hide loading spinner
	    $('#result-info').removeClass("hidden"); // Show result info
    });
    e.preventDefault();
});

