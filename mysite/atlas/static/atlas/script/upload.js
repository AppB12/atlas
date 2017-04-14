(function(){
    console.log("LOADING UPLOAD JS")
    $('#upload').addClass('active');

    $(document).on('ready', function() {
        $("#input-44").fileinput({
            uploadUrl: '/service/upload/',
            maxFilePreviewSize: 1024,
            showBrowse: false,
            allowedFileExtensions: ["txt", "csv", "text"],
            browseOnZoneClick: true,
        });
    });
    /*$('#submitUpload').on('submit', function (e) {
      //$("#submitUpload").fileinput({

        console.log("Upload Button clicked")
        console.log("POST CALL");
        var formData = new FormData($(this)[0]);
        console.log(formData)
        type= 'POST';
        uploadUrl = "/service/upload/"
        $.ajax({
            type: type,
            url: uploadUrl,
            headers: {
                'X-CSRFToken': $.cookie('X-CSRFToken')
            },
            data: formData ,

            success: function(response) {
                alert("Success");
            },
            failure: function(response) {
                alert("Failure")
            },
            cache: false,
            contentType: false,
            processData: false
        });
        return false;
        console.log("ajax call request = ", request)
    });
    */
})();