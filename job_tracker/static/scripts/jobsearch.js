$(".search-btn").click(() => {
    const searchTerm = $("#search-term").val();
    searchString = searchTerm.replace(/\s+/g, "+").toLowerCase();
    const searchUrl = `https://www.simplyhired.ca/search?q=${searchString}`;
    $.ajax({
        url: "/ajax/jobsearch/",
        data: {
            url: searchUrl
        },
        dataType: "json",
        success: function(data) {
            for (i = 0; i < data.length; i++) {
                const card = `<div class='card'>
                    <p class=''>${data[i].title} at ${data[i].company} in ${data[i].location}</p>
                    <p class="txt-sml">${data[i].description}</p>
                    <button class='btn btn-md center txt-center'><a href='${data[i].job_link}'>More!</a></button>
                </div>`;
                $("#scrapper-results").append(card);
            }
        },
        error: function(err) {
            console.log(err);
            $("#scrapper-results").append("<p>Error, please try again</p>");
        }
    });
});
