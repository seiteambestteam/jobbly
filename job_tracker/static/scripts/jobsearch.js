//api

$(".search-btn").click(() => {
    const searchTerm = $("#search-term").val();
    const locationTerm = $("#search-location").val();
    const JOBBLY_CSRF_TOKEN = document.getElementById('csrf_token').value;
    const JOBBLY_APPLICATION_LINK = document.getElementById('application_link').value;
    $.ajax({
        url: "/ajax/job_search_api/",
        data: {
            searchTerm: searchTerm,
            location: locationTerm
        },
        dataType: "json",
        success: function(data) {
            if (!data.jobs) {
                $("#scrapper-results").append(
                    `<p>No ${searchTerm} positions in ${locationTerm}.</p>`
                );
            } else {
                
                $("#scrapper-results").empty();
                for (i = 0; i < data.jobs.length; i++) {
                    const card = `<div>
                        <p class="txt-center">${data.jobs[i].title} at ${data.jobs[i].company} in ${data.jobs[i].locations}</p>
                        <p class="txt-sml">${data.jobs[i].description}</p>
                        <button class='btn center txt-center'><a href='${data.jobs[i].url}' target="_blank">More!</a></button>
                        <form method='POST' action='${JOBBLY_APPLICATION_LINK}' style='display:inline;'>
                            <input type="hidden" name="csrfmiddlewaretoken" value="${JOBBLY_CSRF_TOKEN}">
                            <input name='jobtitle' type='hidden' value='${data.jobs[i].title}'>
                            <input name='company' type='hidden' value='${data.jobs[i].company}'>
                            <input name='joblisting' type='hidden' value='${data.jobs[i].url}'>
                            <input type='submit' style='display:inline;' value='Add Application' class='btn center txt-center link-btn'>
                        </form>
                    </div>`;
                    $("#scrapper-results").append(card);
                }
            }
        },
        error: function(err) {
            $("#scrapper-results").append("<p>Please try again</p>");
        }
    });
});

//web scraper
// $('.search-btn').click(()=>{
//     const searchTerm = $('#search-term').val()
//     searchString = searchTerm.replace(/\s+/g, '+').toLowerCase()
//     const searchUrl = `https://www.simplyhired.ca/search?q=${searchString}`
//     $.ajax({
//         url: '/ajax/jobsearch/',
//         data: {
//             'url' : searchUrl
//         },
//         dataType: 'json',
//         success: function(data) {
//             for (i = 0; i< data.length; i++) {
//                 const card= `<div class='card'>
//                     <span class='job-title'>${data[i].title} at ${data[i].company} in ${data[i].location}</span>
//                     <p>${data[i].description}</p>
//                     <a href='${data[i].job_link}' class='btn'>Learn more!</a>
//                 </div>`
//                 $('#scrapper-results').append(card)
//             }
//         },
//         error: function(err) {
//             console.log(err)
//             $('#scrapper-results').append('<p>Error, please try again</p>')
//         }
//     })
// })
