var Forms = {

    init_form: function(form_type){
        Forms.hours_clear();
        Forms.hours_add();
        Forms.hours_grouping_clearfix();
        Forms.load_images();
        Forms.image_delete();
        Forms.image_upload();
        Forms.image_check_count();
        Forms.toggle_extended_info();
        Forms.toggle_is_hidden();
        Forms.toggle_item_active();
        Forms.init_validate();
        Forms.init_delete_button();
        Forms.init_campus_building_filter();
        Forms.sort_building_list();

        $("#campus_select").trigger("change");

        if(form_type === "items") {
            Forms.init_building_spot_filter();
            Forms.sort_spot_list();
            $("#building_select").trigger("change");
        }

        // handle submitting spot to server
        $("#submit_spot").click(Spot.submit_spot);
        $("#submit_item").click(Item.submit_item);

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

    image_upload: function() {

        $('#mgr_upload_image').bind("change",function() {
            if ($('#mgr_upload_image').get(0).files.length !== 0) {
                console.log("Files here.");
                $("#mgr_upload_button").show();
            }
            else {
                $("#mgr_upload_button").hide();
            }
        });

        $('#mgr_upload_button').click(function() {
            // submit spot
            Spot.submit_spot();
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
                //$("#extended_food_template").show();
                //$("#extended_study_template").hide();
                $("#study_radio").prop('checked', false);
            }
            else if($(this).val() == 'tech') {
                //$("#extended_food_template").hide();
                //$("#extended_study_template").hide();
                $("#study_radio").prop('checked', false);
            }
        });

        // handle radio lick event for study type
        $("#study_radio").click(function(e){
            //$("#extended_food_template").hide();
            //$("#extended_study_template").show();
            $("#add_new_extended_info input[name='extended_info:app_type']").prop('checked', false);
        });

        // handle radio button change for item category
        $("#item_category input[name='category']").change(function(e){
            // hide all subcategory forms
            $(".subcategory").hide();
            // show only subcategory form that corresponds to clicked category
            $("#category_" + $(this).val()).show();
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

    toggle_item_active: function() {

        $("#toggle_item_active").click(function() {
            var checkBoxes = $("input[name='extended_info:i_is_active']");
            checkBoxes.prop("checked", !checkBoxes.prop("checked"));

            // submit "save changes"
            Item.submit_item();

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

    init_validate: function() {

        // page based JS calls
        var page_path = window.location.pathname;

        // ignore query params
        page_path = page_path.split("?")[0];

        // path for spot create form
        var spaces_add_path = new RegExp("\/manager\/spaces\/add\/?$");

        // validate form
        $('#submit_form').validator({'focus': false});
        $('#submit_form').validator('validate');

        Forms.handle_app_type_clicks();
        Forms.handle_checkbox_group_clicks();

        if (spaces_add_path.test(page_path)) {
            console.log("at space add");

            // require app_type prior to create
            Forms.validate_required_app_type();

            // validate if spot can be created
            Forms.validate_create();

        }
        else {

            // custom validators
            Forms.validate_required_app_type();
            Forms.validate_required_checkbox_group();

            // validate if spot can be published (ONLY during spot edit)
            Forms.validate_publish();

        }

        // form validation callback after any validation occurs
        $("#submit_form").on('validated.bs.validator', function (e) {
            Forms.validate_create();
            Forms.validate_publish();
        })

    },

    validate_publish: function() {

        // get number of validation errors on page
        var num_errors = 0;
        num_errors = $('.has-error').length;
        console.log(num_errors);

        // control whether the publish button can be clicked or not
        if (num_errors > 0) {
            console.log("spot cannot be published")

            // for draft, don't allow publish if errors exist
            $(".scout-draft span").html("Note: You have validation errors, but can still save!")

            $(".scout-draft-actions #toggle_is_hidden").attr('disabled', 'disabled');
            $(".scout-draft-actions #toggle_item_active").attr('disabled', 'disabled');
            $(".scout-draft-actions .help-block").css('color', '#a94442');
            $(".scout-draft-actions .help-block").html("Note: Validation errors prevent this spot from being published.");

            // for published, don't allow unpublish or submit if errors exist
            $(".scout-published-actions #toggle_is_hidden").attr('disabled', 'disabled');
            $(".scout-published-actions #toggle_item_active").attr('disabled', 'disabled');
            $(".scout-published-actions .help-block").css('color', '#a94442');
            $(".scout-published-actions .help-block").html("Note: Validation errors prevent this spot from being un-published.");

            $(".scout-published #submit_spot").attr('disabled', 'disabled');
            $(".scout-published #submit_item").attr('disabled', 'disabled');
            $(".scout-published span").addClass("text-danger");
            $(".scout-published span").html("Note: Validation errors prevent any changes from being published.")
        }
        else {
            console.log("spot can be published")

            $(".scout-draft span").html("Note: While in draft, you can save changes regardless of validation errors.")

            $(".scout-draft-actions #toggle_is_hidden").removeAttr("disabled");
            $(".scout-draft-actions #toggle_item_active").removeAttr("disabled");
            $(".scout-draft-actions .help-block").css('color', '');
            $(".scout-draft-actions  .help-block").html("Note: Publishing this space will make it visible in all client apps!");

            $(".scout-published-actions #toggle_is_hidden").removeAttr("disabled");
            $(".scout-published-actions #toggle_item_active").removeAttr("disabled");
            $(".scout-published-actions .help-block").css('color', '');
            $(".scout-published-actions .help-block").html("Note: Unpublishing this space will remove it from being seen in client apps.");

            $(".scout-published #submit_spot").removeAttr("disabled");
            $(".scout-published #submit_item").removeAttr("disabled");
            $(".scout-published span").removeClass("text-danger");
            $(".scout-published span").html("Note: This space is published and any changes will be shown immediately in client apps.")
        }

    },

    validate_create: function() {

        // get number of validation errors on page
        var num_errors = $('.has-error').length;
        console.log(num_errors);

        // control whether the publish button can be clicked or not
        if (num_errors > 0) {
            console.log("spot cannot be created")
            $(".scout-create #submit_spot").attr('disabled', 'disabled');
            $(".scout-create #submit_item").attr('disabled', 'disabled');
            $(".scout-create span").show();
        }
        else {
            console.log("spot can be created")
            $(".scout-create #submit_spot").removeAttr("disabled");
            $(".scout-create #submit_item").removeAttr("disabled");
            $(".scout-create span").hide();
        }

    },

    init_delete_button: function () {
        $("#spot_delete").on("click", function(e) {
            console.log("delete button clicked");
            var spot_id = Forms._get_spot_id();
            var etag = Forms._get_spot_etag();

            // delete the spot, then redirect back to manager home (dashboard)
            Spot.delete_spot(spot_id, etag, function(){document.location.replace("/manager/");});
        });

        $("#item_delete").on("click", function(e) {
            console.log("delete button clicked");
            var item_id = Forms._get_item_id();
            var spot_id = Forms._get_spot_id();
            var etag = Forms._get_spot_etag();

            // delete the item, then redirect back to spot
            Item.delete_item(item_id, etag, function(){document.location.replace("/manager/spaces/" + spot_id);});
        });
    },

    init_building_spot_filter: function () {
        $("#building_select").change(function(e){
            var building = $(e.target).val();
            Forms._filter_spots_by_building(building);
        });
    },

    init_campus_building_filter: function () {
        $("#campus_select").change(function(e){
            var campus = $(e.target).val();
            var pre_selected = $("#building_select>option:selected");
            var selected;
            Forms._filter_buildings_by_campus(campus);
            // Keep current selected on first load
            if(pre_selected.length > 0 && $.contains($("#building_select")[0], pre_selected[0])) {
                selected = pre_selected;
            } else {
                var default_select = $("#building_select>option:disabled");
                selected = default_select;
            }
            $(selected).prop('selected', true);

            // Manually fire event as building filtering doesn't trigger change
            $("#building_select").trigger("change");
        });
    },

    sort_building_list: function () {
        Forms._sort_select($("#building_select"));
    },

    sort_spot_list: function () {
        Forms._sort_select($("#spot_select"));
    },

    _sort_select: function (select) {
        var options = select.find("option");
        var selected = select.val();
        options.sort(function(a, b){
            if (a.text > b.text) return 1;
            if (a.text < b.text) return -1;
            return 0;
        });
        select.empty().append(options);
        select.val(selected);
    },

    _filter_buildings_by_campus: function (campus) {
        Forms._filter_select_by_attribute($("#building_select"), "data-campus", campus);
    },

    _filter_spots_by_building: function (building) {
        Forms._filter_select_by_attribute($("#spot_select"), "data-building", building);
    },

    _filter_select_by_attribute: function (select, attribute, value) {
        var options = select.find("option");

        // store full building list so we can re-filter if campus changes
        if (select.data("optionsHTML") === undefined) {
            select.data("optionsHTML", options);
        }

        $(select).empty();
        $(select.data("optionsHTML")).each(function (idx, option){
            var attr_value = $(option).attr(attribute);
            if (attr_value === value || $(option).prop('disabled')){
                $(select).append(option);
            }
        });
    },

    _get_spot_id: function () {
        if ($('input[name="spot_id"]').length)
            return $('input[name="spot_id"]').attr("value")
        else
            return $('input[name="id"]').attr("value")
    },

    _get_item_id: function () {
        return $('input[name="id"]').attr("value")
    },

    _get_spot_etag: function () {
        return $('input[name="etag"]').attr("value")
    }

};
