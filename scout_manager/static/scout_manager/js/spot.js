var Spot = {
    submit_spot: function (e) {
        if(e.target);
    },

    init_events: function () {
        $("input.submit").click(Spot.submit_spot)
    }
}