const COLORS = Object.freeze({
	PRIMARY: "primary",
	SECONDARY: "secondary",
	SUCCESS: "success",
	DANGER: "danger",
	WARNING: "warning",
	INFO: "info",
})

function pushToast(color, message) {
	console.log("pushToast", color, message);
	if (!Object.values(COLORS).includes(color)) {
		throw new Error('Invalid color');
	}

	const toastDOM = document.getElementById('toast')

	toastDOM.querySelector('.toast-body').innerText = message;

	toastDOM.setAttribute("class", `toast border text-${color}-emphasis bg-${color}-subtle border-${color}-subtle`);

	const toast = bootstrap.Toast.getOrCreateInstance(toastDOM);
	toast.show();
}