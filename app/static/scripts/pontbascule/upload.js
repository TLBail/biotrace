function readFile(file) {
    const reader = new FileReader();
	const editor = document.getElementById("inputDataContainer");
    reader.onload = function(e) {
		editor.getModel().setValue(e.target.result);
    };
    reader.readAsText(file);
}

document.getElementById('drop-zone').addEventListener('dragover', function(e) {
    e.preventDefault(); // Annule l'effet par défaut qui n'est pas de permettre le dépôt
    e.stopPropagation();
    e.dataTransfer.dropEffect = 'copy'; // Affiche le curseur approprié
});

document.getElementById('drop-zone').addEventListener('drop', function(e) {
    e.preventDefault();
    e.stopPropagation();

	if (e.dataTransfer.files.length > 1) {
		const toastDOM = document.getElementById('toast')

		toastDOM.querySelector('.toast-body').innerText = "Seulement un fichier peut être téléchargé à la fois. Le premier fichier a été sélectionné.";

		const toast = bootstrap.Toast.getOrCreateInstance(toastDOM);
		toast.show();
    }

	readFile(e.dataTransfer.files[0]);
});

document.getElementById('drop-zone').addEventListener('click', function() {
    document.getElementById('file-input').click();
});

document.getElementById('file-input').addEventListener('change', function(e) {
    const file = e.target.files[0];
    readFile(file);
});