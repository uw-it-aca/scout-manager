var Spot = {

    submit_spot: function (e) {
        var form_data = Spot.get_edit_form_data();
        var is_create= Spot._get_is_add(form_data);
        var will_exit = false;
        if (e.data.hasOwnProperty('exit')) {
            will_exit = e.data.exit;
        }

        if (is_create) {
            Spot._create_spot(form_data, will_exit);

        } else {
            Spot._edit_spot(form_data, will_exit);
        }
    },

    submit_spot_continue: function (e) {
        var form_data = Spot.get_edit_form_data();
        var is_create= Spot._get_is_add(form_data);

        if (is_create) {
            Spot._edit_spot(form_data);
        }
    },

    delete_spot: function (spot_id, etag, success_callback) {
        $.ajax({
            url: "/manager/api/spot/" + spot_id,
            type: "DELETE",
            data: etag,
            dataType: "text",
            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            success: function(results) {
                if (typeof success_callback !== "undefined") {
                    success_callback();
                }
            },
            error: function(xhr, status, error) {
            }
        });
    },

    _get_is_add: function(form_data) {
        return !(form_data.id.length > 0);
    },

    _edit_spot: function (form_data, will_exit) {
        var f_data = new FormData();
        f_data.append("json", JSON.stringify(form_data));
        var image = $("#mgr_upload_image")[0];
        var file = image.files[0];
        f_data.append("file", file);
        $.ajax({
            url: "/manager/api/spot/" + form_data.id,
            type: "PUT",
            data: f_data,
            contentType: false,
            processData: false,
            dataType: "json",
            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            success: function(results) {
                $("#pub_error").removeClass("hidden");
                $("#pub_error").addClass("alert-success");
                $("#pub_error").html("All changes have been saved.");

                // reload the page
                Spot._spot_post_submit(will_exit);
            },
            error: function(xhr, status, error) {
                $("#pub_error").removeClass("hidden");
                $("#pub_error").addClass("alert-danger");
                switch (xhr.status) {
                    case 500:
                        $("#pub_error").html("Something went wrong on our end and our developers have been alerted. Please try again later and feel free to contact help@uw.edu.");
                        break;
                    case 403:
                        $("#pub_error").html("Sorry, but you don't have permission to update this page.");
                        break;
                    case 400:
                        $("#pub_error").html("Sorry, there is some bad data in your submission. Please fix it and try again.");
                        break;
                }
            }
        });

    },

    _create_spot: function (form_data, will_exit) {
        var f_data = new FormData();
        f_data.append("json", JSON.stringify(form_data));
        var image = $("#mgr_upload_image")[0];
        if (image && image.files && image.files[0]) {
            var file = image.files[0];
            f_data.append("file", file)
        }
        $.ajax({
            url: "/manager/api/spot/",
            type: "PUT",
            data: f_data,
            contentType: false,
            processData: false,
            dataType: "json",
            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            success: function(results) {
                $("#pub_error").removeClass("hidden");
                $("#pub_error").addClass("alert-success");
                $("#pub_error").html("All changes have been saved.");

                Spot._spot_post_submit(will_exit);
            },
            error: function(xhr, status, error) {
                $("#pub_error").removeClass("hidden");
                $("#pub_error").addClass("alert-danger");

                switch (xhr.status) {
                    case 500:
                        $("#pub_error").html("Something went wrong on our end and our developers have been alerted. Please try again later and feel free to contact help@uw.edu.");
                        break;
                    case 403:
                        $("#pub_error").html("Sorry, but you don't have permission to update this page.");
                        break;
                    case 400:
                        $("#pub_error").html("Sorry, there is some bad data in your submission. Please fix it and try again.");
                        break;
                }
            }
        });
    },

    _spot_post_submit: function (will_exit) {
        if (will_exit) {
            Spot._navigate_to_apptype();
        } else {
            window.location.reload(true);
        }
    },

    get_edit_form_data: function() {
        var form = $("form").first();
        var serialized_form = form.serializeObject();
        serialized_form["available_hours"] = Spot._get_spot_hours();
        serialized_form["removed_images"] = window.removed_images;
        return serialized_form;

    },

    _get_spot_hours: function() {
        var days = $("fieldset.mgr-hours");
        var avalible_hours = {};
        $.each(days, function(idx, day_fieldset){
            var day_name = $(day_fieldset).attr("data-day");
            var hours_blocks = $(day_fieldset).find(".mgr-hours-block");
            avalible_hours[day_name] = [];
            $.each(hours_blocks, function(idx, block){
                var inputs = $(block).find("input");
                var start = $(inputs[0]).val();
                var end = $(inputs[1]).val();
                if(start.length > 0 && end.length > 0){
                    avalible_hours[day_name].push([start, end]);
                }
            });

        });
        return avalible_hours;
    },

    _navigate_to_apptype: function() {
        var type_inputs = $("input[name='extended_info:app_type']");
        var app_type;
        $(type_inputs).each(function (idx, input){
            app_type = $(input).val();
        });
        if (app_type == undefined) {
            app_type = "study";
        }
        window.location.href ="../?app_type=" + app_type;
    }

};
