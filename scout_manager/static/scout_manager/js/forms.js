var Forms = {

    init_form: function(){

        Forms.hours_clear();
        Forms.hours_add();
        Forms.image_upload();
        Forms.image_delete();
        Forms.image_check_count();
    },

    // hours functions

    hours_clear: function(){
        // clear hours for a given day
        $(".mgr-clear-hours").click(function(e) {
            $(this).parent().find("input[type=time]").val("");
        });
    },

    hours_add: function(){
        // add hours input fields
        $(".mgr-add-hours").click(function(e) {
            $(this).siblings('.mgr-current-hours').append('added hours <label for="">Open:<input type="time" name="" value="" /></label><label for="">Close:<input type="time" name="" value="" /></label>');
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
                $('#mgr_list_spot_images').append('<li><img src="' + e.target.result +'" style="width:100px;"><label for="" class="scope"><input type="radio" name="" id="" />default</label><input type="button" value="Delete image" class="mgr-delete-image" /></li>');
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
    }

};
