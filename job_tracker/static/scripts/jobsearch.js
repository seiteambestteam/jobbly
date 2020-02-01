//api
$(".search-btn").click(() => {
    const searchTerm = $("#search-term").val();
    const locationTerm = $("#search-location").val();
    const JOBBLY_CSRF_TOKEN = document.getElementById("csrf_token").value;
    const JOBBLY_APPLICATION_LINK = document.getElementById("application_link")
        .value;
    $("#scrapper-loader").append(
        '<i class="fas fa-spinner fa-pulse fa-5x"></i>'
    );
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
                $("#scrapper-loader").empty();
                $("#scrapper-results").empty();
                for (i = 0; i < data.jobs.length; i++) {
                    const card = `<div class='search-result'>
                        <p class="text-center">${data.jobs[i].title} at ${data.jobs[i].company} in ${data.jobs[i].locations}</p>
                        <p class="txt-sml">${data.jobs[i].description}</p>
                        <div class='d-flex justify-content-around'>
                            <button class='btn link-btn'><a href='${data.jobs[i].url}' target="_blank">Job Posting</a></button>
                            <form method='POST' action='${JOBBLY_APPLICATION_LINK}' style='display:inline;'>
                                <input type="hidden" name="csrfmiddlewaretoken" value="${JOBBLY_CSRF_TOKEN}">
                                <input name='jobtitle' type='hidden' value='${data.jobs[i].title}'>
                                <input name='company' type='hidden' value='${data.jobs[i].company}'>
                                <input name='joblisting' type='hidden' value='${data.jobs[i].url}'>
                                <button type='submit' style='display:inline;' class='btn link-btn'>Add Application</button>
                            </form>
                        </div>
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
