(function(){

    $('#parent').removeClass('hidden');
    $('#parent').addClass('active');

    var request = window.urlUtils.getQueryParameter(window.location.href, 'request');
    $('#analysis a').attr('href', '/analysis/?request=' + request)

    $.get('/service/product?query=' + request).then(function (successResponse) {
        var sentimentData = JSON.parse(successResponse).analyticData.sentimentData;
        var normalizedSentimentData = getNormalizeSentimentDataForLineChart(sentimentData);

        chartUtils.drawBarChart({
            'chartContainerId': 'bar-chart',
            'title'           : 'Overall Sentiments',
            'xAxis'           : {
                categories: ['Positive', 'Negative', 'Neutral']
            },
            'yAxis'           : {
                title: {
                    text: ''
                }
            },
            'series'          : normalizedSentimentData
        });
    }, function (errorResponse) {
        console.log('errorResponse', errorResponse);
        if (errorResponse.status == "404") {

        }
    });


    var getNormalizeSentimentDataForLineChart = function(sentimentData) {
        console.log(sentimentData);
        var sentimentDataClone = [];
        sentimentData.map(function(sData){
            var dataClone = {
                'name': sData.name,
                'data': [
                    sData.data.Positive, sData.data.Negative, sData.data.Neutral
                ]
            };
            sentimentDataClone.push(dataClone);
        });

        console.log('sentimentDataClone', sentimentDataClone)
        return sentimentDataClone;
    }
})();