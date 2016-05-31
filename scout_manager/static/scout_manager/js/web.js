$(document).on('ready', function(event) {

    /// async load css by flipping the media attribute to all
    $('link[rel="stylesheet"]').attr('media', 'all');

    Forms.init_form();

    Maps.init_picker();

    // Function to serialize form data into an JS object
    $.fn.serializeObject = function() {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function() {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };

});
