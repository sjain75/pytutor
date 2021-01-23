var request=null;
var csrftoken=null;
var count = 0;
$(document).ready(function(){
	csrftoken = $('[name=csrfmiddlewaretoken]')[0].value;
	$(".inner-container").on('click', '.convert-btn', convert);
	$(".inner-container").on('click', '.add-manual-btn', addManualQuestion);
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

function addManualQuestion() {
	TEMPLATE = `
<div class="manual-container">
    <h2>Enter Manual Question Here for Line ###:</h2>
    <input class="manual-question"/>
    <h2>Enter Answer Here:</h2>
    <input class="manual-question"/>
</div>
`;
	let thisStory = $(this).parent();
	let step =  $(this).prev(".problem").find("#curInstr").text().split(" ")[1];;
	// Above should locate correct step number.
	thisStory.append(TEMPLATE.replace("###", step))
}

function convert() {
	let code = $($(this).prevAll(".story-question")[0]).val();
	let thisStory = $(this).parent();
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
