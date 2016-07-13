var Spot = {
    submit_spot: function (e) {
        var form_data = Spot.get_edit_form_data();
        var is_create= Spot._get_is_add(form_data);

        if (is_create) {
            Spot._create_spot(form_data);

        } else {
            Spot._edit_spot(form_data);
        }


    },

    _get_is_add: function(form_data) {
        return !(form_data.id.length > 0);
    },

    _edit_spot: function (form_data) {
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
                $("#pub_error").html("yay all good!");
            },
            error: function(xhr, status, error) {
                $("#pub_error").removeClass("hidden");
                $("#pub_error").addClass("alert-danger");
                $("#pub_error").html(error + ": " + xhr.responseText);
            }
        });

    },

    _create_spot: function (form_data) {
        var f_data = new FormData();
        f_data.append("json", JSON.stringify(form_data));
        var image = $("#mgr_upload_image")[0];
        var file = image.files[0];
        f_data.append("file", file)
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
                $("#pub_error").html();
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

    init_events: function () {
        // todo: always make sure spot is_hidden=true
        $("#save_unpublished").click(Spot.submit_spot);

        //todo: always remove is_hidden flag
        $("#save_published").click(Spot.submit_spot);
    }
};
