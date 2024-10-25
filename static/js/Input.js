$(function() {
    Input = {};
    Input.fnSetTextareaHeight = function()
    {
        $("textarea").each(function(i, x) {
            x = $(x);

            x.css("minHeight", "0px");
            x.css(
                "minHeight",
                x[0].scrollHeight +
                    parseInt(x.css("paddingTop")) +
                    parseInt(x.css("paddingBottom")) +
                    "px"
                );
        });
    };
});


