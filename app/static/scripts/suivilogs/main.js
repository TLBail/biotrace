let logs = window.logs;
const table = document.querySelector('#table');
let logCards = document.querySelectorAll('.log');

let errors_wrapper = document.querySelector('#errors-content');

logs.forEach(log => {
    log.content.forEach(content => {
        if (content.failed) {
            let error = document.createElement('div');
            error.classList.add('alert', 'alert-danger');
            error.innerHTML = log.name + ": " + content.application;
            error.id = log.id;
            error.addEventListener('click', handleClick);
            errors_wrapper.appendChild(error);
        }
    })
})

function handleClick(event) {
    setTable(parseInt(event.target.id));
    logCards.forEach(card => {
        card.classList.remove('active');

        if (parseInt(card.getAttribute('data-id')) === parseInt(event.target.id)) {
            card.classList.add('active');
            card.scrollIntoView({ behavior: 'smooth', block: 'center' });

        }
    });
}

function setTable(id){

    let content = logs.filter(log => log.id === id)[0].content;

	table.innerHTML = "";
	content.forEach(c => {

		let row = document.createElement("tr");

		let date =  document.createElement("td");
		let application = document.createElement("td");

		date.innerHTML = c.date;
		application.innerHTML = c.application;

		if(c.failed){
			application.style.color = "red";
		}

		row.appendChild(date);
		row.appendChild(application);


		table.appendChild(row);
	});

}