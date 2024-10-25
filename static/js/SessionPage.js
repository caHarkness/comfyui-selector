$(function() {
    SessionPage = {};

    SessionPage.fnSaveInput = function()
    {
        localStorage.setItem(
            "userMessage",
            $("[name='user-input']").first().val());
    };

    SessionPage.fnInit = function()
    {
        $("[name='user-input']").on("input", function() {
            SessionPage.fnSaveInput();
        });

        if (localStorage.getItem("userMessage"))
        {
            $("[name='user-input']")
                .first()
                .val(localStorage.getItem("userMessage"));
        }
    };

    SessionPage.fnAddMessage = function(o)
    {
        var elem = $(".message-template").first().clone();
        var body = elem.find("[name='body']").first();

        body.html(o.body);
        elem.find("[name='author']").first().html(o.author);

        switch (o.author)
        {
            case "Assistant":
                elem.addClass("reply");
                body.addClass("alert alert-primary mb-1");
                break;

            case "User":
                elem.addClass("query");
                body.addClass("alert alert-secondary mb-1");
                break;
        }

        elem.o      = o;
        elem.body   = body;
        elem.removeClass("message-template d-none");

        $("#messages")
            .first()
            .append(elem);

        return elem;
    };

    SessionPage.fnSend = function()
    {
        var message = $("[name='user-input']").first().val();

        /**/
        var elem1 = SessionPage.fnAddMessage({
            author: "User",
            body: message
        });


        var elem2 = SessionPage.fnAddMessage({
            author: "Assistant",
            body: "..."
        });

        SessionPage.fnScroll();

        $.ajax({
            url: "/v1/stub",
            type: "post",
            contentType: "application/json",
            data: JSON.stringify({
                "category":         $("[name='category']").first().val(),
                "channel_topic":    $("[name='channel_topic']").first().val(),
                "user":             $("[name='user']").first().val(),
                "user_roles":       $("[name='user_roles']").first().val(),
                "user_message": message
            }),
            success: function(data)
            {

                $.ajax({
                    url: "/v1/process",
                    type: "post",
                    contentType: "application/json",
                    data: JSON.stringify(data),
                    success: function(data)
                    {
                        elem2.body.removeClass("alert alert-primary");
                        elem2.body.css("padding", "0");
                        elem2.body.html("");

                        for (const i of data.output_files)
                        {
                            var img = $("<img />");

                            img.attr("src", `data:image/png;base64, ${i.file_data}`);
                            img.attr("image-data", i.file_data);
                            img.attr("file-name", i.file_name);
                            img.attr("download", `${i.file_name}`);
                            // img.css("display", "none");

                            img.on("click", function() {
                                var anchor      = document.createElement("a");
                                anchor.href     = img.attr("src");
                                anchor.target   = "_blank";
                                anchor.download = `${i.file_name}`;
                                anchor.click();
                            });

                            
                            elem2.body.append(img);
                        }

                        setTimeout(function() {
                            SessionPage.fnScroll();
                        }, 250);
                    }
                });
                
            },
            error: function (xhr, status, error)
            {
            }
        });
    }

    SessionPage.fnScroll = function()
    {
        window.scrollTo(0, document.body.scrollHeight);
    };

    SessionPage.fnInit();
});
