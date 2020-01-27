//api
$('.search-btn').click(()=>{
    const searchTerm = $('#search-term').val()
    searchString = searchTerm.replace(/\s+/g, '+').toLowerCase()
    $.ajax({
        url: '/ajax/job_search_api/',
        data: {
            'searchString' : searchString
        },
        dataType: 'json',
        success: function(data) {
            // for (i = 0; i< data.length; i++) {
            //     const card= `<div class='card'>
            //         <span class='job-title'>${data[i].title} at ${data[i].company} in ${data[i].location}</span>
            //         <p>${data[i].description}</p>
            //         <a href='${data[i].job_link}' class='btn'>Learn more!</a>
            //     </div>`
            //     $('#scrapper-results').append(card)
            // }
            console.log(data)

//scraper
$('.search-btn').click(()=>{
    const searchTerm = $('#search-term').val()
    searchString = searchTerm.replace(/\s+/g, '+').toLowerCase()
    const searchUrl = `https://www.simplyhired.ca/search?q=${searchString}`
    $.ajax({
        url: '/ajax/jobsearch/',
        data: {
            'url' : searchUrl
        },
        dataType: 'json',
        success: function(data) {
            for (i = 0; i< data.length; i++) {
                const card= `<div class='card'>
                    <span class='job-title'>${data[i].title} at ${data[i].company} in ${data[i].location}</span>
                    <p>${data[i].description}</p>
                    <a href='${data[i].job_link}' class='btn'>Learn more!</a>
                </div>`
                $('#scrapper-results').append(card)
            }
        },
        error: function(err) {
            console.log(err)
            $('#scrapper-results').append('<p>Error, please try again</p>')
        }
    })
})