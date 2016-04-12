$(document).on('ready', function(event) {

    /// async load css by flipping the media attribute to all
    $('link[rel="stylesheet"]').attr('media', 'all');

    // page based JS calls
    var page_path = window.location.pathname;

    if (page_path.indexOf("manager/spaces") !== -1) {
        console.log("at spaces");
    } else if (page_path.indexOf("manager/items") !== -1){
        console.log("at items");
    } else {
        console.log("at manager");
        // if at /manager.... load space and items content via ajax
        $("#spaces").load("/manager/spaces/");
        $("#items").load("/manager/items/");
    }

});
