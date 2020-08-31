// Prevent empty search
$('#search-form').submit(function(e) {
    var query = $('#search').val();
    console.log('Search submitted with query "' + query + '"');
    if (query == "") {
        alert("Search cannot be blank! Please enter a keyword to perform a search.\n");
        e.preventDefault();
    }
});