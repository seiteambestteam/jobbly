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
        const search = $(this).val();
        const re = new RegExp(search, "i");
        const filteredContacts = contacts
            .filter(contact => re.test(contact.name))
            .sort((a, b) => a.name.localeCompare(b.name));

        console.log(filteredContacts);
        const html = filteredContacts.map(contact => {
            let newHtml = `
                <div class="col-sm-6 col-md-4">
                    <div class="card contacts-card m-3">
                        <div class="card-title">
                            <a href="{% url 'contacts_delete' contact.id%}" class="ml-2"><i class="far fa-times-circle"></i></a>
                            <h5 class="txt-bold txt-center pt-3">${contact.name}</h5>
                        </div>
                        <div class="card-content pl-3 pr-3">`;
            if (contact.application) {
                newHtml += `<h6 class="txt-medium d-inline">Application:</h6>
                            <span>${contact.application}</span>
                            <br>`;
            }
            if (contact.email) {
                newHtml += `<h6 class="txt-medium d-inline">Email:</h6>
                            <span>${contact.email}</span>
                            <br>`;
            }
            if (contact.phone_number) {
                newHtml += `<h6 class="txt-medium d-inline">Phone:</h6>
                            <span>${contact.phone_number}</span>
                            <br>`;
            }
            if (contact.linkedin) {
                newHtml += `<h6 class="txt-medium"><a href='${contact.linkedin}'>LinkedIn</a></h6>
                            <br>`;
            }
            if (contact.notes) {
                newHtml += `<h6 class="txt-medium d-inline">Notes:</h6>
                            <span>${contact.notes}</span>`;
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
