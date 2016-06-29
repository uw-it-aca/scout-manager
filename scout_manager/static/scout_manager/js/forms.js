var Forms = {

    init_form: function(){

        Forms.hours_clear();
        Forms.hours_add();
        Forms.hours_grouping_clearfix();
        Forms.load_images();
        Forms.image_delete();
        Forms.image_check_count();
        Forms.toggle_extended_info();
        Forms.toggle_is_hidden();
    },

    // hours functions

    hours_clear: function(){
        // clear hours for a given day
        $(".mgr-clear-hours").click(function(e) {
            $(this).parent().siblings().find("input[type=time]").val("");
        });
    },

    hours_add: function(){
        // add hours input fields
        $(".mgr-add-hours").click(function(e) {

            var hours_blocks = $(this).parent().siblings().find('.mgr-hours-block');

            var empty_hours = $(hours_blocks[0]).clone();
            $(empty_hours).find("input").val("");

            $($(this).parent().parent().find('.mgr-current-hours')).append(empty_hours);

        });
    },

    hours_grouping_clearfix: function(){
        $("<div class='clearfix'></div>").insertBefore(".mgr-hours-group .col-md-4:nth-child(4)");
        $("<div class='clearfix'></div>").insertBefore(".mgr-hours-group .col-md-4:last");
    },

    // image handling functions

    load_images: function() {
        // Get the image URLs and load them via AJAX
        var images = $(".mgr-edit-img-container");
        $.each(images, function(idx, image_container){
            var url = $(image_container).attr("data-url");
            $.ajax({
                url: url,
                type: "GET",
                process_data: false,
                success: function(data, textStatus, request) {
                    Forms.attach_image(image_container, data, request.getResponseHeader('etag'))
                },
                error: function(xhr, status, error) {
                }
            });
        });
    },

    attach_image: function(container, image_data, etag) {
        // AJAX callback to attach images to DOM
        // and set data-csrf to returned CSRF header
        $(container).attr('data-etag', etag);
        var img = $("<img>", {src:"data:image/png;base64,"+image_data,
                              width: '100'});
        $(container).append(img);
    },

    image_add: function(input) {

        // read the image from file input and display in preview list
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#mgr_list_spot_images').append('<div class="col-md-4"><div class="well" style="height:200px;"><img src="' + e.target.result +'" style="width:100px;"><label for="" class="scope"><input type="radio" name="" id="" />default</label><input type="button" value="Delete image" class="mgr-delete-image" /></div></div>');
                Forms.image_check_count();
            };
            reader.readAsDataURL(input.files[0]);
        }
    },

    image_delete: function() {

        // remove image from list to be uploaded
        $('#mgr_list_spot_images').on('click', '.mgr-delete-image', function() {
            var image_id = $(this).siblings("img").first().attr("data-id");
            if(window.removed_images !== undefined){
                window.removed_images.push(image_id);
            } else {
                window.removed_images = [image_id];
            }
            $(this).parent("div").remove();
            Forms.image_check_count();
        });
    },

    image_check_count: function() {

        // handle display of empty message
        if( $('#mgr_list_spot_images > div').length < 1 ){
            console.log("empty image list");
            $('#mgr_list_spot_empty').show();
        }
        else {
            $('#mgr_list_spot_empty').hide();
        }
    },

    toggle_extended_info: function() {

        // handle extended_info field for adding new space
        $("#add_new_extended_info input[name='extended_info:app_type']").change(function(e){
            if($(this).val() == 'food') {
                $("#extended_food_template").show();
                $("#extended_study_template").hide();
            }
            else {
                $("#extended_food_template").hide();
                $("#extended_study_template").show();
            }
        });

    },

    toggle_is_hidden: function() {

        $("#toggle_is_hidden").click(function() {
            var checkBoxes = $("input[name='extended_info:is_hidden']");
            checkBoxes.prop("checked", !checkBoxes.prop("checked"));
            // submit "save changes"

            Spot.submit_spot();

        });

    },

};
