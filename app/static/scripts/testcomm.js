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
const read_modbus_btn = document.getElementById("read_modbus_btn");


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

        const data = {
            "action": "read",
            "type": cf,
            "address": parseInt(starting_addr),
            "count": parseInt(count),
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
            const log = createLogElement(`Read ${response.type} from ${response.address} and size of ${response.count}: ${response.data}`);
            log_container.insertBefore(log, log_container.firstChild);
        }
        else {
            const log = createLogElement(response.data);
            log_container.insertBefore(log, log_container.firstChild);
        }
    }
});
