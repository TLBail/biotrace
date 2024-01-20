import { io } from "https://cdn.socket.io/4.7.2/socket.io.esm.min.js";

export class Model {
    constructor(){
        this.socket = io();

        this.isConnected = false;
        this.ip = localStorage.getItem("ip_input") || "";
        this.port = localStorage.getItem("port_input") || "";

        this.starting_addr = "";
        this.count = "";
        this.type = "int";
        this.codeFunction = "holding";
        this.isInvert = false;
        this.isUnsigned = false;

        this.data = [];
        this.logs = [];
    }

    bindSocketEvents(handler){
        this.socket.on("modbus", (data) => {
            handler(JSON.parse(data));
        });
    }

    canConnect(){
        return this.ip.length > 0 && this.port.length > 0;
    }

    canRead(){
        return this.isConnected && this.starting_addr.length > 0 && this.count.length > 0 && this.type.length > 0 && this.codeFunction.length > 0;
    }

    connect(){
        if (!this.isConnected){
            const data = {
                "action": "connect",
                "ip": this.ip,
                "port": this.port
            }
            this.socket.emit("modbus", JSON.stringify(data));
            this._commit();
        }
        else {
            const data = {
                "action": "disconnect"
            }
            this.socket.emit("modbus", JSON.stringify(data));
        }
    }


    read(){
        if (!this.isConnected && !this.canRead) return;

        const data = {
            "action": "read",
            "type": this.codeFunction,
            "address": parseInt(this.starting_addr),
            "count": parseInt(this.count),
            "value_type": this.type,
            "invert": this.isInvert,
            "unsigned": this.isUnsigned
        }

        this.socket.emit("modbus", JSON.stringify(data))

    }

    _commit(){
        localStorage.setItem("ip_input", this.ip);
        localStorage.setItem("port_input", this.port);
    }
}