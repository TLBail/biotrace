import { io } from "https://cdn.socket.io/4.7.2/socket.io.esm.min.js";

const socket = io();

// Connection form
const ip_input = document.getElementById("ip_input");
const port_input = document.getElementById("port_input");
const connect_btn = document.getElementById("connect_btn");
const log_container = document.getElementById("logs-content");

// Modbus form
const starting_addr_input = document.getElementById("starting_addr_input");
const cf_selection = document.getElementById("cf_selection");
const count_input = document.getElementById("count_input");
const type_selection = document.getElementById("type_selection");
const read_modbus_btn = document.getElementById("read_modbus_btn");
const modbus_table = document.getElementById("modbus_table");


function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds} `;
}

function createLogElement(data) {
    let wrapper = document.createElement("div");
    wrapper.classList.add("log");

    let date = document.createElement("span");
    date.innerHTML = formatDate(new Date());

    let content = document.createElement("span");
    content.innerHTML = data;

    wrapper.appendChild(date);
    wrapper.appendChild(content);

    return wrapper;
}

function createRowElement(addr, count, type, read, value) {
    let row = document.createElement("tr");

    let addr_col = document.createElement("th");
    addr_col.scope = "row";
    addr_col.innerHTML = addr;

    let count_col = document.createElement("td");
    count_col.innerHTML = count;

    let type_col = document.createElement("td");
    type_col.innerHTML = type;

    let read_col = document.createElement("td");
    read_col.innerHTML = read;

    let value_col = document.createElement("td");
    value_col.innerHTML = value;

    row.appendChild(addr_col);
    row.appendChild(count_col);
    row.appendChild(type_col);
    row.appendChild(read_col);
    row.appendChild(value_col);

    return row;
}

connect_btn.addEventListener("click", () => {

    const ip = ip_input.value;
    const port = port_input.value;

    if (connect_btn.innerHTML == "Connect") {
        const data = {
            "action": "connect",
            "ip": ip,
            "port": port,
        }
        socket.emit('modbus', JSON.stringify(data))
    } else {
        const data = {
            "action": "disconnect",
        }
        socket.emit('modbus', JSON.stringify(data))
    }
});


read_modbus_btn.addEventListener("click", () => {
    const starting_addr = starting_addr_input.value;
    const cf = cf_selection.value;
    const count = count_input.value;
    const type = type_selection.value;

    const data = {
        "action": "read",
        "type": cf,
        "address": parseInt(starting_addr),
        "count": parseInt(count),
        "value_type": type,
        "invert": false
    }
    socket.emit('modbus', JSON.stringify(data))
});

socket.on('modbus', (msg) => {
    const response = JSON.parse(msg);
    console.log(response);

    if (response.action == "connect") {
        const log = createLogElement(response.data);
        log_container.insertBefore(log, log_container.firstChild);
        if (response.status) {
            connect_btn.innerHTML = "Disconnect";
        }
    }
    if (response.action == "disconnect") {
        const log = createLogElement(response.data);
        log_container.insertBefore(log, log_container.firstChild);
        if (response.status) {
            connect_btn.innerHTML = "Connect";
        }
    }
    if (response.action == "read") {
        if (response.status) {
            const row = createRowElement(response.address, response.count, response.value_type, response.type, response.data);
            modbus_table.insertBefore(row, modbus_table.firstChild);
            const log = createLogElement(`Read ${response.type} from ${response.address} and size of ${response.count}: ${response.data}`);
            log_container.insertBefore(log, log_container.firstChild);
        }
        else {
            const log = createLogElement(response.data);
            log_container.insertBefore(log, log_container.firstChild);
        }
    }
});


// Fonction pour sauvegarder les données
function sauvegarderDonnees() {
    localStorage.setItem('ip_input', ip_input.value);
    localStorage.setItem('port_input', port_input.value);
    localStorage.setItem('starting_addr_input', starting_addr_input.value);
    localStorage.setItem('count_input', count_input.value);
}

// Fonction pour charger les données
function chargerDonnees() {
    if (localStorage.getItem('ip_input')) {
        ip_input.value = localStorage.getItem('ip_input');
    }
    if (localStorage.getItem('port_input')) {
        port_input.value = localStorage.getItem('port_input');
    }
    if (localStorage.getItem('starting_addr_input')) {
        starting_addr_input.value = localStorage.getItem('starting_addr_input');
    }
    if (localStorage.getItem('count_input')) {
        count_input.value = localStorage.getItem('count_input');
    }
}

// Appeler chargerDonnees lors du chargement de la page
window.onload = chargerDonnees;
ip_input.onblur = sauvegarderDonnees;
port_input.onblur = sauvegarderDonnees;
starting_addr_input.onblur = sauvegarderDonnees;
count_input.onblur = sauvegarderDonnees;
