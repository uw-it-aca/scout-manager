var Item = {
    submit_item: function (e) {
        var form_data = Item.get_edit_form_data();
        // Use the value of the input that was not hidden during submission
        if ($("#switch_input").val() == 'Use Text Inputs') {
            // Second entry corresponds to dropdown selection
            form_data['category'] = form_data['category'][1]
            form_data['subcategory'] = form_data['subcategory'][1]
            form_data['extended_info:i_brand'] = form_data['extended_info:i_brand'][1]
        } else if ($('#switch_input').val() == 'Use Selections') {
            // First entry corresponds to a text input
            form_data['category'] = form_data['category'][0]
            form_data['subcategory'] = form_data['subcategory'][0]
            form_data['extended_info:i_brand'] = form_data['extended_info:i_brand'][0]
        }
        // Normalize category name format for db storage (lowercase and underscore-seperated)
        form_data['category'] = form_data['category'].replace(/\s+/g, '_').toLowerCase();

        var is_create = Item._get_is_add(form_data);

        if (is_create) {
            Item._create_item(form_data);

        } else {
            Item._edit_item(form_data);
        }
    },

    submit_item_batch: function (e) {
        var form_data = Item.get_batch_form_data();
        var items = [];
        for (var i = 1; i < form_data['name'].length; i++) {
            var entry = {
                'id': '',
                'csrfmiddlewaretoken': form_data['csrfmiddlewaretoken'],
                'spot_id': form_data['spot_id'],
                'etag': form_data['etag'],
                'name': form_data['name'][i],
                'category': form_data['category'][i],
                'subcategory': form_data['subcategory'][i],
                'extended_info:i_brand': form_data['extended_info:i_brand'][i],
                'extended_info:i_description': form_data['extended_info:i_description'][i],
            };
            if (form_data['extended_info:i_is_active'][i] == "yes") {
                entry['extended_info:i_is_active'] = "true"
            }
            items.push(entry);
        }
        Item._create_item_batch(items);
    },

    delete_item: function (item_id, etag, success_callback) {
        $.ajax({
            url: "/manager/api/item/" + item_id,
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
                $("#pub_error").removeClass("hidden");
                $("#pub_error").addClass("alert-danger");
                $("#pub_error").html(error + ": " + xhr.responseText);
                switch (xhr.status) {
                    case 500:
                        $("#pub_error").html("Something went wrong on our end and our developers have been alerted. Please try again later and feel free to contact help@uw.edu.");
                        break;
                    case 403:
                        $("#pub_error").html("Sorry, but you don't have permission to update this page.");
                        break;
                    case 400:
                        $("#pub_error").html("Sorry, your submission contained bad data. Please fix it and try again:<br/><strong>" + xhr.responseText + "</strong>");
                        break;
                }
            }
        });
    },

    _get_is_add: function(form_data) {
        return !(form_data.id.length > 0);
    },

    _edit_item: function (form_data) {
        var f_data = new FormData();
        f_data.append("json", JSON.stringify(form_data));
        var image = $("#mgr_upload_image")[0];
        var file = image.files[0];
        f_data.append("file", file);
        $.ajax({
            url: "/manager/api/item/" + form_data.id,
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
                $("#submit_form").html("");
                window.location.reload(true);
            },
            error: function(xhr, status, error) {
                $("#pub_error").removeClass("hidden");
                $("#pub_error").addClass("alert-danger");
                $("#pub_error").html(error + ": " + xhr.responseText);
            }
        });

    },

    _create_item: function (form_data) {
        var f_data = new FormData();
        f_data.append("json", JSON.stringify(form_data));
        $.ajax({
            url: "/manager/api/item/",
            type: "PUT",
            data: f_data,
            contentType: false,
            processData: false,
            dataType: "json",
            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            success: function(results) {
                $("#pub_error").removeClass("hidden");
                $("#pub_error").addClass("alert-success");
                $("#pub_error").html();
                Item._navigate_after_create();
            },
            error: function(xhr, status, error) {
                $("#pub_error").removeClass("hidden");
                $("#pub_error").addClass("alert-danger");
                $("#pub_error").html(error + ": " + xhr.responseText);
            }
        });
    },

    _create_item_batch: function (item_batch) {
        var form_data = item_batch;;
        var f_data = new FormData();
        f_data.append("json", JSON.stringify(form_data));
        $.ajax({
            url: "/manager/api/item/",
            type: "PUT",
            data: f_data,
            contentType: false,
            processData: false,
            dataType: "json",
            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            success: function(results) {
                $("#pub_error").removeClass("hidden");
                $("#pub_error").addClass("alert-success");
                $("#pub_error").html();
                Item._navigate_after_create();
            },
            error: function(xhr, status, error) {
                $("#pub_error").removeClass("hidden");
                $("#pub_error").addClass("alert-danger");
                $("#pub_error").html(error + ": " + xhr.responseText);
            }
        });
    },

    get_batch_form_data: function() {
        var form = $("form").first();
        var serialized_form = form.serializeObject();
        return serialized_form;
    },

    get_edit_form_data: function() {
        var form = $("form").first();
        var serialized_form = form.serializeObject();
        serialized_form["removed_images"] = window.removed_images;
        return serialized_form;

    },

    _navigate_after_create: function() {
        var spot_select = $("#spot_id_input");
        var spot_id = spot_select.val();
        window.location.href ="/manager/spaces/" + spot_id;
    }
};
