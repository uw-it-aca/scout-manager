var Spot = {
    submit_spot: function (e) {
        var form_data = Spot.get_edit_form_data();
        var is_create= Spot._get_is_add(form_data);

        if (is_create === false) {
            Spot._edit_spot(form_data);
        } else {
            Spot._create_spot(form_data)
        }


    },

    _get_is_add: function(form_data) {
        if (form_data.id === undefined){
            return true
        }
        return false
    },

    _edit_spot: function (form_data) {

        console.log(form_data);

        $.ajax({
            url: "/manager/api/spot/" + form_data.id,
            type: "PUT",
            data: JSON.stringify(form_data),
            contentType: "application/json",
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

    _create_spot: function (form_data) {
        $.ajax({
            url: "/manager/api/spot/",
            type: "POST",
            data: JSON.stringify(form_data),
            contentType: "application/json",
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
        $("input[value='Save Changes']").click(Spot.submit_spot);
    }
};
