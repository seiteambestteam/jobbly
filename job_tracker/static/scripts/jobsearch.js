//api
$('.search-btn').click(()=>{
    const searchTerm = $('#search-term').val()
    $.ajax({
        url: '/ajax/job_search_api/',
        data: {
            'searchTerm' : searchTerm,
        },
        dataType: 'json',
        success: function(data) {
             for (i = 0; i < data.length; i++) {
                const card = `<div class='card'>
                    <p class=''>${data.jobs[i].title} at ${data.jobs[i].company} in ${data.jobs[i].location}</p>
                    <p class="txt-sml">${data.jobs[i].description}</p>
                    <button class='btn btn-md center txt-center'><a href='${data.jobs[i].url}'>More!</a></button>
                </div>`;
                $("#scrapper-results").append(card);
            }
        },
        error: function(err) {
            $("#scrapper-results").append("<p>Error, please try again</p>");
        }
    })
})
            

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
