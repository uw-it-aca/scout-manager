var Maps = {

    init_maps: function(){

        var mapExists = document.getElementById("gmap_chooser");
        var isMobile = $("body").data("mobile");
        var myLatlng, mapOptions;

        if (mapExists) {

            // get spot location from data attributes
            var spot_lat = $("#space_latitude").attr('value');
            var spot_lng = $("#space_longitude").attr('value');

            // center map direction on spot location
            myLatlng = new google.maps.LatLng(spot_lat, spot_lng);

            // set map options based on mobile or desktop
            if (isMobile !== undefined ) {

                mapOptions = {
                    center: myLatlng,
                    zoom: 18,
                    scrollwheel: false,
                    draggable: false,
                    disableDefaultUI: true,
                    zoomControl: false,
                    disableDoubleClickZoom: true

                };

            }
            else {

                mapOptions = {
                    center: myLatlng,
                    zoom: 19,
                };

            }

            var styles = [
                {
                    "featureType": "poi.place_of_worship",
                    "elementType": "all",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {
                    "featureType": "poi.business",
                    "elementType": "labels.icon",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {
                    "featureType": "poi.school",
                    "elementType": "labels",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                }
            ];

            var map = new google.maps.Map(document.getElementById('gmap_chooser'), mapOptions);
            map.setOptions({styles: styles});

            var marker = new google.maps.Marker({
               position: myLatlng,
               map: map,
               title: 'Hello World!'
             });


        }

    },

};
