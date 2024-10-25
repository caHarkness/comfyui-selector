$(function() {
    var consoleErrorHandler = console.error;
    var visualErrorHandler = function(message)
    {
        ConfirmationModal.fnShow(message, { theme: "danger" });
    };

    window.onerror = function(error, url, line, column, message)
    {
        visualErrorHandler(message);
    };

    console.error = function(message)
    {
        consoleErrorHandler(message);
        visualErrorHandler(message);
    };
});
