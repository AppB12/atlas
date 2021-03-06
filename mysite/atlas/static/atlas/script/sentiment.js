(function(){
    var request = window.urlUtils.getQueryParameter(window.location.href, 'request');
    $.get('/service/product?query=' + request).then(function (successResponse) {
        var sentimentData = JSON.parse(successResponse).analyticData.sentimentData;
        var normalizedSentimentData  = getNormalizeSentimentDataForLineChart(sentimentData);

        chartUtils.drawBarChart({
            'chartContainerId': 'bar-chart',
            'title'           : 'Overall Sentiments for Product',
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
                    sData.data.positive, sData.data.negative, sData.data.neutral
                ]
            };
            sentimentDataClone.push(dataClone);
        });

        console.log('sentimentDataClone', sentimentDataClone)
        return sentimentDataClone;
    }
})();