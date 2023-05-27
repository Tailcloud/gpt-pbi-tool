// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.
var qnaContainer = $('#qnaContainer')[0];
var models = window["powerbi-client"].models;
var qnaConfig = {
    type: "qna",
    tokenType:   models.TokenType.Embed,
    datasetIds:  ["1b864961-4c2e-4a9c-b2a6-6aaf4d2aa8b4"],
    viewMode:    models.QnaMode.Interactive
};

function callAOAI(inputnlp) {
    $.ajax({
 
        // Our sample url to make request
        url: '/translate',
        type: "POST",

        // Function to call when to
        // request is ok
        success: function (data) {
            console.log(data);
            var x = JSON.stringify(data);
            console.log(x);
            getReport(data);

        },

        // Error handling
        error: function (error) {
            console.log(`Error ${error}`);
        }
    });
   
}

function getReport(aiqa){
    $.ajax({
        type: "GET",
        url: "/getembedinfo",
        dataType: "json",
        success: function (data) {
            embedData = $.parseJSON(JSON.stringify(data));
            // reportLoadConfig.accessToken = embedData.accessToken;

            // You can embed different reports as per your need
            // reportLoadConfig.embedUrl = embedData.reportConfig[0].embedUrl;
            qnaConfig.embedUrl = "https://app.powerbi.com/qnaEmbed?groupId=ef0d41ba-8607-44b1-9d70-befa2898e90b/reports/038608d1-55fa-402a-92ae-a3be92e3b749/ReportSection",
            qnaConfig.accessToken = embedData.accessToken;
            qnaConfig.question = aiqa;
            // Use the token expiry to regenerate Embed token for seamless end user experience
            // Refer https://aka.ms/RefreshEmbedToken
            tokenExpiry = embedData.tokenExpiry;

            var qna = powerbi.embed(qnaContainer, qnaConfig);

            qna.on("loaded", function () {
                console.log(" qna Report load successful")
            });
            
            // Triggers when a report is successfully embedded in UI
            qna.on("rendered", function () {
                console.log("qna Report render successful")
            });

            // Clear any other error handler event
            qna.off("error");

            // Below patch of code is for handling errors that occur during embedding
            qna.on("error", function (event) {
                var errorMsg = event.detail;

                // Use errorMsg variable to log error in any destination of choice
                console.error(errorMsg);
                return;
            });

            // qna = powerbi.get(qnaContainer);
            qna = powerbi.get(qnaContainer);

            // qna.setQuestion(input)
            //     .then(function (result) {
                 
            //     })
            //     .catch(function (errors) {
                  
            //     });
            // qna.off("visualRendered");

            // qna.on will add an event listener.
            qna.on("visualRendered", function(event) {
                console.log(" qna Report load successful")
                console.log(" qna Report load successful")
                console.log(" qna Report load successful")
                callAOAI();
                // qnaConfig.question = callAOAI();
                // print(qnaConfig.question);
                // powerbi.embed(qnaContainer, qnaConfig);
                
            });
        },
        error: function (err) {

            // Show error container
            var errorContainer = $(".error-container");
            $(".embed-container").hide();
            errorContainer.show();

            // Format error message
            var errMessageHtml = "<strong> Error Details: </strong> <br/>" + $.parseJSON(err.responseText)["errorMsg"];
            errMessageHtml = errMessageHtml.split("\n").join("<br/>")

            // Show error message on UI
            errorContainer.html(errMessageHtml);
        }
    });
}

$(function () {
    getReport("best product");
    // var qnaContainer = $('#qnaContainer')[0];
    // var inputfield = $('#_ngcontent-vkl-c406');
    // var models = window["powerbi-client"].models;
    // var aiquestion = callAOAI(prompt());

    // $.ajax({
    //     type: "GET",
    //     url: "/getembedinfo",
    //     dataType: "json",
    //     success: function (data) {
    //         embedData = $.parseJSON(JSON.stringify(data));
    //         // reportLoadConfig.accessToken = embedData.accessToken;

    //         // You can embed different reports as per your need
    //         // reportLoadConfig.embedUrl = embedData.reportConfig[0].embedUrl;
    //         qnaConfig.embedUrl = "https://app.powerbi.com/qnaEmbed?groupId=ef0d41ba-8607-44b1-9d70-befa2898e90b/reports/ce9a62ce-9c85-4896-b514-bb252dde79f9/ReportSection",
    //         qnaConfig.accessToken = embedData.accessToken;
    //         qnaConfig.question = "what's the BU numbers";
    //         // Use the token expiry to regenerate Embed token for seamless end user experience
    //         // Refer https://aka.ms/RefreshEmbedToken
    //         tokenExpiry = embedData.tokenExpiry;

    //         var qna = powerbi.embed(qnaContainer, qnaConfig);

    //         qna.on("loaded", function () {
    //             console.log(" qna Report load successful")
    //         });
            
    //         // Triggers when a report is successfully embedded in UI
    //         qna.on("rendered", function () {
    //             console.log("qna Report render successful")
    //         });

    //         // Clear any other error handler event
    //         qna.off("error");

    //         // Below patch of code is for handling errors that occur during embedding
    //         qna.on("error", function (event) {
    //             var errorMsg = event.detail;

    //             // Use errorMsg variable to log error in any destination of choice
    //             console.error(errorMsg);
    //             return;
    //         });

    //         // qna = powerbi.get(qnaContainer);
    //         qna = powerbi.get(qnaContainer);

    //         // qna.setQuestion(input)
    //         //     .then(function (result) {
                 
    //         //     })
    //         //     .catch(function (errors) {
                  
    //         //     });
    //         // qna.off("visualRendered");

    //         // qna.on will add an event listener.
    //         qna.on("visualRendered", function(event) {
    //             console.log(" qna Report load successful")
    //             console.log(" qna Report load successful")
    //             console.log(" qna Report load successful")
                
    //             qnaConfig.question = callAOAI(prompt());
    //             print(qnaConfig.question);
    //             powerbi.embed(qnaContainer, qnaConfig);
                
    //         });
    //     },
    //     error: function (err) {

    //         // Show error container
    //         var errorContainer = $(".error-container");
    //         $(".embed-container").hide();
    //         errorContainer.show();

    //         // Format error message
    //         var errMessageHtml = "<strong> Error Details: </strong> <br/>" + $.parseJSON(err.responseText)["errorMsg"];
    //         errMessageHtml = errMessageHtml.split("\n").join("<br/>")

    //         // Show error message on UI
    //         errorContainer.html(errMessageHtml);
    //     }
    // });
   

});