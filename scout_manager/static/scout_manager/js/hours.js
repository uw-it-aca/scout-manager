var Hours = {

    init_hours: function(){

        Hours.clear_hours();
        Hours.add_hours();
    },

    clear_hours: function(){
        // clear hours for a given day
        $(".mgr-clear-hours").click(function(e) {
            $(this).parent().find("input[type=time]").val("");
        });
    },

    add_hours: function(){
        $(".mgr-add-hours").click(function(e) {
            alert("add hours for this day!");
        });
    },

};
