String.prototype.replaceWhile = function(str, replacement)
{
    var a = this;

    while (a.includes(str))
        a = a.replace(str, replacement);

    return a;
};

String.prototype.unspace = function()
{
    var a = this;

    // Remove newlines, tabs, and carriage returns:
    ["\n", "\t", "\r"].forEach(
        function (i) {
            a = a.replaceWhile(i, "");
        });

    a = a.replaceWhile("  ", " ");
    a = a.trim();

    return a;
};

// A function to see if a "normalized" string contains all of the pieces, but not necessarily in order:
String.prototype.hasWords = function(str)
{
    var a = this.unspace().toLowerCase();
    var b = str.unspace().toLowerCase();

    var aArray  = a.split(" ");
    var bArray  = b.split(" ");
    var pass    = true;

    bArray.forEach(
        function (i) {
            if (!(a.includes(i)))
                pass = false;
        });

    return pass;
};

// A bi-directional version of String.prototype.hasWords:
String.prototype.isLike = function(str)
{
    var a = this.unspace().toLowerCase();
    var b = str.unspace().toLowerCase();

    var aArray  = a.split(" ");
    var bArray  = b.split(" ");
    var match   = false;

    if (a.includes(b)) return true;
    if (b.includes(a)) return true;

    aArray.forEach(
        function (i) {
            if (bArray.includes(i))
                match = true;
        });

    if (match) return true;

    bArray.forEach(
        function (i) {
            if (aArray.includes(i))
                match = true;
        });

    return match;
};

// Like String.includes(), but checks for unspaced, lowercase versions of the input string in self:
String.prototype.checkFor = function(str)
{
    var a = this.unspace().toLowerCase();
    var b = str.unspace().toLowerCase();

    if (a.includes(b))
        return true;

    return false;
};

String.prototype.copy = function()
{
    navigator
        .clipboard
        .writeText(this);

    if (typeof(toastr) === "object")
        if (typeof(toastr.success) === "function")
            toastr.success("Text copied to the clipboard");
};
