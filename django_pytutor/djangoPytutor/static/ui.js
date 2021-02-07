$(window).on('load', function () {
    $(window).on('scroll', function() {
        if ($(window).scrollTop() > 10) {
            $('.navbar').addClass('nav-active');
        } else {
            $('.navbar').removeClass('nav-active');
        }
    })

    $("#addQuestion").on('click', function () {
        var TEMPLATE =
        '                <div class="question-container">  '  +
        '                       <button class="del-story-btn">Delete Entire Story Question</button>' +
        '                       <div class="question-name-container">  '  +
        '                           <h2>Enter Question Title Here:</h2>  '  +
        '                           <textarea class="question-name story-question-title" id=""></textarea>  '  +
        '                       </div>  '  +
        '                       <div class="story-container">  '  +
        '                           <h2>Enter Python Code Here:</h1>  '  +
        '                           <textarea class="story-question"></textarea>  '  +
        '                           <button class="convert-btn">Preview</button>  '  +
        '                       </div>  ' +
        '                       <button class="add-manual-btn">Add Manual Question Here</button>' +
        '                       <hr/>'+
        '                 </div>';
        $(".inner-container").append(TEMPLATE);
    })
})