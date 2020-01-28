let selectEl = document.getElementById("id_application");

optionsEl = selectEl.children;

optionsArray = [...optionsEl];

console.log(optionsArray);

optionsArray.forEach(item => {
    for (let i = 1; i < optionsArray.length; i++) {
        item[i].text = "";
    }
});
