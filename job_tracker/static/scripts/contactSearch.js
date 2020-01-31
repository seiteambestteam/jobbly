$(document).ready(function() {
    let contacts = [];

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

    $("#contacts-search").on("input", function(e) {
        const CONTACT_DELETE_LINK = document.getElementById("contact_delete")
            .value;
        const CONTACT_UPDATE_LINK = document.getElementById("contact_update")
            .value;
        const search = $(this).val();
        const re = new RegExp(search, "i");
        const filteredContacts = contacts
            .filter(contact => re.test(contact.name))
            .sort((a, b) => a.name.localeCompare(b.name));

        const html = filteredContacts.map(contact => {
            let newHtml = `
                <div class="col-sm-6 col-md-4">
                    <div class="card contacts-card m-3">
                        <div class="card-title">
                            <a href="${CONTACT_DELETE_LINK}" class="ml-2"><i class="far fa-times-circle"></i></a>
                            <a href="${CONTACT_UPDATE_LINK}" class="ml-2">
                            <i class="far fa-edit"></i>
                        </a>
                            <h5 class="txt-bold txt-center pt-3">${contact.name}</h5>
                        </div>
                        <div class="card-content pl-3 pr-3">`;
            if (contact.application) {
                newHtml += `<h6 class="txt-medium d-inline">Application: ${contact.application} at ${contact.company}</h6>
                            <br>`;
            }
            if (contact.email != "None") {
                newHtml += `<h6 class=" txt-medium d-inline"><a href='mailto:${contact.email}'>${contact.email}</a></h6>`;
            }
            if (contact.phone_number) {
                newHtml += `<h6 class="txt-medium d-inline">Phone: ${contact.phone_number}</h6>
                            <br>`;
            }
            if (contact.linkedin != "None") {
                newHtml += `<h6 class="txt-medium"><a href='${contact.linkedin}'>LinkedIn</a></h6>
                            <br>`;
            }
            if (contact.notes) {
                newHtml += `<h6 class="txt-medium d-inline">Notes: ${contact.notes}</h6>`;
            }
            newHtml += `</div>
                    </div>
                </div>
                <br>`;
            return newHtml;
        });

        $("#display-contacts").html("");
        $("#display-contacts").html(html);
    });
});
