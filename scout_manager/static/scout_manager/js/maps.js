var Maps = {

    init_picker: function() {

        var mapExists = document.getElementById("gmap_chooser");
        var isMobile = $("body").data("mobile");

        if (mapExists) {

            var spot_lat = $("#space_latitude").attr('value');
            var spot_lng = $("#space_longitude").attr('value');

            var latlng_input = $('input[name="location.latitude|location.longitude"]'),
            picker = $("#gmap_chooser"),
            map, marker, latlng, zoom, m, original_val,
            setLatLongValue = function(latLng) {

                //latlng_input.val([latLng.lat(), latLng.lng()].join(', '));

                $("#space_latitude").val(latLng.lat());
                $("#space_longitude").val(latLng.lng());
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
            },
            centerMarker = function (ctr) {
                map.setCenter(ctr);
                setMarker(ctr);
            };

            if (picker.length) {

                if (spot_lat && spot_lng) {
                    latlng = new google.maps.LatLng(spot_lat, spot_lng);
                    zoom = 18;
                } else {
                    latlng = new google.maps.LatLng(47.653787, -122.307808);
                    zoom = 16;
                }

                map = new google.maps.Map(picker.get(0), {
                    mapTypeId: google.maps.MapTypeId.ROADMAP,
                    mapTypeControl: false,
                    panControl: true,
                    zoomControlOptions: true,
                    streetViewControl: false,
                    center: latlng,
                    zoom: zoom,
                    scrollwheel: false,
                });

                if (spot_lat && spot_lng) {
                    setMarker(latlng);
                }

                google.maps.event.addListener(map, 'click', function(e) {
                    if (!marker) {
                        setMarker(e.latLng);
                    }
                });

                // handle keypress and input field changes
                $("#space_latitude").change(function () {
                    console.log("space_latitude changed");
                });

                $("#space_latitude").keypress(function (event) {
                    console.log("space_latitude keypress");
                });

                $("#space_longitude").change(function () {
                    console.log("space_latitude changed");
                });

                $("#space_longitude").keypress(function (event) {
                    console.log("space_latitude keypress");
                });

            }

        }

    },

};
