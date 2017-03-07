(function() {
    $("#main-panel").addClass('hidden');
    $('#refresh-data').addClass('hidden');

    var searchQuery = null;

    $('#search-query-submit').on('click', function (e) {
        query = $('#search-query').val();
        console.log('searchQuery', query);

        $('.dashboard').addClass('disabled');
        $('#create-request').addClass('hidden');

        $('#create-request #make-request').attr('href', '/requests/?request=');

        $.get('/service/product?query=' + query).then(function (successResponse) {
            console.log('successResponse', successResponse);
            $('#refresh-data').removeClass('hidden');
            $('#refresh-data').attr('href', '/requests/?request='+ encodeURI(query) + '&refresh=true')
            activateDashboard(JSON.parse(successResponse).analyticData, query)
        }, function (errorResponse) {
            console.log('errorResponse', errorResponse);
            if (errorResponse.status == "404") {
                console.log("Changing search value button to submit");
                $('#create-request').removeClass('hidden');
                $('#create-request #make-request').attr('href', '/requests/?request='+ encodeURI(query) + '&refresh=false')
            }
        });
    });


    var activateDashboard = function(dashboards, request) {
        $('#main-panel').removeClass('hidden');
        if (dashboards["sentimentData"] && dashboards["sentimentData"].length > 0) {
            console.log("sentiment data available");
            $('#sentiment').removeClass('disabled');
            $('#sentiment').attr('href', '/sentiment/?request=' + request)
        } else {
            console.log('Nothing available')
        }
    }
})();