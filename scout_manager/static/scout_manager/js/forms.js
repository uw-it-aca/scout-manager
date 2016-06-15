var Forms = {

    init_form: function(){

        Forms.hours_clear();
        Forms.hours_add();
        Forms.image_upload();
        Forms.image_delete();
        Forms.image_check_count();
        Forms.toggle_extended_info();
    },

    // hours functions

    hours_clear: function(){
        // clear hours for a given day
        $(".mgr-clear-hours").click(function(e) {
            $(this).parent().siblings().find("input[type=time]").val("");
        });
    },

    hours_add: function(){
        // add hours input fields
        $(".mgr-add-hours").click(function(e) {

            var hours_blocks = $(this).parent().siblings().find('.mgr-hours-block');

            var empty_hours = $(hours_blocks[0]).clone();
            $(empty_hours).find("input").val("");

            $($(this).parent().parent().find('.mgr-current-hours')).append(empty_hours);

        });
    },

    // image handling functions

    image_upload: function(){

        // upload image
        $("#mgr_upload_image").change(function(){
            // add image to list of images list
            Forms.image_add(this);
        });
    },

    image_add: function(input) {

        // read the image from file input and display in preview list
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#mgr_list_spot_images').append('<li class="well"><img src="' + e.target.result +'" style="width:100px;"><label for="" class="scope"><input type="radio" name="" id="" />default</label><input type="button" value="Delete image" class="mgr-delete-image" /></li>');
                Forms.image_check_count();
            }
            reader.readAsDataURL(input.files[0]);
        }
    },

    image_delete: function() {

        // remove image from list to be uploaded
        $('#mgr_list_spot_images').on('click', '.mgr-delete-image', function() {
            $(this).parent("li").remove();
            Forms.image_check_count();
        });
    },

    image_check_count: function() {

        // handle display of empty message
        if( $('#mgr_list_spot_images > li').length < 1 ){
            console.log("empty image list");
            $('#mgr_list_spot_empty').show();
        }
        else {
            $('#mgr_list_spot_empty').hide();
        }
    },

    toggle_extended_info: function() {

        // handle extended_info field for adding new space
        $("#add_new_extended_info input[name='extended_info:app_type']").change(function(e){
            if($(this).val() == 'food') {
                $("#extended_food_template").show();
                $("#extended_study_template").hide();
            }
            else {
                $("#extended_food_template").hide();
                $("#extended_study_template").show();
            }
        });

    },

};
