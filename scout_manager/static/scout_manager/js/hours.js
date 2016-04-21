var Hours = {

    clear_hours: function(){
        // clear hours for a given day
        $(".mgr-clear-hours").click(function(e) {
            $(this).parent().find("input[type=time]").val("");
        });
    },
    
};
