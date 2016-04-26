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
        // add hours input fields
        $(".mgr-add-hours").click(function(e) {
            $(this).siblings('.mgr-current-hours').append('<label for="">Open:<input type="time" name="" value="" /></label><label for="">Close:<input type="time" name="" value="" /></label>');
        });

    },

};
