$(document).on('ready', function(event) {

    /// async load css by flipping the media attribute to all
    $('link[rel="stylesheet"]').attr('media', 'all');

    // page based JS calls
    var page_path = window.location.pathname;

    if (page_path.indexOf("manager/spaces") !== -1) {
        console.log("at spaces");
        Spot.init_events();
    } else if (page_path.indexOf("manager/items") !== -1){
        console.log("at items");
    } else {
        console.log("at manager");
        // if at /manager.... load space and items content via ajax
        $("#spaces").load("/manager/spaces/");
        //$("#items").load("/manager/items/");
    }

    Forms.init_form();

    Maps.init_maps();

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
