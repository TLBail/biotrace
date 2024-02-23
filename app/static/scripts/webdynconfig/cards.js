const configCards = document.querySelectorAll('.config');

configCards.forEach(config => {
	config.addEventListener('click', () => {
		const editor = document.getElementsByTagName('monaco-editor')[0];
		const id = parseInt(config.getAttribute('data-id'));
		const conf = window.configs.filter(config => config.id === id)[0];

		editor.setValue(conf.content);

		configCards.forEach(card => {
			card.classList.remove('active');
		});
		
		config.classList.add('active');
	});
});