const cardContainer = document.querySelector('.card-container');
let configCards = document.querySelectorAll('.config');
const editor = document.querySelector("monaco-editor");


editor.addEventListener('save', (event) => {
	const config = event.detail.config;

	if(window.configs <= 0) {
		const emptyText = cardContainer.querySelector('p');
		cardContainer.removeChild(emptyText);
	}


	window.configs.push(config);
	addConfigCard(config);
});

function addConfigCard(config) {
	const template = document.querySelector('#card-template');
	const newCard = template.content.cloneNode(true);

	const card = newCard.querySelector('.card');
	const title = newCard.querySelector('.card-title');
	const body = newCard.querySelector('.card-text');

	card.setAttribute('data-id', config.id);
	title.innerText = config.name,
	body.innerText = `${config.createdAt} (${config.updatedAt})`;

	cardContainer.insertBefore(newCard, cardContainer.firstChild);
	update();
	card.classList.add('active');
}


function update(){
	configCards = document.querySelectorAll('.config');

	configCards.forEach(card => {
		card.classList.remove('active');
	});

	configCards.forEach(card => {
		card.addEventListener('click', () => {
			const id = parseInt(card.getAttribute('data-id'));
			const conf = window.configs.filter(config => config.id === id)[0];

			editor.setValue(conf.content);

			configCards.forEach(card => {
				card.classList.remove('active');
			});
			card.classList.add('active');
		});
	});
}

update();