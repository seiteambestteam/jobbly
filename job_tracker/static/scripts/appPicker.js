const dateEl = document.getElementById('id_dueDate');
  M.Datepicker.init(dateEl, {
    format: 'yyyy-mm-dd',
    defaultDate: new Date(),
    setDefaultDate: true,
    autoClose: true
  });