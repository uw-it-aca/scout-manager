var List = {

    init: function () {
        List.init_delete();
    },

    init_delete: function () {
        $("button.btn-delete").on("click", function(e) {
            var row = $(e.target).closest("tr");
            var spot_id = $(row).attr('data-spotid');
            var etag = $(row).attr('data-etag');
            Spot.delete_spot(spot_id, etag, function(){document.location.reload(true);});

        });

    }

};
