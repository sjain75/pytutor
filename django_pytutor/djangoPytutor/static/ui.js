$(window).on('load', function () {
    var counter = 1;
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
        '                           <textarea class="question-name" id="story-question-title-UNIQUE_IDENTIFIER"></textarea>  '  + 
        '                       </div>  '  + 
        '                       <div class="story-container">  '  + 
        '                           <h2>Enter Python Code Here:</h1>  '  + 
        '                           <textarea class="story-question" id="story-question-UNIQUE_IDENTIFIER"></textarea>  '  + 
        '                           <button class="convert-btn" onclick="convert()">Preview</button>  '  + 
        '                       </div>  ' +
        '                </div>' + 
        '                <hr/>';
        let text = TEMPLATE.replace(/UNIQUE_IDENTIFIER/g, counter++);
        $(".inner-container").append(text);
    })
})