function convert() {
	let code = $("#demoCode").val();

	$.ajax({
	  type: "POST",
	  url: "http://127.0.0.1:8000/template",
	  data: "{'hi':1}",
	  success: success,
	  dataType: "json"
	});

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
