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
            height: 'parent',
            aspectRatio: 4
        });
        calendar.render();
    });
  });


// sample data returned:
//   [
//       {
//           "model": "job_tracker.landmark",
//           "pk": 3,
//           "fields": {
//               "name": "Technical Interview",
//               "datetime": "2020-01-29T18:00:00Z",
//               "location": "",
//               "followup": "2020-02-07T00:00:00Z",
//               "application": 3
//             }},
//         {
//             "model": "job_tracker.landmark",
//             "pk": 2,
//             "fields": {
//                 "name": "Phone Interview",
//                 "datetime": "2020-01-30T12:00:00Z",
//                 "location": "",
//                 "followup": "2020-02-20T12:00:00Z",
//                 "application": 2
//         }}]