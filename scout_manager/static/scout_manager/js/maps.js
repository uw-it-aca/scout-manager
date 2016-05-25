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
            parseLatLongValue = function (s) {
                return s.match(/^([-]?[\d\.]+)\s*,\s*([-]?[\d\.]+)$/);
            },
            setLatLongValue = function(latLng) {
                latlng_input.val([latLng.lat(), latLng.lng()].join(', '));
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
                m = parseLatLongValue(latlng_input.val());
                if (m && m.length) {
                    latlng = new google.maps.LatLng(m[1],m[2]);
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
                    zoom: zoom
                });

                if (m && m.length) {
                    setMarker(latlng);
                }

                google.maps.event.addListener(map, 'click', function(e) {
                    if (!marker) {
                        setMarker(e.latLng);
                    }
                });

                latlng_input.prev().bind('displayed', function () {
                    google.maps.event.trigger(map, 'resize');
                    if (marker) {
                        map.setCenter(marker.getPosition());
                    } else if (navigator.geolocation) {
                        navigator.geolocation.getCurrentPosition(function (position) {
                            centerMarker(new google.maps.LatLng(position.coords.latitude,
                                                                position.coords.longitude));
                        }, function (perr) {
                            map.setCenter(new google.maps.LatLng(47.653787, -122.307808));
                            console.log('problem getting lat/long (' + perr.code + ') ' + perr.message);
                        });
                    } else {
                        map.setCenter(new google.maps.LatLng(47.653787, -122.307808));
                    }
                });

                latlng_input.change(function () {
                    var m = parseLatLongValue($(this).val());

                    if (m && m.length) {
                        centerMarker(new google.maps.LatLng(m[1], m[2]));
                    }
                });

                latlng_input.keypress(function (event) {
                    original_val = $(event.target).val();
                    var x = window.spacescout_admin.isNumberInput(event),
                        y = [32,44,45].indexOf(event.keyCode);

                    if (!(window.spacescout_admin.isNumberInput(event)
                          || [32, 44, 45, 46].indexOf(event.which) >= 0)) {
                        event.preventDefault();
                    }
                });
            }

        }

    },

};
