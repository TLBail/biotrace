function readFile(file) {
    const reader = new FileReader();
	const editor = document.getElementById("inputDataContainer");
    const filename = document.getElementById("file-name");
	reader.onload = function(e) {
		editor.getModel().setValue(e.target.result);
		filename.innerText = file.name;

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

function download(name, content) {
	const a = document.createElement('a');
	const file = new Blob([content], {type: 'text/plain'});

	a.href = URL.createObjectURL(file);
	a.download = name;
	a.click();

	URL.revokeObjectURL(a.href);
}

document.getElementById("download-btn").addEventListener("click", () => {
	const text = document.getElementById("outputDataContainer").getModel().getValue();
	const name = document.getElementById("file-name-input").value;
	download(name, text);
})