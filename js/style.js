



$("div.ExecutionVisualizer").css("width", "50vw");
// $("#lec-07_w19_py").css("width", "50vw");
$(".problem").css({
    display: "flex",
    flexDirection: "column",
    alignItems: "center"
});
$('[id="stackHeader"]').css("color", "white");
$('[id="heapHeader"]').css("color", "white");
$('[id="langDisplayDiv"]').css("color", "white");
$('[id="printOutputDocs"]').css("color", "white");
$('[id="legendDiv"]').css("color", "white");
$('[id="editBtn"]').css("color", "white");

$("td").css("color", "white");
$('[id="v1__globals"]').css("color", "black");
// $('[id="stackFrameVar"]').css("color", "black");


$('[id="jmpStepBack"]').addClass("button");
$('[id="jmpStepBack"]').css({
    height: "auto",
    padding: "10px"
});

$('[id="jmpStepFwd"]').addClass("button");
$('[id="jmpStepFwd"]').css({
    height: "auto",
    padding: "10px"
});

$(".submitManual").addClass("button");
$(".submitManual").css({
    height: "auto",
    padding: "10px"
});