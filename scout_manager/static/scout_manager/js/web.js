$(function(){

    /// async load css by flipping the media attribute to all
    $('link[rel="stylesheet"]').attr('media', 'all');

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


    // page based JS calls
    var page_path = window.location.pathname;

    // ignore query params
    page_path = page_path.split("?")[0];

    var list_path = new RegExp("\/manager\/spaces\/?$");
    var items_edit_path = new RegExp("\/manager\/items\/[0-9].+\/?$");
    var items_add_path = new RegExp("\/manager\/items\/add\/?$");
    var items_add_batch_path = new RegExp("\/manager\/items\/add\/batch\/?$");
    var spaces_add_path = new RegExp("\/manager\/spaces\/add\/?$");
    var spaces_edit_path = new RegExp("\/manager\/spaces\/[0-9].+\/?$");

    if (spaces_add_path.test(page_path) || spaces_edit_path.test(page_path)) {
        Forms.init_form();
        Maps.init_picker();
    } else if (items_add_path.test(page_path) || items_edit_path.test(page_path)) {
        Forms.init_form("items");
    } else if (list_path.test(page_path)) {
        //List.init();
    } else if (items_add_batch_path.test(page_path)) {
        Forms.handle_item_row_add();
        Forms.handle_multi_item_row_add();
        $(".item-entry-row").first().hide();
        Forms.handle_delete_item_row();
        Forms.handle_submit_item_batch();
        Forms.validate_batch();
        $("#submit_form :input").on('input', function (e) {
            Forms.validate_batch();
        })
    }

    // datatables
    $('#sortable_datatables').DataTable({
        "paging": false,
        "dom": '<"top"f>rt<"bottom"lp><"clear">',
        "order": [[ 1, "asc" ]],
        fixedHeader: true
    });

});

$(window).scroll(function(){
    var sticky = $('.sticky'),
        scroll = $(window).scrollTop();

    if (scroll >= 230) sticky.addClass('fixed');
    else sticky.removeClass('fixed');
});
