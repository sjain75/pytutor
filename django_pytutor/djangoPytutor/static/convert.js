var request=null;
var csrftoken=null;
var count = 0;
$(document).ready(function(){
	csrftoken = $('[name=csrfmiddlewaretoken]')[0].value;
	$(".inner-container").on('click', '.convert-btn', convert);
	$(".inner-container").on('click', '.add-manual-btn', addManualQuestion);
	$(".inner-container").on('click', '.del-story-btn', delStoryQuestion);
	$(".inner-container").on('click', '.del-manual-question', delManualQuestion);
});

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
    <h2>Enter Manual Question Here for Line ###:</h2>
    <input class="manual-question"/>
    <h2>Enter Answer Here:</h2>
	<input class="manual-question"/>
	<button class="del-manual-question">Delete</button>
</div>
`;
	let thisStory = $(this).parent();
	// check if a question already exists at this step
	let step =  $(this).prev(".problem").find("#curInstr").text().split(" ")[1];
	// Above should locate correct step number.
	for (let i = 0; i < thisStory.has(".manual-container").length; ++i) {
		// TODO find different value than "has.""
		if (thisStory.has(".manual-container")[i].find("h2").text().split(" ")[thisStory.has(".manual-container").length - 1] == step) {
			$.alert({
				title: "Error!",
				content: "There is already a manual question on step line " + step +"."
			})
			return;
		}
	}
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
