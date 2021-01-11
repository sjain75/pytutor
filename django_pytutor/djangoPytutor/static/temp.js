var request=null;
var csrftoken=null;
$(document).ready(function(){
csrftoken = $('[name=csrfmiddlewaretoken]')[0].value;

request = new Request(
    "template",
    {headers: {'X-CSRFToken': csrftoken}}
);
});
function convert() {
	let code = $("#demoCode").val();

	fetch(request, {
	    method: 'POST',
	    mode: 'same-origin',  // Do not send CSRF token to another domain.
		data: JSON.stringify({"code":code})
	}).then(function(response) {
	    response.json().then(body => console.log(body));

	});

	// $.ajax({
	//   type: "POST",
	//   url: "http://127.0.0.1:8000/template",
	//   data: {CSRF: csrftoken, 'hi':1},
	//   success: success,
	//   dataType: "json"
	// });

/*	$.post({
	  type: "POST",
	  url: "http://127.0.0.1:8000/template",
	  data: JSON.stringify({"code":code}),
	  contentType: "application/json; charset=utf-8",
	  dataType: "json"
	}).done(function(data) {
		if (data.statusCode == 200) {
		  console.log("post succeeded, got back %o", data);
		} else {
		  console.log("post returned status "+data.statusCode);
		  console.log("error body %o", data.body);
		}
	});*/
}

function success(data){
	  console.log("post succeeded, got back %o", data);
}
