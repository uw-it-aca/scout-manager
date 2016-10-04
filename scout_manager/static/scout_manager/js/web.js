$(document).on('ready', function(event) {

    /// async load css by flipping the media attribute to all
    $('link[rel="stylesheet"]').attr('media', 'all');

    // page based JS calls
    var page_path = window.location.pathname;

    // ignore query params
    page_path = page_path.split("?")[0];


    var list_path = new RegExp("\/manager\/spaces\/?$");
    var items_edit_path = new RegExp("\/manager\/items\/[0-9].+\/?$");
    var items_add_path = new RegExp("\/manager\/items\/add\/?$");
    var spaces_add_path = new RegExp("\/manager\/spaces\/add\/?$");
    var spaces_edit_path = new RegExp("\/manager\/spaces\/[0-9].+\/?$");

    if (spaces_add_path.test(page_path) || spaces_edit_path.test(page_path)) {
        console.log("at spaces");
        Forms.init_form();
        Maps.init_picker();
    } else if (items_add_path.test(page_path) || items_edit_path.test(page_path)) {
        console.log("at items");
        Forms.init_form("items");
    } else if (list_path.test(page_path)) {
        List.init();
        console.log('list view')
    } else {
        console.log("at home");
    }


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

$(window).scroll(function(){
    var sticky = $('.sticky'),
        scroll = $(window).scrollTop();

    if (scroll >= 230) sticky.addClass('fixed');
    else sticky.removeClass('fixed');
});
