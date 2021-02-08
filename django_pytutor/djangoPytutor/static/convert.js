var request=null;
var csrftoken=null;
var count = 0;
$(document).ready(function(){
	csrftoken = $('[name=csrfmiddlewaretoken]')[0].value;
	$(".inner-container").on('click', '.convert-btn', convert);
	$(".inner-container").on('click', '.add-manual-btn', addManualQuestion);
	$(".inner-container").on('click', '.del-story-btn', delStoryQuestion);
	$(".inner-container").on('click', '.del-manual-question', delManualQuestion);
	$("#config-btn").on('click', convertJson);
});

/**
 * This function is the parser function for the Python file in backend.
 * Will read into the current HTML document, assembling the file into
 * a json file that can be read by the Python file.
 */
function convertJson() {
	// Notes:
	// ws-title: inside of ws-title-input
	// story questions: inside of question-container classes
	// manual-questions: inside of manual-container classes

	retJson = {};

	// Step 1: parse and get the wsTitle
	retJson['wsTitle'] = $("#ws-title-input").val();

	// Step 2: get all story questions, parse into them. Also, find manual Qs.
	let storyQuestions = $(".question-container");
	for (let i = 0; i < storyQuestions.length; ++i) {
		// Create dictionary to represent each problem
		let prob = {};

		// Identify trace.
		let trace = $(storyQuestions[i]).find(".story-question").val();

		// Identify question name.
		let traceTitle = $(storyQuestions[i]).find(".question-name").val();
		prob["problemName"] = traceTitle;
		prob["stepNumber"] = 1;
		// get all manual containers, store into iteratable list.
		let manualContainer = $(storyQuestions[i]).find(".manual-container").toArray();
		let manualQuestions = []
		for (let j = 0; j < manualContainer.length; ++j) {
			// Parses into manual containers, finds the necessary info for manual questions.
			let question = {}
			question['question'] = $(manualContainer[j]).find(".question-prompt").val();
			let stepNumH2 = $(manualContainer[j]).find(".line-num").text().split(" ")
			question['stepNumber'] = stepNumH2[stepNumH2.length - 1].replace(":","");
			question['answer'] = $(manualContainer[j]).find(".question-ans").val();

			// pass finished json parse into manualQuestion list above
			manualQuestions.push(question);
		}

		// Add to outer dict that represents each python trace.
		prob['manualQuestion'] = manualQuestions;

		// Below is temporary TODO
		prob["trace"] = trace;
		retJson['pathToPyFile.py_' + i] = prob;
	}

	$.ajax({
		method:"POST",
		url: "saveJson",
		data: {
			// here getdata should be a string so that
			// in your views.py you can fetch the value using get('getdata')
			'confJson': JSON.stringify(retJson)
		},
		dataType: 'json',
		success: function (response, status) {
			window.open(response.WsPath, '_blank');
		},
		error: function (res) {
			alert(res.status);
		}
	});
}

function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
	beforeSend: function (xhr, settings) {
		// if not safe, set csrftoken
		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});

function delManualQuestion() {
	let thisManual = $(this).parent();
	$.confirm({
		title:"Warning!",
		content: "You are about to delete the manual question. Are you sure you want to?",
		buttons: {
			confirm: function() {
				thisManual.remove();
			},
			cancel: () => {return}
		}
	})
}

function delStoryQuestion() {
	let thisStory = $(this).parent();
	$.confirm({
		title: "Warning!",
		content: "You are about to delete this story question. Are you sure you want to?",
		buttons: {
			confirm: function() {
				thisStory.remove();
			},
			cancel: function() {
				return;
			}
		}
	});

}

function addManualQuestion() {
	TEMPLATE = `
<div class="manual-container">
    <h2 class="line-num">Enter Manual Question Here for Line ###:</h2>
    <input class="manual-question question-prompt"/>
    <h2>Enter Answer Here:</h2>
	<input class="manual-question question-ans"/>
	<button class="del-manual-question">Delete</button>
</div>

<hr>
`;
	let thisStory = $(this).parent();
	// check if a question already exists at this step
	let step =  $(this).prev(".problem").find("#curInstr").text().split(" ")[1];
	// Above should locate correct step number.
	console.log(thisStory.children('.manual-container').toArray())
	for (let i = 0; i < thisStory.children(".manual-container").toArray().length; ++i) {
		// Locate h2 titled "Enter Your Step Number Here ###""
		let splitLineArr = $(thisStory.children(".manual-container").toArray()[i]).find(".line-num").text().split(" ")
		// Parse into h2 to find the step num of the current (ith) manual question.
		if (splitLineArr[splitLineArr.length - 1] == step + ":") {
			// Check if line's step number already has a manual question.
			$.alert({
				title: "Error!",
				content: "There is already a manual question on step line " + step +"."
			})
			return;
		}
	}

	// Find way to move <hr> above.
	thisStory.append(TEMPLATE.replace("###", step))
}

function convert() {
	let code = $($(this).prevAll(".story-question")[0]).val();
	let thisStory = $(this).parent();
	let questionContainer = thisStory.parent();
	// delete all previous manual questions upon selection, after alert.
	if (questionContainer.has(".manual-container").length) {
		$.confirm({
			title: "Warning!",
			content: "There are already manual questions from a previous preview. If you convert the code, the previous questions will be overwritten. Do you still want to create a new trace?",
			buttons: {
				confirm: function() {
					while (questionContainer.has('.manual-container').length != 0) {
						questionContainer.find(".manual-container").remove();
					}
				},
				cancel: function() {
					return;
				}
			}
		})
	}
	$.ajax({
		method:"POST",
		url: "convert",
		data: {
			// here getdata should be a string so that
			// in your views.py you can fetch the value using get('getdata')
			'code': JSON.stringify(code)
		},
		dataType: 'json',
		success: function (response, status) {
			let newDivId = null;
			let isNext = thisStory.next(".problem").length;
			if(isNext){
				 newDivId = thisStory.next(".problem").attr("id");
			}
			else{
				newDivId = "p"+count+"_py";
				$(thisStory).after(`<div id="`+newDivId+`" class="problem parentDiv"></div>`)
				count++;
			}
			success(response, newDivId)
		},
		error: function (res) {
			alert(res.status);
		}
	});
	let manualButton = thisStory.next(".add-manual-btn");
	// Why does that work, but not "$(this).parent().next('.add-manual-btn')????"
	manualButton.addClass("add-manual-display");

	//TODO: add the manual question converter.
}



function success(data, divId){

	addVisualizerToPage(data, divId, {
										startingInstruction: 0,
										hideCode: false,
										lang: "py3",
										disableHeapNesting: true//,
										//verticalStack: window.matchMedia("(max-width: 1768px)").matches
									});
	  console.log("post succeeded, got back %o", data);
}
