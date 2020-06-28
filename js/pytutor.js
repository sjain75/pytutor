var manualQuestionStack={};

function signInReload(){
		if(common.googleToken!=null){
			username = common.getEmail();
			if(username.split("@").pop()!="wisc.edu"){

				$.confirm({title: 'Not wisc.edu account',
				content: 'You have not logged in with your wisc.edu account. Your submissions are not graded on accuracy but only on participation, so please login with your wisc.edu account. </br>If you are not a CS220 or a wisc student, no worries, feel free to practice :)',
				buttons: {
					"Log out and sign in with wisc account": function () {
						common.googleSignOut();
						//$("span#not_signed_inhhqwiuutv1fs").click();
					},
					"Continue with non-wisc account": function () {
					
						loadPage();
						manualQuestionStackLoad({});
					}
					
				}});

			}
			else{
				loadPage();
				let wsCode = $(window.location.pathname.split("/")).last()[0].replace(".html","");
				common.callLambda({"fn":"reload", "netId":common.getEmail(), "worksheetCode":wsCode},
						function (obj){
							if(!("errorCode" in obj || "incorrectDomain" in obj)){
								manualQuestionStackLoad(obj["isCorrect"]);	
							}
							else{
									manualQuestionStackLoad({});
							}
						});
			}
		}
		else{
			 $(".abcRioButton").click();
			$.dialog({ 
				title: "Waiting for login!",
				content: "login to do the worksheet"
			});
			$(".jconfirm-closeIcon").remove();
		}
    };

$("#signin").on("load", signInReload);//figure this out

		
questionHtmlString=`<div content_resource_id="32241403" class="manualQuestionDiv">
			<div>"""manualQuestion"""</div> 
			<div style="margin-bottom: 5px;"><textarea style="width: 85%;" cols="20" rows="1" spellcheck="false" autocapitalize="false" class="manualAnswer"></textarea></div>"""answerCorrectness"""
			<div><button class="submitManual button">Check</button></div>
		</div>`;
correctImage = `<div id=answerTruth style='font-size:40px'><img width='8%' style='padding-left:2%' src='../resources/correct-checkmark.svg'></img></div>`;
incorrectImage = `<div id=answerTruth><img width='8%' style='padding-left:2%' src='../resources/incorrect-cross.svg'></img></div>`;
//Take the simple div with class manual question and make it fancier. Runs at page load for each div with class "manualQuestion"
function manualQuestionStackLoad(isCorrect){
	$(".manualQuestion").each(function(){
		manualQuestionString= $(this).text();
		let privateQuestionHtml=questionHtmlString;
		privateQuestionHtml = privateQuestionHtml.replace('"""manualQuestion"""',manualQuestionString);
		let parentScriptText =$($(this).prevAll("script")[0]).text();
		let parentScriptRefined  = parentScriptText.substring(parentScriptText.lastIndexOf("addVisualizerToPage")).split(",");

		let parentStoryKey = parentScriptRefined[1].replace(/\'/g,"").replace(/ /g,"");
		let parentStoryBeginsAt = Number(parentScriptRefined[2].substring(parentScriptRefined[2].lastIndexOf(":")+1).replace(/ /g,""));
		let questionStep = Number($(this).attr("step"));
		if(!(parentStoryKey in manualQuestionStack)){
			manualQuestionStack[parentStoryKey] = {};
		}
		let image = (isCorrect[parentStoryKey+"_"+questionStep])?correctImage:((isCorrect[parentStoryKey+"_"+questionStep]==false)?incorrectImage:"");
		privateQuestionHtml = privateQuestionHtml.replace('"""answerCorrectness"""',image);
		manualQuestionStack[parentStoryKey][questionStep] = privateQuestionHtml;
		if(parentStoryBeginsAt+1==questionStep){
			$(this).after(privateQuestionHtml);  
			$($(this).prevAll("div.parentDiv")[0]).attr("disabled", true);
			$($(this).prevAll("div.parentDiv")[0]).addClass("waitingStory");	
		}
		$(this).remove();
	});
}

var waitDialog = null;
$(document).ready(function(){
	waitDialog = $.dialog({
            title: "Waiting for login!",
            content: "login to do the worksheet"
        });
});



function manualCheck(){
        parentDiv = $(this).closest(".manualQuestionDiv");

        userAnswer = $(parentDiv).find(".manualAnswer").val();
        $(parentDiv).find(".manualAnswerTruth").remove();

        if(common.googleToken != null){
				let parentStory = $($(parentDiv).prevAll("div.parentDiv")[0]);
                let questionCode=parentStory.attr("id")+($("#curInstr", parentStory).text().split(" ")[1]);
                let wsCode = $(window.location.pathname.split("/")).last()[0].replace(".html","");
                common.callLambda({"fn":"addNewAnswer", "worksheetCode":wsCode, "questionCode":questionCode, "response":userAnswer},
                    function (obj) {
                          if(!("errorCode" in obj)){
                            if(obj["fnExecuted"]=="addNewAnswer" && questionCode in obj["isCorrect"]){
                                if(obj["isCorrect"][questionCode]==true){
                                    $(parentDiv).find(".manualAnswer").after(correctImage);
                                }
                                else{
                                     $(parentDiv).find(".manualAnswer").after(incorrectImage);
                                }
                            }
                            else{
                                $(parentDiv).append("Something went wrong! No error code...");
								$(parentDiv).attr("disabled", true);
								$(parentDiv).addClass("waitingStory");
                            }
                          }
                          else {
                              console.log(obj);
                              console.log(obj["errorCode"]);
                              $(parentDiv).append("Something went wrong! Error Code: "+obj["errorCode"]);
							  $(parentDiv).attr("disabled", true);
							  $(parentDiv).addClass("waitingStory");
                          }
						  if("incorrectDomain" in obj){
						      $(parentDiv).append("</br>Incorrect Domain: Attempt not recorded");
							}
							$(parentStory).attr("disabled", false);
							$(parentStory).removeClass("waitingStory");
                        }
                    );
        }

        else{
             $(parentDiv).append("<span id='notLoggedIn'>You are not logged in so none of these questions will be graded! But feel free to continue for practice! :)</span>");
        }

    };






    
    
function displayPrevious() {
	if (current == 1) {
        previousButton.addClass("hidden");
    }
    if (current == end) {
		nextButton.removeClass("hidden");
    }
    $($(".parentDiv")[current]).addClass("hidden");
    current--;
    $($(".parentDiv")[current]).removeClass("hidden");
}

function displayNext() {
	if (current == end - 1) {
		nextButton.addClass("hidden");
	}
	if (current == 0) {
		previousButton.removeClass("hidden");
	}
	$($(".parentDiv")[current]).addClass("hidden");
	current++;
	$($(".parentDiv")[current]).removeClass("hidden");
}


var previousButton = null;
var nextButton = null;
var end =null;
var current =null;

function loadPage() {
	waitDialog.close();
	$("[id=executionSlider]").each(function(){ $(this).remove();});
	$(".waiting").removeClass("waiting");

	$("[id=vcrControls]").children().attr("disabled",true);
	
	

	const start = 1;
    current = 0;
    end = $(".parentDiv").length-1; //Find the number of problems on page
	previousButton = $("#previousButton");
	nextButton = $("#nextButton");

	if (window.matchMedia("(max-width: 768px)").matches) {
		$(".parentDiv").each(function(){
				$(this).parent().addClass("hidden");
			})
		$($(".parentDiv")[0]).parent().removeClass("hidden");
        previousButton.addClass("hidden");
    }


	$(".lineNo").each(function(){
		$(this).attr("style","cursor: pointer;")
		$(this).text("🔘");
	}); //replace all line numbers with something that looks more clickable
	var obj;
	
	var noClick = function() {
		parentDiv =$(this).parents("div.parentDiv").last(); //find the parentDiv of the question based on the step clicked on 
		console.log(parentDiv);
		var script = (parentDiv.next().text()); //get the trace value for this question
		script = script.substring(0, script.search("addVisualizerToPage")); //get code that evaluateds trace array
		eval(script); //evaulate script
		currInstr = parseInt($("#curInstr", parentDiv).text().split(" ")[1]); //current step based on the visualizer

		try{     
                        currInstrLine = parseInt((trace["trace"])[currInstr-1]["line"]);//line that program is currently on
                }catch(error){
                        $(parentDiv).find("#answerTruth").remove();
                        $(parentDiv).find("#dataViz").after("<div id=answerTruth style='font-size:40px'><b>Complete</b></div>");
			return;
                }
	
		nextInstrLine = parseInt((trace["trace"])[currInstr]["line"]); //line that program should go to next
		if((trace["trace"])[currInstr]["event"]=="return"&&currInstrLine==nextInstrLine){
			nextInstrLine=parseInt((trace["trace"])[currInstr+1]["line"]); //line that program should go to next
		}
		var currLine=this.id; //the line that user clicked on 
		var answerTruth = (("lineNo"+(nextInstrLine))==currLine);
		if(answerTruth)		
		{
			$(parentDiv).find("#vcrControls").children().attr("disabled",false);

			$(parentDiv).find("#answerTruth").remove();
			$(parentDiv).find("#dataViz").after(correctImage);
			var fwdButton = $(parentDiv).find("#jmpStepFwd");			
						
			var timeout = 0;			
			while("lineNo"+currInstrLine!=currLine)
			{	$(fwdButton).trigger("click");			
				currInstr = parseInt($("#curInstr", parentDiv).text().split(" ")[1]);
			

				currInstrLine = parseInt((trace["trace"])[currInstr-1]["line"]);
				timeout++;				
				if(timeout==20)
					break;
			}	
			$("[id=vcrControls]").children().attr("disabled",true);
			
			if($(parentDiv).next().next().hasClass("manualQuestionDiv")){
				$(parentDiv).next().next().remove();
			}
			if(parentDiv.attr("id") in manualQuestionStack){
				if(currInstr in manualQuestionStack[parentDiv.attr("id")]){
					$(parentDiv).next().after(manualQuestionStack[parentDiv.attr("id")][currInstr]);
					$(parentDiv).attr("disabled", true);
					$(parentDiv).addClass("waitingStory");
				}
			}
		}		
		else{
			$(parentDiv).find("#answerTruth").remove();
			$(parentDiv).find("#dataViz").after(incorrectImage);		

		}


	}	

	$(".lineNo").on("click", noClick);

	//Attach Handler to element with class "submitManual" so that it runs function manualCheck on click
    //attaching handler to dynamic children through static parent 
	$("body").on("click", ".submitManual", manualCheck);
	
	//Define function handler for  
	$("#question").on('input',function(e){
		var question = $(this).val();
		console.log(question);
		if(question.indexOf("line")!=-1){
			console.log("True");

		var script = (parentDiv.next().text());
		script = script.substring(0, script.search("addVisualizerToPage"));
		console.log(script);
		eval(script);
		}
	});
}
