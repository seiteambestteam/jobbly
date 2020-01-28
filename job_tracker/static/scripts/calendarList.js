$(document).ready(function() {
    // Fetch our events
    var calendarEl = document.getElementById('calendar');
    let events = [];
    $.ajax({
      url: "/ajax/get_calendar/",
      method: "GET",
      datatype: "json",
      
    }).done(function(response) {
        let calendar = new FullCalendar.Calendar(calendarEl, {
            events: response,
            plugins: [ 'list' ],
            defaultView: 'listWeek',
            height: 'parent'
        });
        calendar.render();
    });
  });