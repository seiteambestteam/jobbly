$(document).ready(function() {
    let selectEl = document.getElementById("id_application");
    let j = 0;

    optionsEl = selectEl.children;

    optionsArray = [...optionsEl];

    $.ajax({
        url: "/ajax/get_applications/",
        method: "GET",
        datatype: "json"
    }).done(res => {
        for (let i = 1; i < optionsArray.length; i++) {
            optionsArray[i].text = `${res[j].company}`;
            j++;
        }
    });
});
