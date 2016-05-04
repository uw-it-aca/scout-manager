var Spot = {
    submit_spot: function (e) {
        var form_data = Spot.get_edit_form_data();
        console.log(form_data);
        $.ajax({
            url: "/manager/api/spot/" + form_data.id,
            type: "PUT",
            data: JSON.stringify(form_data),
            contentType: "application/json",
            dataType: "json",
            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            success: function(results) {
                console.log('success');
            },
            error: function(xhr, status, error) {
            }
        });
    },

    get_edit_form_data: function() {
        var form = $("form").first();
        return form.serializeObject();

    },

    init_events: function () {
        $("input[value='Publish']").click(Spot.submit_spot);
    }
}