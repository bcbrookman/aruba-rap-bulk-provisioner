// Search submission API Call
$('#search-form').submit(function(e) {
    var query = $('#search').val();
    console.log('Search submitted with query "' + query + '"');
    if (query != "") {
        $('#results').removeClass("hidden"); // Show results card
        $('#result-info').addClass("hidden"); // Hide any previous results
        $('#result-img').addClass("hidden"); // Hide any previous result image
        $('#result-loader').removeClass("hidden"); // Show loading spinner
        $.ajax({
            "url": "/api/search/" + encodeURI(query),
            "method": "GET",
        })
        .done(function(response) {
            console.log(response)
            if (response.error == "Not Found") {
                $('#serial').text("Not Found");
                $('#mac').text("Not Found");
                $('#model').text("Not Found");
                $('#image').text("Not Found");
                $('#folder').text("Not Found");
                $('#apName').text("Not Found");
                $('#fullName').text("Not Found");
                $('#description').text("Not Found");
                $('#inventoryDate').text("Not Found");
                $('#result-img img').attr('src', ''  + '/static/images/products/notfound.png')
            } else {
                response = response.devices[0]; // Only display first result for now
                $('#serial').text(response.serialNumber);
                $('#mac').text(response.mac);
                $('#model').text(response.partNumber);
                $('#image').text(response.additionalData.lastAosVersion);
                $('#folder').text(response.additionalData.folder);
                $('#apName').text(response.additionalData.deviceName);
                $('#fullName').text(response.additionalData.deviceFullName);
                $('#description').text(response.additionalData.deviceDescription);
                $('#inventoryDate').text(response.inventoryDate)
                $('#result-img img').attr('src', '' + '/static/search/images/products/' + response.additionalData.img)
            }
            $('#result-loader').addClass("hidden"); // Hide loading spinner
            $('#result-info').removeClass("hidden"); // Show result info
            $('#result-img').removeClass("hidden"); // Show result info
        });
    } else {
        alert("Search cannot be blank! Please enter a keyword to perform a search.\n");
    }
    e.preventDefault();
});

