var Spot = {
    submit_spot: function (e) {
        var form_data = Spot.get_edit_form_data();
        //console.log(form_data)
    },

    get_edit_form_data: function() {
        var form = $("form").first();
        return form.serializeObject();

    },

    init_events: function () {
        $("input[value='Publish']").click(Spot.submit_spot);
    }
}