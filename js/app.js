var baseURL = "https://activate.arubanetworks.com/";
var APIDir = "api/ext/";
var baseAPIURL = baseURL + APIDir;

// Add shift() to jQuery prototype
$.fn.shift = [].shift;

// Copy CMDs to Clipboard
$('#copy-btn').click(function() {
  var $tempTextarea = $("<textarea style='whitespace:pre'></textarea>");
  $('body').append($tempTextarea);
  $tempTextarea.val($('#whitelist-cmds').text()).select();
  document.execCommand("copy");
  $tempTextarea.remove();
});

// Aruba Activate Logon
$('#login-btn').click(function() {
	var username = $("#user").val();
	var password = $("#pass").val();
	if (username && password) { // If username or password values are not empty...
		// Send Aruba Activate login request
    $.ajax({
      "url": baseURL + "LOGIN",
      "method": "POST",
      "headers": {"cache-control": "no-cache"},
      "data": encodeURI("credential_0=" + username + "&credential_1=" + password + "&destination=null")
    })
    .done(function() {
      $('#auth-result-icon').switchClass( "glyphicon-remove-sign", "glyphicon-ok-sign", 100);
    })
    .fail(function (response){
      console.log(response.responseText); // Log the response text for the failure
      $('#auth-result-icon').switchClass( "glyphicon-ok-sign", "glyphicon-remove-sign", 100);
    });
  } else {
		// If username and/or password is blank, indicate auth failure without sending request
    $('#auth-result-icon').switchClass( "glyphicon-ok-sign", "glyphicon-remove-sign", 100);
  }
});

// Aruba Activate Inventory Update
$('#update-btn').click(function() {
	var confirm = window.confirm("All entries (including blank values) will be sent to Aruba Activate.\n\nThis action CANNOT be undone!");
	if (confirm) {
		$(".error").remove(); // Remove any previously added error rows
		var $rows = $('#table').find('tr:not(:hidden)');
		$rows.shift(); // Exclude header row
		var keys = ['mac','folderName','deviceName','deviceFullName','deviceDescription'];
		var json = {}; 
		json.devices = [];
		// For each table row...
		$rows.each(function(rowIndex) {
			var $input = $(this).find('td input');
			var dict = {};
			// Set the value for each key to the value of each input
			keys.forEach(function(value, index) {
				dict[value] = $input.eq(index).val();
			});
			json.devices = [dict];
			// Send the inventory update to Aruba Activate
			$.ajax({
				"url": baseAPIURL + "inventory.json?action=update",
				"method": "POST",
				"headers": {"cache-control": "no-cache"},
				"data": encodeURI("json=" + JSON.stringify(json))
			})
			.done(function(response) {
				// If 'message.code' properties exist and code is 0 and "1 Devices Updated"...
				if (response.hasOwnProperty('message') &&
						response.message.hasOwnProperty('code') &&
						response.message.code === 0 &&
						response.message.text === "1 Devices Updated") {
					// Color the row green
					$input.parent().parent().css("background-color","#C1FCC1");
				}
				// If 'errors' property exists...
				else if (response.hasOwnProperty('errors')) {
					// color the row red and display the first error
					$input.parent().parent().css("background-color","#FFE0E0");
					$($rows[rowIndex]).after('<tr class="error" style="background-color:#FFE0E0"><td style="text-indent:40px" colspan="7">' + (response.errors[0].errMessage).toString() + '</tr>');
				}	
				// If 'failure' property exists...
				else if (response.hasOwnProperty('failure')) {
					// Color the row red and display the message
					$input.parent().parent().css("background-color","#FFE0E0");
					$($rows[rowIndex]).after('<tr class="error" style="background-color:#FFE0E0"><td style="text-indent:40px" colspan="7">' + (response.failure).toString() + '</tr>');
				}
				else { 
					// Color the row red and log the entire response
					$input.parent().parent().css("background-color","#FFE0E0");
					console.log(response);
				}
			})
			.fail(function (response){
				// Color the row red and log the entire response
				$input.parent().parent().css("background-color","#FFE0E0");
				console.log(response);
			});
		});
	}
});

// Table Operations
$('.add-row').click(function() {
	// Use the hidden row as a template and append to the table
	var $hiddenRow = $('#table').find('tr.hide').clone(true).removeClass('hide table-line');
	$('#table').find('table').append($hiddenRow);
});

$('.del-row').click(function() {
	// Remove the related error row if it exists
	if ($(this).parents('tr').next().hasClass("error")) {
			$(this).parents('tr').next().detach();
			}
	$(this).parents('tr').detach(); // Then remove the row
});

// Whitelist CMDs 
$('#cmd-btn').click(function() {
	$('#whitelist-div').removeClass('hide');
	var $rows = $('#table').find('tr:not(:hidden)');
	$rows.shift(); // Exlcude header row
	var $commands = $("#whitelist-cmds");
	$commands.text(null); // Clear existing entries
	// For each table row...
	$rows.each(function () {
		if (!$(this).hasClass('error')) { // If not an error row
			var $input = $(this).find('td input');
			var mac = $input.eq(0).val();
			var apName = $input.eq(2).val();
			var fullName = $input.eq(3).val();
			var description = $input.eq(4).val();
			var apGroup = $input.eq(5).val();
			$commands.append(
				"whitelist-db rap add mac " + mac +
				" ap-group \"" + apGroup +
				"\" ap-name \"" + apName + 
				"\" full-name \"" + fullName + 
				"\" description \"" + description + 
				"\"" + "\n"
			);
		}
	});
});

// CSV Import
$('#import-btn').change(function(event) {
	var file = event.target.files[0];
	var reader = new FileReader();
	reader.readAsText(file);
	reader.onload = function() {
		var $rows = $('#table').find('tr:not(:hidden)');
		$rows.shift(); // Exclude header row
		$rows.detach(); // Remove previously added rows
		var importedData = [];
		var lines = this.result.split('\n');
		lines.shift();
		// For each line in the file...
		for(var line = 0; line < lines.length; line++){
			// Turn the line into an array and append to importedData
			var list = lines[line].split(',');
			importedData.push(list);
		}
		// For each row in importedData...
		for(var importedRow = 0; importedRow < importedData.length; importedRow++){
			// Create a new row in the table
			var $hiddenRow = $('#table').find('tr.hide').clone(true).removeClass('hide table-line');
			$('#table').find('table').append($hiddenRow);
		}
		$rows = $('#table').find('tr:not(:hidden)');
		$rows.shift(); //remove header row
		// For each table row...
		$rows.each(function(rowIndex){
			var $input = $(this).find('td input');
			// Set each input element's value to it's imported value
			$input.each(function(tdIndex){
				$(this).val(importedData[rowIndex][tdIndex]);
			});
		});
	};
	reader.onerror = function() {
			alert('Unable to read ' + file.fileName);
	};
	$('#import-btn').val(null); // Needed for change to be triggered if same file is re-imported
});
