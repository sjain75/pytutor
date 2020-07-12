$('[id="editBtn"]').css("color", "white");

$('[id="legendDiv"]').html('<svg id="prevLegendArrowSVG"><polygon points="0,3 12,3 12,0 18,5 12,10 12,7 0,7"' +
    ' fill="#c9e6ca"></polygon></svg> line that has just executed<p style="margin-top: 4px"><svg id="curLegendArrowSVG"><polygon points="0,3 12,3 12,0 18,5 12,10 12,7 0,7" fill="#e93f34"></polygon></svg> current line</p>')

console.log($(".submitManual"))
$(".submitManual").addClass("button");

$('[id="heapHeader"]').css("color", "white");

var sidebar = $('.sidebar ul')
$('h2').each(function (index) {
    var number = $(this).text().split(" ");
    var number = number[number.length - 1];
    sidebar.append('<li class="sidebar-item"><a href="#problem' + number + '">Problem ' + number +'</a></li>');
});
