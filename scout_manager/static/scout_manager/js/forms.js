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
        Forms.init_hours_midnight();
        Forms.capitalize_space_name();
        Forms.init_input_switch();

        $("#campus_select").trigger("change");

        if(form_type === "items") {
            Forms.init_building_spot_filter();
            Forms.sort_spot_list();
            $("#building_select").trigger("change");
        }

        //display labstats fields
        if ($("#has_labstats")[0]) {
            if ($("#has_labstats")[0].checked) {
                $("#labstats-id-group").show();
                $("#labstats-props").hide();
            }

            if ($("#labstats_cloud")[0].checked) {
                $("#labstats-id-group").hide();
                $("#labstats-props").show();
            }

            if ($("#no_labstats")[0].checked) {
                $("#labstats-id-group").hide();
                $("#labstats-props").hide();
            }
        }

        // handle submitting spot to server
        $("#save_continue").on('click', {exit: 'reload'}, Spot.submit_spot);
        $("#save_close").on('click', {exit: 'apptype'}, Spot.submit_spot);
        $("#add_item").on('click', {exit: 'link'}, Spot.submit_spot);
        $("a.item_link").on('click', {exit: 'link'}, Spot.submit_spot);

        $("#submit_item").click(Item.submit_item);

    },

    // Capitalize the first letter of each word (first letter or a letter following a space)
    // But also allow a user to go back and change it to lowercase if wanted
    capitalize_space_name: function() {
        var input = $("#space-name");
        input.on('keypress', function(event) {
            var event = event || window.event;
            var key = event.keyCode || event.which;
            var v = input.val();
            var len = v.length;
            if (key >= 97 && key <= 122 && !event.metaKey) {
                // If our cursor is on the last letter and the prev letter was a space
                // OR this is the first letter OR the user deletes everything
                if (v[len - 1] === " " && (this.selectionStart == len) || v.length == 0) {
                    event.preventDefault();
                    var char = String.fromCharCode(key).toUpperCase();
                    input.val(v + char);
                } else if (this.selectionStart == 0 && this.selectionEnd == len) {
                    // User did a controlA and wants to start over
                    event.preventDefault();
                    var char = String.fromCharCode(key).toUpperCase();
                    input.val(char);
                    // Adding this for Edge (doesn't update correctly)
                    this.selectionStart = 1;
                }
            }
        });
    },

    // hours functions

    hours_clear: function(){
        // clear hours for a given day
        $(".mgr-clear-hours").click(function(e) {
            var hours_inputs = $(this).parent().siblings().find("input[type=time]");
            var hours_block = $(this).parent().siblings().find(".mgr-hours-block");
            // clear hours and remove all but first element
            $(hours_inputs).val("");
            $(hours_block).slice(1).remove();
            $(this).parent().siblings().find(".hours_midnight").prop('checked', false).change();
        });
    },

    hours_add: function(){
        // add hours input fields
        $(".mgr-add-hours").click(function(e) {

            var hours_blocks = $(this).parent().siblings().find('.mgr-hours-block');

            var empty_hours = $(hours_blocks).last().clone();

            var open_input,
                close_input,
                close_midnight;
            $(empty_hours).find("input").each(function(idx, hour_input){
                if($(hour_input).attr('id').indexOf("open") !== -1){
                    open_input = hour_input;
                } else if($(hour_input).attr('id').indexOf("close_midnight") !== -1){
                    close_midnight = hour_input;
                } else if($(hour_input).attr('id').indexOf("close") !== -1){
                    close_input = hour_input;
                }
            });

            var input_id = $(open_input).attr('id').split("_");
            var prev_input_id_int = parseInt(input_id[input_id.length - 1]);
            var input_id_int = prev_input_id_int + 1;
            var input_id_day = input_id[input_id.length - 2];

            $(empty_hours).find("input").val("");

            // Update input IDs
            var open_id = 'open_' + input_id_day + "_" + input_id_int;
            $(open_input).attr('id', open_id);
            var close_id = 'close_' + input_id_day + "_" + input_id_int;
            $(close_input).attr('id', close_id);
            var midnight_id = 'close_midnight_' + input_id_day + "_" + input_id_int;
            $(close_midnight).attr('id', midnight_id);

            // Update corresponding label FORs
            $(empty_hours).find("label[for='open_" + input_id_day + "_" + prev_input_id_int + "']").attr('for', open_id);
            $(empty_hours).find("label[for='close_" + input_id_day + "_" + prev_input_id_int + "']").attr('for', close_id);
            $(empty_hours).find("label[for='close_midnight_" + input_id_day + "_" + prev_input_id_int + "']").attr('for', midnight_id);

            $($(this).parent().parent().find('.mgr-current-hours')).append(empty_hours);
            Forms.init_hours_midnight();

        });
    },

    init_hours_midnight: function () {
        $(".hours_midnight").change(function(e){
            var close_label = $(e.target).parent().parent("div.close-hours").children("label");
            var close_input = $(e.target).parent().parent("div.close-hours").children("input");
            if($(e.target).is(":checked")){
                close_input.val("23:59");
                close_input.prop('disabled', true);
                close_input.addClass("visually-hidden");
                close_label.addClass("visually-hidden");
                close_label.siblings("span").addClass("pull-left");
                close_label.siblings("span").removeClass("pull-right");
                close_label.siblings("span").addClass("midnight-selected");

                } else {
                close_input.val("");
                close_input.prop('disabled', false);
                close_input.removeClass("visually-hidden");
                close_label.removeClass("visually-hidden");
                close_label.siblings("span").addClass("pull-right");
                close_label.siblings("span").removeClass("pull-left");
                close_label.siblings("span").removeClass("midnight-selected");
            }
        });

        // Find spots with close set to 11:59pm and mark as midnight
        var hours_blocks = $(".mgr-hours-block");
        $(hours_blocks).each(function(idx, block){
            var inputs = $(block).find("input[type='time']");
            $(inputs).each(function(idx, input){
                var id = $(input).attr('id');
                if ( id.indexOf('close_') !== -1 ) {
                    var close_time = $(input).val();
                    if (close_time === "23:59"){
                        $(input).parent().find("input:checkbox").prop("checked", true).change();
                    }
                }
            })
        });
    },

    init_input_switch: function() {
        $("#switch_input").click(function(e) {
            if (e.target.value == 'Use Text Inputs') {
                $("#text_input_controls").show();
                $('#category_text_input').val($("input[name='category']:checked").val());
                $('#subcategory_text_input').val($("input[name='subcategory']:checked").val());
                $("#dropdown_controls").hide();
                $("#switch_input").val('Use Selections');
            } else {
                $("#dropdown_controls").show();
                $("#text_input_controls").hide();
                $("#switch_input").val('Use Text Inputs');
            }
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
        $(container).css("background-image" , "url(data:image/png;base64,"+image_data+")");
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

        // remove image from spaces
        $('#mgr_list_spot_images').on('click', '.mgr-delete-image', function() {
            var wrapper_elm = $(this).parent().siblings("div.mgr-edit-img-container").first();
            var image_id = $(wrapper_elm).attr("data-id");
            var image_etag = $(wrapper_elm).attr("data-etag");

            if(window.removed_images !== undefined){
                window.removed_images.push({id: image_id,
                                           etag: image_etag});
            } else {
                window.removed_images = [{id: image_id,
                                          etag: image_etag}];
            }
            Forms.image_check_count();

            // reload spot after image delete
            Spot.submit_spot({'data':{'exit': false}});

        });

        // remove item image
        $('#mgr_list_item_images').on('click', '.mgr-delete-image', function() {
            var wrapper_elm = $(this).parent().siblings("div.mgr-edit-img-container").first();
            var image_id = $(wrapper_elm).attr("data-id");
            var image_etag = $(wrapper_elm).attr("data-etag");

            if(window.removed_images !== undefined){
                window.removed_images.push({id: image_id,
                                           etag: image_etag});
            } else {
                window.removed_images = [{id: image_id,
                                          etag: image_etag}];
            }
            Forms.image_check_count();

            Item.submit_item();

        });
    },

    image_upload: function() {

        $('#mgr_upload_image').on("change", function() {
            if ($('#mgr_upload_image').get(0).files.length !== 0) {
                $("#mgr_upload_button").show();
            }
            else {
                $("#mgr_upload_button").hide();
            }
        });

        $('#mgr_upload_button').click(function() {
            if ($(this).val() == "upload-item-image") {
                Item.submit_item();
            }
            else {
                // submit spot
                Spot.submit_spot({'data': {'exit': false}});
            }
        });

    },

    image_check_count: function() {

        // handle display of empty message
        if( $('#mgr_list_spot_images > div').length < 1 ){
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
            //Spot.submit_spot();
            Spot.submit_spot({'data':{'exit': false}});

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

    validate_required_radio_group: function() {

        // get the count of all checkboxes for a given grouping
        $(".radio-group.required input[type='radio']").each(function() {

            // get the checkbox groupings id
            var group_id = $(this).closest(".well").attr('id');
            // get count of checkboxes checked for given grouping
            var count_checked = $("#"+group_id+" [type='radio']:checked").length;

            // if more than 1 checked, remove error css
            if(count_checked > 0) {
                $(this).closest(".radio-group").removeClass("has-error");
            }
            else {
                $(this).closest(".radio-group").addClass("has-error")
            }

        });
    },

    handle_category_change: function() {
        // Get all category dropdowns for every row currently in the batch form
        let categorySelects = document.getElementsByClassName("category_dropdown");
        // Set an onchange listener for all the dropdowns that populates the subcategory dropdown
        Array.prototype.filter.call(categorySelects, function(categorySelect){
            categorySelect.addEventListener('change', function() {
                let rowNum = $(this).attr("data-row-key");
                // hide all subcategory groups for this row
                $(".subcategory_dropdown_" + rowNum).val('');
                $(".subcategory_group_" + rowNum).hide();
                // show only subcategory group that corresponds to clicked category
                $(".category_" + $(this).val() + "_" + rowNum).show();
                Forms.validate_batch();
            });
        });
    },

    handle_submit_item_batch: function() {
        $("#submit_item_batch").click(Item.submit_item_batch);
    },

    handle_delete_item_row: function() {
        $(".remove-row-btn").click(function(e) {
            $(this).parent().parent().remove();
            Forms.validate_batch();
            $("#submit_form :input").on('input', function (e) {
                Forms.validate_batch();
            });
        });
    },

    handle_item_row_add: function() {
        $("#item_row_add").click(function(e) {
            Forms.handle_add_row(this, 1);
        });
    },

    handle_multi_item_row_add: function() {
        $("#item_row_add_x").click(function(e) {
            let count = $("#add_row_num").val();
            Forms.handle_add_row(this, count);
        });
    },

    handle_add_row: function(context, count) {
        for (let step = 0; step < count; step++) {
            let newRow = Forms.add_row_to_batch_form();
            $(context).parent().parent().parent().append(newRow);
        }
        Forms.handle_delete_item_row();
        Forms.validate_batch();
        Forms.handle_category_change();
        $("#submit_form :input").on('input', function (e) {
            Forms.validate_batch();
        });
    },

    add_row_to_batch_form: function() {
        window.batchRows++;
        let newRow = $(".item-entry-row").first().clone();
        newRow.removeAttr('id');
        let newCategories = newRow.find("#category_select");
        newCategories.attr("data-row-key", window.batchRows);
        let newSelect = newRow.find("#subcategory_select");
        newSelect.addClass("subcategory_dropdown_" + window.batchRows);
        let newOptGroups = newSelect.find("optgroup");
        newOptGroups.each(function() {
            let classes = $(this).attr("class");
            $(this).removeClass(classes);
            $(this).addClass("subcategory_group_" + window.batchRows);
            $(this).addClass(classes + window.batchRows);
            $(this).css("display", "none");
        });
        newRow.show();
        return newRow;
    },

    handle_checkbox_group_clicks: function() {
        // handle clicks for any checkboxes in a "checkbox-group" grouping
        $(".checkbox-group.required input[type='checkbox']").change(function(e) {
            Forms.validate_required_checkbox_group();
        });

    },

    handle_radio_group_clicks: function() {
        // handle clicks for any checkboxes in a "checkbox-group" grouping
        $(".radio-group.required input[type='radio']").change(function(e) {
            Forms.validate_required_radio_group();
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
        Forms.handle_radio_group_clicks();

        //only need to listen for labstats data changes if form has labstats data
        //not using jquery selector because it's truthy even if the object isn't found
        if (document.getElementById("has_labstats")) {
            Forms.handle_labstats_change();
        }

        if (spaces_add_path.test(page_path)) {
            // require app_type prior to create
            Forms.validate_required_app_type();
            // validate if spot can be created
            Forms.validate_create();

        }
        else {
            // custom validators
            Forms.validate_required_app_type();
            Forms.validate_required_checkbox_group();
            Forms.validate_required_radio_group();

            //validate labstats data only if it exists
            if (document.getElementById("has_labstats")) {
                Forms.validate_labstats();
            }
            // validate if spot can be published (ONLY during spot edit)
            Forms.validate_group();
            Forms.validate_publish();

        }

        // form validation callback after any validation occurs
        $("#submit_form").on('validated.bs.validator', function (e) {
            Forms.validate_group();
            Forms.validate_create();
            Forms.validate_publish();
            Forms.validate_either();
        })

    },

    validate_either: function() {
        var hours_blocks = $("div.mgr-hours-block");
        $(hours_blocks).each(function(idx, block){
            var is_valid = Forms._validate_hours(block);
            if (! is_valid) {
                $(block).css("color", "red");
-               $(block).children().children("input").css("background-color", "lightyellow");
            } else {
                $(block).css("color", "");
-               $(block).children().children("input").css("background-color", "");
            }
        });
    },

    _validate_hours: function(block) {
        var inputs = $(block).find("input[type='time']");
        var open = $(inputs[0]);
        var close = $(inputs[1]);
        var m_open = moment(open.val(), "hh:mm");
        var m_close = moment(close.val(), "hh:mm");

        // valid if both blank
        if (open.val().length === 0 && close.val().length === 0){
            return true;
        }
        else if (open.val().length === 0 || close.val().length === 0){
            // invalid if one blank
            return false;
        }
        else if (m_close.isBefore(m_open)){
            // invalid if close before open
            return false;
        }
        return true
    },

    validate_batch: function() {
        var serialized_form = Item.get_batch_form_data();
        $("#submit_item_batch").prop("disabled", false);
        if (serialized_form["name"].length < 1) {
            $("#submit_item_batch").prop("disabled", true);
        }
        for (var i = 1; i < serialized_form["name"].length; i++) {
            if (serialized_form["name"][i] === "" ||
                serialized_form["category"][i] === "" ||
                serialized_form["subcategory"][i] === "" ||
                serialized_form["extended_info:i_brand"][i] === "" ||
                serialized_form["extended_info:i_description"][i] === "") {
                $("#submit_item_batch").prop("disabled", true);
            }
        }
    },

    validate_publish: function() {

        // get number of validation errors on page
        var num_errors = 0;
        num_errors = $('.has-error').length;

        // control whether the publish button can be clicked or not
        if (num_errors > 0) {

            // for draft, don't allow publish if errors exist
            $(".scout-draft-actions #toggle_is_hidden").prop("disabled", true);
            $(".scout-draft-actions #toggle_item_active").prop("disabled", true);
            $(".scout-draft-actions .help-block").css('color', '#a94442');
            $(".scout-draft-actions .help-block").attr('role', 'alert');
            $(".scout-draft-actions .help-block").html("Error: Form validation errors prevent this spot from being published.");

            $(".scout-draft-actions .item-help-block").css('color', '#a94442');
            $(".scout-draft-actions .item-help-block").attr('role', 'alert');
            $(".scout-draft-actions .item-help-block").html("Error: Form validation errors prevent this item from being published.");

            // for published, don't allow unpublish or submit if errors exist
            $(".scout-published-actions #toggle_is_hidden").prop("disabled", true);
            $(".scout-published-actions #toggle_item_active").prop("disabled", true);
            $(".scout-published-actions .help-block").attr('role', 'alert');
            $(".scout-published-actions .help-block").css('color', '#a94442');
            $(".scout-published-actions .help-block").html("Error: Form validation errors prevent this spot from being un-published.");

            $(".scout-published-actions .item-help-block").attr('role', 'alert');
            $(".scout-published-actions .item-help-block").css('color', '#a94442');
            $(".scout-published-actions .item-help-block").html("Error: Form validation errors prevent this item from being un-published.");

            $(".scout-published #submit_spot").prop("disabled", true);
            $(".scout-published #submit_item").prop("disabled", true);
            $(".scout-published #save_continue").prop("disabled", true);

            $(".scout-published span").attr('role', 'alert');
            $(".scout-published span").addClass("text-danger");
            $(".scout-published span").html("Error: Form validation errors prevent any changes from being published.")
        }
        else {

            $(".scout-draft-actions #toggle_is_hidden").prop("disabled", false);
            $(".scout-draft-actions #toggle_item_active").prop("disabled", false);
            $(".scout-draft-actions .help-block").css('color', '');
            $(".scout-draft-actions  .help-block").html("Note: Publishing this space will make it visible in all client apps!");

            $(".scout-draft-actions .item-help-block").css('color', '');
            $(".scout-draft-actions .item-help-block").html("Note: Publishing this item will make it visible in all client apps!");

            $(".scout-published-actions #toggle_is_hidden").prop("disabled", false);
            $(".scout-published-actions #toggle_item_active").prop("disabled", false);
            $(".scout-published-actions .help-block").css('color', '');
            $(".scout-published-actions .help-block").html("Note: Unpublishing this space will remove it from being seen in client apps.");
            $(".scout-published-actions .item-help-block").css('color', '');
            $(".scout-published-actions .item-help-block").html("Note: Unpublishing this item will remove it from being seen in client apps.");

            $(".scout-published #submit_spot").prop("disabled", false);
            $(".scout-published #submit_item").prop("disabled", false);
            $(".scout-published #save_continue").prop("disabled", false);

            $(".scout-published span.item-help").removeClass("text-danger");
            $(".scout-published span.item-help").html("Note: This item is published and any changes will be shown immediately in client apps.")
            $(".scout-published span").removeClass("text-danger");
            $(".scout-published span").html("Note: This space is published and any changes will be shown immediately in client apps.")

        }

    },

    validate_create: function() {

        // get number of validation errors on page
        var num_errors = $('.has-error').length;

        // control whether the save draft or continue buttons can be clicked or not
        if (num_errors > 0) {
            $(".scout-create span").show();

             // save draft button disabled
            $(".scout-create #submit_spot").prop("disabled", true);
            $(".scout-create #submit_item").prop("disabled", true);
            // continue button disabled
            $(".scout-create-continue #submit_spot_continue").prop("disabled", true);
            $(".scout-create-continue #submit_item_continue").prop("disabled", true);

            // save & close, save & continue buttons
            $(".scout-create #save_close").prop("disabled", true);
            $(".scout-create #save_continue").prop("disabled", true);

        }
        else {

            $(".scout-create span").hide();

            // save draft button enabled
            $(".scout-create #submit_spot").prop("disabled", false);
            $(".scout-create #submit_item").prop("disabled", false);
            // continue button enabled
            $(".scout-create-continue #submit_spot_continue").prop("disabled", false);
            $(".scout-create-continue #submit_item_continue").prop("disabled", false);

            // save & close, save & continue buttons
            $(".scout-create #save_close").prop("disabled", false);
            $(".scout-create #save_continue").prop("disabled", false);
        }

    },

    validate_labstats: function() {
        //labstats 5
        if ($("#has_labstats")[0].checked) {
            //make sure customer id, label, and page id are not filed in
            $("#labstats_customer_id")[0].value = "";
            $("#labstats_label")[0].value = "";
            $("#labstats_page_id")[0].value = "";

            //make sure the labstats id is filled out
            if ($("#labstats_id")[0].value.length <= 0) {
                $("#labstats-id-group").addClass("has-error");
            }
            else {
                //check if id is an integer
                var value = $("#labstats_id")[0].value;
                if ("" + parseInt(value,10) == value) {
                    $("#labstats-id-group").removeClass("has-error");
                }
                else {
                    $("#labstats-id-group").addClass("has-error");
                }
            }
        }

        //labstats cloud
        if ($("#labstats_cloud")[0].checked) {
            //make sure customer id, label, and page id are filed in
            if (
                $("#labstats_customer_id")[0].value.length <= 0 ||
                $("#labstats_label")[0].value.length <= 0 ||
                $("#labstats_page_id")[0].value.length <= 0
            ) {
                $("#labstats-props").addClass("has-error");
            } else {
                $("#labstats-props").removeClass("has-error");
            }

            //make sure the labstats id is not filled out
            $("#labstats_id")[0].value = "";
        }

        // N/A
        if ($("#no_labstats")[0].checked) {
            //make sure customer id, label, and page id are not filed in
            $("#labstats_customer_id")[0].value = "";
            $("#labstats_label")[0].value = "";
            $("#labstats_page_id")[0].value = "";

            //make sure the labstats id is not filled out
            $("#labstats_id")[0].value = "";
        }

        Forms.validate_publish();
        Forms.validate_create();
    },

    handle_labstats_change: function(){
        //validate changes to labstats info
        $("#labstats-type").change(Forms.validate_labstats);
        $("#labstats_id").keyup(Forms.validate_labstats);
        $("#labstats_customer_id").keyup(Forms.validate_labstats);
        $("#labstats_label").keyup(Forms.validate_labstats);
        $("#labstats_page_id").keyup(Forms.validate_labstats);

        // handle radio click events for labstats
        $("#has_labstats").click(function(e){
            // only submit labstats_id
            $("#labstats-id-group").show();
            $("#labstats-props").hide();
        });

        $("#labstats_cloud").click(function(e){
            // only submit cloud fields
            $("#labstats-id-group").hide();
            $("#labstats-props").show();
        });

        $("#no_labstats").click(function(e){
            // make sure labstats fields are empty
            $("#labstats-id-group").hide();
            $("#labstats-props").hide();
        });

    },

    validate_group: function() {

        // check to see if the owner field has a validation error
        var num_errors = $('.has-error #owner').length;

        // control whether the save draft or continue buttons can be clicked or not
        if (num_errors > 0) {
            $(".scout-draft #save_close").prop("disabled", true);
            $(".scout-draft #save_continue").prop("disabled", true);
            $(".scout-published #save_close").prop("disabled", true);
            $(".scout-published #save_continue").prop("disabled", true);

        }
        else {
            $(".scout-draft #save_close").prop("disabled", false);
            $(".scout-draft #save_continue").prop("disabled", false);
            $(".scout-published #save_close").prop("disabled", false);
            $(".scout-published #save_continue").prop("disabled", false);
        }
    },

    init_delete_button: function () {
        $("#spot_delete").on("click", function(e) {
            var spot_id = Forms._get_spot_id();
            var etag = Forms._get_spot_etag();

            // delete the spot, then redirect back to manager home (dashboard)
            Spot.delete_spot(spot_id, etag, function(){document.location.replace("/manager/");});
        });

        $("#item_delete").on("click", function(e) {
            var item_id = Forms._get_item_id();
            var spot_id = Forms._get_spot_id();

            // delete the item, then redirect back to spot
            Item.delete_item(item_id, spot_id, function(){document.location.replace("/manager/spaces/" + spot_id);});
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
            Maps.set_campus_center(campus);
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
        // Move default, disabled option to top of list
        var default_opt = $(select).find(":disabled");
        default_opt.detach();
        select.prepend(default_opt);

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
