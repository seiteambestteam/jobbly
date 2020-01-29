$(document).ready(function() {
    let contacts = [];

    console.log("in js");

    $.ajax({
        method: "GET",
        url: "/ajax/get_contacts/",
        success: function(res) {
            contacts = res;
        },
        error: function(res) {
            console.log("error");
        }
    });

    console.log(contacts);

    $("#contacts-search").on("input", function(e) {
        const search = $(this).val();
        const re = new RegExp(search, "i");
        const filteredContacts = contacts.filter(contact =>
            re.test(contact.name)
        );

        const html = filteredContacts.map(contact => {
            return `
            <div class="flex-item">
                <div class="card">
                        <div class="card-title-div">
                            <div class="card-title">
                                <a href="#">${contact.name}</a>
                            </div>
                        </div>
                    <div class="card-content">
                        <p> Application: ${contact.application} </p>
                        <p> Email: ${contact.email} </p>
                        <p> LinkedIn: ${contact.linkedin} </p>
                        <p> Notes: ${contact.notes} </p>
                    </div>
                </div>
            </div>`;
        });

        $("#display-contacts").html("");
        $("#display-contacts").html(html);
    });
});

// MY LUNCH:
// let selectEl = document.getElementById("id_application");
// let j = 0;

// optionsEl = selectEl.children;

// optionsArray = [...optionsEl];

// $.ajax({
//     url: "/ajax/get_applications/",
//     method: "GET",
//     datatype: "json"
// }).done(res => {
//     for (let i = 1; i < optionsArray.length; i++) {
//         optionsArray[i].text = `${res[j].company}`;
//         j++;
//     }
// });
