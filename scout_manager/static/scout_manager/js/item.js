var Item = {
    submit_item: function (e) {
        var form_data = Item.get_edit_form_data();
        var is_create = Item._get_is_add(form_data);

        if (is_create) {
            Item._create_item(form_data);

        } else {
            Item._edit_item(form_data);
        }
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
                $("#pub_error").html("yay all good!");
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
        var image = $("#mgr_upload_image")[0];
        if (image && image.files && image.files[0]) {
            var file = image.files[0];
            f_data.append("file", file)
        }
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

    get_edit_form_data: function() {
        var form = $("form").first();
        var serialized_form = form.serializeObject();
        serialized_form["removed_images"] = window.removed_images;
        return serialized_form;

    },

    _navigate_after_create: function() {
        var spot_select = $("#spot_select");
        var spot_id = spot_select.val();
        window.location.href ="/manager/spaces/" + spot_id;
    }
};
