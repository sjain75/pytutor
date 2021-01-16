$(window).on('load', function () {
    // $(window).on('scroll', function() {
    //     if ($(window).scrollTop() > 10) {
    //         $('.navbar').addClass('nav-active');
    //     } else {
    //         $('.navbar').removeClass('nav-active');
    //     }
    // })

    $("#addQuestion").on('click', function () {
        var TEMPLATE =
        '                <div class="question-container">  '  +
        '                       <div class="question-name-container">  '  +
        '                           <h2>Enter Question Title Here:</h2>  '  +
        '                           <textarea class="question-name story-question-title" id=""></textarea>  '  +
        '                       </div>  '  +
        '                       <div class="story-container">  '  +
        '                           <h2>Enter Python Code Here:</h1>  '  +
        '                           <textarea class="story-question"></textarea>  '  +
        '                           <button class="convert-btn" onclick="convert()">Preview</button>  '  +
        '                       </div>  ' +
        '                </div>' +
        '                <hr/>';
        $(".inner-container").append(text);
    })
})
