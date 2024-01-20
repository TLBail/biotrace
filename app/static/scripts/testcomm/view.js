export class View {
    constructor(){
        this.ip_input = document.getElementById("ip_input");
        this.port_input = document.getElementById("port_input");
        this.connect_btn = document.getElementById("connect_btn");
        this.log_container = document.getElementById("logs-content");

        this.starting_addr_input = document.getElementById("starting_addr_input");
        this.cf_selection = document.getElementById("cf_selection");
        this.count_input = document.getElementById("count_input");
        this.type_selection = document.getElementById("type_selection");
        this.read_modbus_btn = document.getElementById("read_modbus_btn");
        this.invertByteOrder = document.getElementById("invertByteOrder");
        this.unsigned = document.getElementById("unsigned");
        this.modbus_table = document.getElementById("modbus_table");

    }

    bindIpInput(handler){
        this.ip_input.addEventListener("input", () => {
            handler(this.ip_input.value);
        });
    }

    bindPortInput(handler){
        this.port_input.addEventListener("input", () => {
            handler(this.port_input.value);
        });
    }

    bindStartingAddrInput(handler){
        this.starting_addr_input.addEventListener("input", () => {
            handler(this.starting_addr_input.value);
        });
    }

    bindCountInput(handler){
        this.count_input.addEventListener("input", () => {
            handler(this.count_input.value);
        });
    }

    bindCfSelection(handler){
        this.cf_selection.addEventListener("change", () => {
            handler(this.cf_selection.value);
        });
    }

    bindTypeSelection(handler){
        this.type_selection.addEventListener("change", () => {
            handler(this.type_selection.value);
        });
    }

    bindConnectButton(handler){
        this.connect_btn.addEventListener("click", () => {
            handler();
        });
    }

    bindReadModbusButton(handler){
        this.read_modbus_btn.addEventListener("click", () => {
            handler();
        });
    }

    bindInvertByteOrder(handler){
        this.invertByteOrder.addEventListener("click", () => {
            handler();
        });
    }

    bindUnsigned(handler){
        this.unsigned.addEventListener("click", () => {
            handler();
        });
    }

    addLog(data) {
        this.log_container.insertBefore(this._createLogElement(data), this.log_container.firstChild);
    }

    addRow(addr, count, type, read, value) {
        this.modbus_table.insertBefore(this._createRowElement(addr, count, type, read, value), this.modbus_table.firstChild);
    }

    setConnectButtonState(state) {
        this.connect_btn.disabled = !state;
    }

    setConnectButtonText(state) {
        this.connect_btn.innerHTML = state ? "Disconnect" : "Connect";
    }

    setReadButtonState(state) {
        this.read_modbus_btn.disabled = !state;
    }

    setIpInput(value){
        this.ip_input.value = value;
    }

    setPortInput(value){
        this.port_input.value = value;
    }

    setStartingAddrInput(value){
        this.starting_addr_input.value = value;
    }

    setCountInput(value){
        this.count_input.value = value;
    }

    setTypeInput(value){
        this.type_selection.value = value;
    }

    setCodeFunctionInput(value){
        this.cf_selection.value = value;
    }

    setInvertByteOrder(value){
        this.invertByteOrder.checked = value;
    }

    _formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');

        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds} `;
    }

    _createLogElement(data) {
        let wrapper = document.createElement("div");
        wrapper.classList.add("log");

        let date = document.createElement("span");
        date.innerHTML = this._formatDate(new Date());

        let content = document.createElement("span");
        content.innerHTML = data;

        wrapper.appendChild(date);
        wrapper.appendChild(content);

        return wrapper;
    }

    _createRowElement(addr, count, type, read, value) {
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

}