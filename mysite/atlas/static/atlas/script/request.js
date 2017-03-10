(function(){
    console.log("LOADING REQUEST JS")
    var request = window.urlUtils.getQueryParameter(window.location.href, 'request');
    console.log("Request = " , request)
    $('#reqKW').val(request);
    $.get('/service/request/').then(function (successResponse) {
        console.log('Stringify successResponse', JSON.stringify(successResponse,null, 2));
        console.log('PArsed successResponse', JSON.parse(successResponse));
        var clients = [
            { "Request ID": "001", "Product": "TV", "Time": "16:54 Feb 20th 2016" , "Status": "Completed"},
            { "Request ID": "002", "Product": "iMac", "Time": "20:01 April 10th 2016" ,"Status": "Completed"},
            { "Request ID": "003", "Product": "iPad", "Time": "15:41 January 31st 2017" ,"Status": "Processing"},
            { "Request ID": "004", "Product": "iPhone", "Time": "13:09 February 15th " ,"Status": "Pending"},
            { "Request ID": "005", "Product": "Chrome Book" , "Time": "00:45 February 21st" ,"Status": "Pending"}
        ];

        $("#jsGrid").jsGrid({
            width: "100%",
            height: "400px",

            inserting: false,
            editing: false,
            sorting: true,
            paging: true,
            autoload: true,
            pageLoading: true,


            data: JSON.parse(successResponse),

            fields: [
                { name: "reqId", type: "text", width: 100, title:"Request ID" },
                { name: "reqKw", type: "text", width: 150, title: "Product" },
                { name: "reqTime", type: "text", width: 150, title: "Time" },
                { name: "reqStatus", type: "text", width: 150, title: "Status" },

            ]
        });
    }, function (errorResponse) {
            console.log("errorResponse", errorResponse)
    });


    $('#reqBtn').on('click', function (e) {
        console.log("Button clicked")
        var refresh = window.urlUtils.getQueryParameter(window.location.href, 'refresh');
        console.log(refresh)

        var type = null;
        var url= null;
        if(refresh==="true") {
            console.log("PUT CALL");
            type='PUT';
            url = "/service/product/" + encodeURI(request) + '/refresh'
        } else {
            console.log("POST CALL");
            type= 'POST';
            url = "/service/product/add"
        }
        $.ajax({
            type: type,
            url: url,
            headers: {
                'X-CSRFToken': $.cookie('X-CSRFToken')
            },
            data:  {'name': request },
            success: function(response) {
                location.reload(false);
            },
            failure: function(response) {
                alert("Failure")
            }
        });
        console.log("ajax call request = ", request)
    });

})();