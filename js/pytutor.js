var manualQuestionStack={};
var manualAnswer = "B";
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
			
			if($(parentDiv).next().next().hasClass("manualQuestionDiv")){
				$(parentDiv).next().next().remove();
			}
			if(parentDiv.attr("id") in manualQuestionStack){
				if(currInstr in manualQuestionStack[parentDiv.attr("id")]){
					$(parentDiv).next().after(manualQuestionStack[parentDiv.attr("id")][currInstr]);
				}
			}
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
		username = "sjain75"
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
		//eval(script); //evaulate script
		userAnswer = $(parentDiv).find(".manualAnswer").val();
		answerTruth = userAnswer==manualAnswer;
		$(parentDiv).find(".manualAnswerTruth").remove();

		if(answerTruth){
			$(parentDiv).find(".manualAnswer").after("<img class=manualAnswerTruth width='13%' style='padding-left:2%' src='../resources/correct-checkmark.svg'></img>");
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
			 $(parentDiv).find(".manualAnswer").after("<img class=manualAnswerTruth width='13%' style='padding-left:2%' src='../resources/incorrect-cross.svg'></img>");
		}

	};


	questionHtmlString=`<div content_resource_id="32241403" class="manualQuestionDiv">
				<div>"""manualQuestion"""</div> 
				<div style="margin-bottom: 5px;"><textarea style="width: 85%;" cols="20" rows="1" spellcheck="false" autocapitalize="false" class="manualAnswer"></textarea></div>
				<div><button class="submitManual button">Check</button></div>
			</div>`
	//Take the simple div with class manual question and make it fancier. Runs at page load for each div with class "manualQuestion"
	$(".manualQuestion").each(function(){
		manualQuestionString= $(this).text();
		let privateQuestionHtml=questionHtmlString;
		privateQuestionHtml = privateQuestionHtml.replace('"""manualQuestion"""',manualQuestionString);
		let parentScriptText =$($(this).prevAll("script")[0]).text();
		let parentScriptRefined  = parentScriptText.substring(parentScriptText.lastIndexOf("addVisualizerToPage")).split(", ");

		let parentStoryKey = parentScriptRefined[1].substring(1, parentScriptRefined[1].length-1);
		let parentStoryBeginsAt = Number(parentScriptRefined[2].substring(parentScriptRefined[2].lastIndexOf(":")+1));
		let questionStep = Number($(this).attr("step"));
		if(!(parentStoryKey in manualQuestionStack)){
			manualQuestionStack[parentStoryKey] = {};
		}
		manualQuestionStack[parentStoryKey][questionStep] = privateQuestionHtml;
		if(parentStoryBeginsAt+1==questionStep){
			$(this).after(privateQuestionHtml);}
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
