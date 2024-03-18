const cardContainer = document.querySelector('.card-container');
const table = document.querySelector('#table');
let logCards = document.querySelectorAll('.log');


function setTable(content){

	table.innerHTML = "";
	content.forEach(c => {

		console.log(c);

		let row = document.createElement("tr");

		let date =  document.createElement("td");
		let application = document.createElement("td");

		date.innerHTML = c.date;
		application.innerHTML = c.application;

		row.appendChild(date);
		row.appendChild(application);

		table.appendChild(row);
	});

}
function update(){
	logCards = document.querySelectorAll('.log');

	logCards.forEach(card => {
		card.classList.remove('active');
	});

	logCards.forEach(card => {
		card.addEventListener('click', () => {
			const id = parseInt(card.getAttribute('data-id'));
			const log = window.logs.filter(log => log.id === id)[0];

            console.log(log.content);
			setTable(log.content);

			logCards.forEach(card => {
				card.classList.remove('active');
			});
			card.classList.add('active');
		});
	});
}

update();