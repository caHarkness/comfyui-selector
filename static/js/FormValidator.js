$(function() {
    FormValidator = {};
    FormValidator.onPass = function(args)
    {
        var selector = $(document);
        var callback = null;

        if (arguments.length > 0)
            callback = arguments[0];

        if (arguments.length > 1)
        {
            selector = arguments[0];
            callback = arguments[1];
        }

        var pass = 1;

        if (typeof selector === "string")
            selector = $(selector);

        selector.find("*[fv-regex]").each(function(i, x) {
            if (pass == 0)
                return;

            x = $(x);

            var tagStr          = x.get(0).tagName.toLowerCase();
            var regexStr        = x.attr("fv-regex");
            var warningStr      = x.attr("fv-warning");
            var targetStr       = x.attr("fv-target");
            var classStr        = x.attr("fv-class");
            var evalStr         = null;

            // If no failure class is specified, use Bootstrap's .border-danger:
            if (classStr == null || classStr.length < 1)
                classStr = "border-danger";

            if (warningStr == null)
                warningStr = "";

            warningStr = `${warningStr}. Please correct the highlighted input and try again.`;
            warningStr = warningStr.trim();
            warningStr = warningStr.replace(/^\. /gi, "");
            warningStr = warningStr.replace(/\.{2,} /gi, ". ");
            warningStr = warningStr.replace(/ {2,}/, " ");

            if (tagStr == "input")
                evalStr = x.val();

            if (tagStr == "textarea")
                evalStr = x.val();

            // Change the classes of a different element if the fail target is specified:
            if (targetStr !== null && typeof targetStr === "string" && targetStr.length > 0)
                x = $(targetStr);

            var regexObj = new RegExp(regexStr, "g");

            if (!evalStr.match(regexObj))
            {
                x.addClass(classStr);
                x.focus();
                x.select();
                console.error(warningStr);

                pass = 0;
                return;
            }

            x.removeClass(classStr);
        });

        if (pass == 1)
            if (typeof callback === "function")
                callback();
    };
});
