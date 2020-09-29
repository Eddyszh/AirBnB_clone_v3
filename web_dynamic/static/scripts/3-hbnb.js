window.onload = function () {
  const amenitiesDict = {};
  $('input:checkbox:checked').each(function () {
    amenitiesDict[$(this).attr('data-id')] = $(this).attr('data-name');
    $('.amenities h4').text(Object.values(amenitiesDict).join(', '));
  });
  $('input:checkbox:unchecked').each(function () {
    delete amenitiesDict[$(this).attr('data-id')];
    if (Object.values(amenitiesDict) === 0) {
      $('.amenitites h4').html("&nbsp;");
    } else {
      $('.amenities h4').text(Object.values(amenitiesDict).join(', '));
    }
  });
  $.get('http://0.0.0.0:5001/api/v1/status/', function (data, status) {
    if (status === "OK") {
      $('#api_status').addClass('available');
    } else {
      $('#api_status').removeClass('available');
    }
  });
  $.ajax({
    type: 'POST',
    url: 'http://0.0.0.0:5001/api/v1/places_search/',
    contentType: 'application/json',
    dataType: 'json',
    data: '{}',
    success: function (data) {
      for (const place of data) {
        $('.places').append('<article><div class="title"><h2>'
                          + place.name
                          + '</h2><div class="price_by_night">$'
                          + place.price_by_night
                          + '</div></div><div class="information"><div class="max_guest"><i class="fa fa-users fa-3x" aria-hidden="true"></i><br />'
                          + place.max_guest
                          + ' Guests'
                          + '</div><div class="number_rooms"><i class="fa fa-bed fa-3x" aria-hidden="true"></i><br />'
                          + place.number_rooms
                          + ' Bedrooms'
                          + '</div><div class="number_bathrooms"><i class="fa fa-bath fa-3x" aria-hidden="true"></i><br />'
                          + place.number_bathrooms
                          + ' Bathrooms'
                          + '</div></div><div class="user"><strong>Owner: '
                          + '</strong></div><div class="description">'
                          + place.description
                          + '</div></article>');
      }
    }
  });
};
