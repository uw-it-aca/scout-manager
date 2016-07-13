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

        // initial client validation stuff
        $('#add_edit_form').validator('validate');

        // custom checkbox group validator
        Forms.handle_checkbox_group_clicks();
        Forms.validate_required_checkbox_group();

        Forms.handle_app_type_clicks();
        Forms.validate_required_app_type();
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
        $(container).css("background-image" , "url(data:image/png;base64,"+image_data,+")");
    },

    image_add: function(input) {

        // read the image from file input and display in preview list
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                //$('#mgr_list_spot_images').append('<div class="col-md-4"><div class="well" style="padding:0;"><div class="mgr-edit-img-container" style="url(' + e.target.result +')"></div>');
                Forms.image_check_count();
            };
            reader.readAsDataURL(input.files[0]);
        }
    },

    image_delete: function() {

        // remove image from list to be uploaded
        $('#mgr_list_spot_images').on('click', '.mgr-delete-image', function() {
            var wrapper_elm = $(this).siblings("div.mgr-edit-img-container").first();
            var image_id = $(wrapper_elm).attr("data-id");
            var image_etag = $(wrapper_elm).attr("data-etag");

            if(window.removed_images !== undefined){
                window.removed_images.push({id: image_id,
                                           etag: image_etag});
            } else {
                window.removed_images = [{id: image_id,
                                          etag: image_etag}];
            }
            $(this).parent().parent("div").remove();
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

        // handle radio button change for non-study types
        $("#add_new_extended_info input[name='extended_info:app_type']").change(function(e){
            if($(this).val() == 'food') {
                $("#extended_food_template").show();
                $("#extended_study_template").hide();
                $("#study_radio").prop('checked', false);
            }
            else if($(this).val() == 'tech') {
                console.log("tech lksadfjsd")
                $("#extended_food_template").hide();
                $("#extended_study_template").hide();
                $("#study_radio").prop('checked', false);
            }
        });

        // handle radio lick event for study type
        $("#study_radio").click(function(e){
            $("#extended_food_template").hide();
            $("#extended_study_template").show();
            $("#add_new_extended_info input[name='extended_info:app_type']").prop('checked', false);
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

    // custom validation stuff

    validate_required_checkbox_group: function() {

        // get the count of all checkboxes for a given grouping
        $(".checkbox-group.required input[type='checkbox']").each(function() {

            // get the checkbox groupings id
            var group_id = $(this).closest(".well").attr('id');
            // get count of checkboxes checked for given grouping
            var count_checked = $("#"+group_id+" [type='checkbox']:checked").length;

            // if more than 1 checked, remove error css
            if(count_checked > 0) {
                $(this).closest(".checkbox-group").removeClass("has-error");
            }
            else {
                $(this).closest(".checkbox-group").addClass("has-error")
            }

        });
    },

    handle_checkbox_group_clicks: function() {
        // handle clicks for any checkboxes in a "checkbox-group" grouping
        $(".checkbox-group.required input[type='checkbox']").change(function(e) {
            Forms.validate_required_checkbox_group();
        });
    },

    validate_required_app_type: function() {

        $(".radio-group.required input[type='radio']").each(function() {

            var count_checked = $("#app_type_radio [type='radio']:checked").length;

            // if more than 1 checked, remove error css
            if(count_checked > 0) {
                $("#app_type_radio").removeClass("has-error");
            }
            else {
                $("#app_type_radio").addClass("has-error")
            }

        });

    },

    handle_app_type_clicks: function() {
        // handle clicks for any checkboxes in a "checkbox-group" grouping
        $("#app_type_radio input[type='radio']").change(function(e) {
            Forms.validate_required_app_type();
        });
    },

    init_delete_button: function () {
        $("button.btn-delete").on("click", function(e) {
            var spot_id = Forms._get_spot_id();
            console.log(spot_id)
            var etag = Forms._get_spot_etag();
            console.log(etag)
            Spot.delete_spot(spot_id, etag);
        });
    },

    _get_spot_id: function () {
        return $('input[name="id"]').attr("value")
    },

    _get_spot_etag: function () {
        return $('input[name="etag"]').attr("value")
    }

};
