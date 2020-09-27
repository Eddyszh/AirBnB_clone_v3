window.onload = function () {
  const amenities = {}
  $("input:checkbox:checked").each(function () {
    amenities[$(this).attr('data-id')] = $(this).attr('data-name');
  }
  $("input:checkbox:unchecked").each(function () {
    delete amenities[$(this).attr('data-id')];
  }

