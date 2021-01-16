var request=null;
var csrftoken=null;
var count = 0;
$(document).ready(function(){
	csrftoken = $('[name=csrfmiddlewaretoken]')[0].value;

	request = new Request(
		// One error is coming from the fact that the convert view
		// is not totally functional. Work on this to get it working,
		// then try to route everything together
	    "convert",
	    {headers: {'X-CSRFToken': csrftoken}}
	);
	$(".convert-btn").on("click", convert);
});
function convert() {
	let code = $($(this).prevAll(".story-question")[0]).val();
	let thisStory = $(this).parent();
	fetch(request, {
	    method: 'POST',
	    mode: 'same-origin',  // Do not send CSRF token to another domain.
		data: JSON.stringify({"code":code})
	}).then(function(response) {
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
		response.json().then(trace => success(trace, newDivId));
	});
}

function success(data, divId){

	addVisualizerToPage(data, divId, {
										startingInstruction: 0,
										hideCode: false,
										lang: "py3",
										disableHeapNesting: true,
										verticalStack: window.matchMedia("(max-width: 1768px)").matches
									});
	  console.log("post succeeded, got back %o", data);
}
