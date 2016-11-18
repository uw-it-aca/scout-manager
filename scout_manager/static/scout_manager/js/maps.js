var Maps = {

    init_picker: function() {
        var mapExists = document.getElementById("gmap_chooser");
        var isMobile = $("body").data("mobile");

        if (mapExists) {

            var spot_lat = $("#space_latitude").attr('value');
            var spot_lng = $("#space_longitude").attr('value');

            var picker = $("#gmap_chooser"),
            map, marker, latlng, zoom, m, original_val,

            setLatLongValue = function(latLng) {
                $("#space_latitude").val(latLng.lat().toFixed(8));
                $("#space_longitude").val(latLng.lng().toFixed(8));
            },

            setMarker = function (latlng) {
                if (marker) {
                    marker.setPosition(latlng);
                } else {
                    marker = new google.maps.Marker({
                        position: latlng,
                        map: map,
                        draggable: true,
                        animation: google.maps.Animation.DROP
                    });

                    google.maps.event.addListener(marker, 'drag', function(e) {
                        setLatLongValue(e.latLng);
                    });
                }

                setLatLongValue(latlng);

            };

            if (picker.length) {

                if (spot_lat && spot_lng) {
                    latlng = new google.maps.LatLng(spot_lat, spot_lng);
                } else {
                    latlng = new google.maps.LatLng(47.653787, -122.307808);
                }

                map = new google.maps.Map(picker.get(0), {
                    mapTypeId: google.maps.MapTypeId.ROADMAP,
                    mapTypeControl: false,
                    panControl: true,
                    zoomControlOptions: true,
                    streetViewControl: false,
                    center: latlng,
                    zoom: 18,
                    scrollwheel: false,
                });

                if (spot_lat && spot_lng) {
                    setMarker(latlng);

                }

                google.maps.event.addListener(map, 'click', function(e) {
                    if (!marker) {
                        setMarker(e.latLng);

                        // set focus on these fields to clear validation
                        $("#space_latitude").focus();
                        $("#space_longitude").focus();
                        $("select[name='location:building_name']").focus();

                        // init validation after lat/lng has been set
                        Forms.init_validate();

                    }
                });
            }
            window.map = map;

        }

    },

    set_campus_center: function (campus) {
        if (window.map!== undefined
            && window.campus_locations !== undefined
            && window.campus_locations[campus] !== undefined){
            var campus_coords = window.campus_locations[campus];
            var latlng = new google.maps.LatLng(campus_coords.latitude,
                campus_coords.longitude);
            window.map.setCenter(latlng);
        }
    }

};
