$( document ).ready(function() {
	$("[id=vcrControls]").children().attr("disabled",true);
	
	$(".lineNo").each(function(){
		$(this).attr("style","cursor: pointer;")
		$(this).text("🔘");
	}); //replace all line numbers with something that looks more clickable
	var obj;
	var reload = function(){
		username = $("span#useremail").text();

		$(".manualQuestionDiv").each(function(){
				parentDiv=$(this);
				if(username!=""){
				if(!($(parentDiv).attr("sent")=="updated")){
					activity=($(parentDiv).prev().prev().attr("id"));
					(common.callLambda({"fn":"isAnswered", questionCode:activity},
						function (obj) {
							
						
							  if( !('error' in obj) && obj["body"]!="false" ) {
							     parentDiv = $("#"+obj["body"]).next().next();
							      $(parentDiv).attr("sent","updated");
							      $(parentDiv).find(".title-bar-chevron-container").html('<div aria-label="Activity completed" id="ember6016" class="zb-chevron title-bar-chevron orange large check filled ember-view"> </div>');
							      $(parentDiv).find(".chevron-container").html('<div aria-label="Question completed" id="ember6023" class="zb-chevron question-chevron orange medium check filled ember-view"> </div>');
							  }
							  else {
							      console.log(obj);
							  }
						}));   
						
				}
			}
		});

	};

	$(".reload").on("click",reload);
	var noClick = function() {
		parentDiv =$(this).parents("div").last(); //find the parentDiv of the question based on the step clicked on 
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
			$(parentDiv).find("#dataViz").after("<div id=answerTruth style='font-size:40px'><img width='8%' style='padding-left:2%' src='../resources/correct-checkmark.svg'></img></div>");
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

		}		
		else{
			$(parentDiv).find("#answerTruth").remove();
			$(parentDiv).find("#dataViz").after("<div id=answerTruth><img width='8%' style='padding-left:2%' src='../resources/incorrect-cross.svg'></img></div>");		

		}


	}	

	$(".lineNo").on("click", noClick);
	var notLoggedInAttempt = false;
	var manualCheck = function(){
		parentDiv = $(this).closest(".manualQuestionDiv");
		username = $("span#useremail").text();
		if(username==""){
			if(!notLoggedInAttempt){
				notLoggedInAttempt = true;
				$(parentDiv).append("<span id='notLoggedIn'>You are not logged in so none of these questions will be graded! But feel free to continue for practice! :)</span>");
			}
		}
		else{
			 username = $.trim(username);
			if(notLoggedInAttempt){
				$(parentDiv).children("#notLoggedIn").remove();
				notLoggedInAttempt = false;
			}
		}
		script = $(parentDiv).prev().text();
		script = script.substring(script.search("manualAnswer")); //get code that evaluateds trace array
		console.log(script);
		eval(script); //evaulate script
		userAnswer = $(parentDiv).find("#manualAnswer").val();
		answerTruth = userAnswer==manualAnswer;
		$(parentDiv.prev().prev()).find("#manualAnswerTruth").remove();

		if(answerTruth){
			$(parentDiv).find(".title-bar-chevron-container").html('<div aria-label="Activity completed" id="ember6016" class="zb-chevron title-bar-chevron orange large check filled ember-view"> </div>');
			$(parentDiv).find(".chevron-container").html('<div aria-label="Question completed" id="ember6023" class="zb-chevron question-chevron orange medium check filled ember-view"> </div>');
			if(username!=""){
				if(!($(parentDiv).attr("sent")=="updated")){
					activity=($(parentDiv).prev().prev().attr("id"));
					console.log(common.callLambda({"fn":"addNewAnswer", questionCode:activity},
						function (obj) {
							  if( !('error' in obj) ) {
							      console.log(obj);
							      $(parentDiv).attr("sent","updated");
							  }
							  else {
							      console.log(obj);
							  }
						    }
						));
				}
			}
		
		}
		else{
			 $(parentDiv).find(".chevron-container").html("<img width='40%' style='padding-left:2%' src='../resources/incorrect-cross.svg'></img>");

		}

	};


	questionHtmlString = '<div content_resource_id="32241403" class="manualQuestionDiv interactive-activity-container short-answer-content-resource participation large ember-view"><div class="activity-title-bar" data-ember-action="" data-ember-action-6015="6015"> <span aria-hidden="true" class="activity-type"> <div class="type">participation</div> <div class="label">activity</div> </span> <div class="separator"></div> <h6 class="activity-description"> <div class="activity-title">"""manualQuestionTitle"""</div><div class="title-bar-chevron-container"> </div> <!----></h6> </div> <div class="activity-payload"> <div class="activity-instructions"> </div> <div id="ember6017" class="content-resource short-answer-payload ember-view"> <div id="ember6019" class="question-set-question short-answer-question ember-view"><div class="question"> <div class="setup flex-row"> <div class="label">1)</div> <div class="text">"""manualQuestion"""</div> </div> <div class="question-container flex-row"> <div class="input"> <pre><textarea cols="20" rows="1" spellcheck="false" autocapitalize="false" id="manualAnswer" class="zb-text-area hide-scrollbar ember-text-area ember-view"></textarea></pre> <div class="buttons flex-row"> <button class="submitManual" class="check-button zb-button primary raised ember-view"><!----> <span class="title">Check</span> </button> <button id="ember6022" class="show-answer-button zb-button secondary ember-view"><!----> <span class="title">Show answer</span> </button> </div> </div> </div> </div> <div role="alert" aria-atomic="true" class="explanation "> <!----></div> <!----> <div class="chevron-container"> </div> </div> </div> <!----></div> </div>';

	//Take the simple div with class manual question and make it fancier. Runs at page load for each div with class "manualQuestion"
	$(".manualQuestion").each(function(){
		manualQuestionString= $(this).text();
		manualTitleString = $(this).prev().prev().prev().text(); 
		console.log(manualTitleString);
		privateQuestionHtml=questionHtmlString;
		privateQuestionHtml = privateQuestionHtml.replace('"""manualQuestion"""',manualQuestionString);
		privateQuestionHtml = privateQuestionHtml.replace('"""manualQuestionTitle"""',manualTitleString);

		$(this).after(privateQuestionHtml);
		$(this).remove();
	});

	//Attach Handler to element with class "submitManual" so that it runs function manualCheck on click
	$(".submitManual").on("click",manualCheck);
	
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
})
