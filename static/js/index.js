document.addEventListener('DOMContentLoaded', function() {
    var buttonLocation = document.getElementById('button-location');
    if (buttonLocation) {
        buttonLocation.addEventListener('click', function() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    var latitude = "Latitue " + position.coords.latitude;
                    var longitude = ' Longitude ' + position.coords.longitude;
                    document.getElementById('location').value = latitude + ',' + longitude;
                }, function(error) {
                    console.error('Error occurred. Error code: ' + error.code);
                    // Handle errors here
                });
            } else {
                console.error('Geolocation is not supported by this browser.');
            }
        });
    } else {
        console.error('Button location element not found.');
    }

    function toggleQuestionMode() {
        var questionMode = document.getElementById('questionMode').value;
        var singleChoice = document.getElementById('singleChoice');
        var multipleChoice = document.getElementById('multipleChoice');
        var location = document.getElementById('location');

        singleChoice.style.display = 'none';
        multipleChoice.style.display = 'none';

        if (questionMode == '2') {
            singleChoice.style.display = 'block';
        } else if (questionMode == '3') {
            multipleChoice.style.display = 'block';
        }
    }

    toggleQuestionMode();
    document.getElementById('questionMode').addEventListener('change', toggleQuestionMode);
});
