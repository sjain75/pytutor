var waitDialog = null;

$(document).ready(function(){
    waitDialog = $.dialog({
            title: "Waiting for login!",
            content: "login to get the report"
        });
});

function masterReport() {
    if(common.googleToken!=null){

		$("#worksheetReportForm").addClass("hidden");
		$("#studentReportForm").addClass("hidden");
		let wsCode = $(window.location.pathname.split("/"));
		let rootFolder = wsCode[wsCode.length-3];
		common.callLambda({"fn":"getReport", "reportType":"master", "rootFolder":rootFolder},
							function (obj){
								if(!("errorCode" in obj)){
									addVisualizerToPage(obj["trace"], 'reportHolder', {
										startingInstruction: 0,
										hideCode: false,
										lang: "py3",
										disableHeapNesting: true
									});
										
								}
								else{
										waitDialog = $.dialog({
										title: "Something went wrong!",
										content: obj["errorCode"]
										});
								}
					});
	}
	else{
		signInReload();
	}


}

function studentReport() {
	if(common.googleToken!=null){
        let wsCode = $(window.location.pathname.split("/"));
        let rootFolder = wsCode[wsCode.length-3];
        common.callLambda({"fn":"getReport", "reportType":"student",  "studentCode":$("#studentUsername").val(),"rootFolder":rootFolder},
                            function (obj){
                                if(!("errorCode" in obj)){
                                    addVisualizerToPage(obj["trace"], 'reportHolder', {
                                        startingInstruction: 0,
                                        hideCode: false,
                                        lang: "py3",
                                        disableHeapNesting: true
                                    });

                                }
                                else{
                                        waitDialog = $.dialog({
                                        title: "Something went wrong!",
                                        content: obj["errorCode"]
                                        });
                                }
                    });
    }
    else{
        signInReload();
    }
}

function worksheetReport() {
	if(common.googleToken!=null){
        let wsCode = $(window.location.pathname.split("/"));
        let rootFolder = wsCode[wsCode.length-3];
        common.callLambda({"fn":"getReport", "reportType":"worksheet",  "worksheetCode":$("#worksheetID").val(),"rootFolder":rootFolder},
                            function (obj){
                                if(!("errorCode" in obj)){
                                    addVisualizerToPage(obj["trace"], 'reportHolder', {
                                        startingInstruction: 0,
                                        hideCode: false,
                                        lang: "py3",
                                        disableHeapNesting: true
                                    });

                                }
                                else{
                                        waitDialog = $.dialog({
                                        title: "Something went wrong!",
                                        content: obj["errorCode"]
                                        });
                                }
                    });
    }
    else{
        signInReload();
    }
}


function studentReportPrompt() {
    $("#studentReportForm" ).removeClass("hidden");
    $("#worksheetReportForm").addClass("hidden");
}
function worksheetReportPrompt() {
    $( "#worksheetReportForm" ).removeClass("hidden");    
	$("#studentReportForm").addClass("hidden");
}


/*
    Function is a call back for successful sign in through GAPI. It's called from common.js
    It's also called initially during which it checks it disables page and shows waiting for signin dialog box.
    Verifies successful signin and causes reload data to load for wisc accounts and loads manual question stack
    and loads (beautifies) the rest of the page
*/
function signInReload(){
        if(common.googleToken!=null){
				username = common.getEmail();
                loadPage();
        }
        else{
            $(".abcRioButton").click();
			waitDialog = $.dialog({
            title: "Waiting for login!",
            content: "login to get the report"
        });

		}
    };

function loadPage() {
    waitDialog.close();
	$(".waiting").removeClass("waiting");
}

