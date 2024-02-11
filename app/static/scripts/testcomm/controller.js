import { Model } from './model.js';
import { View  } from './view.js';

export class Controller {
    constructor(){
        this.model = new Model();
        this.view = new View();


        this.view.setConnectButtonState(this.model.canConnect());
        this.view.setReadButtonState(this.model.canRead());
        this.view.setIpInput(this.model.ip);
        this.view.setPortInput(this.model.port);
        this.view.setStartingAddrInput(this.model.starting_addr);
        this.view.setTypeInput(this.model.type);
        this.view.setCountInput(this.model.count);
        this.view.setInvertByteOrder(this.model.isInvert);
        this.view.setCodeFunctionInput(this.model.codeFunction);

        this.view.bindIpInput(this.handleIpInput);
        this.view.bindPortInput(this.handlePortInput);
        this.view.bindConnectButton(this.handleConnectButton);

        this.view.bindStartingAddrInput(this.handleStartingAddrInput);
        this.view.bindCountInput(this.handleCountInput);
        this.view.bindCfSelection(this.handleCfSelection);
        this.view.bindTypeSelection(this.handleTypeSelection);
        this.view.bindInvertByteOrder(this.handleInvertByteOrder);
        this.view.bindUnsigned(this.handleUnsigned);
        this.view.bindReadModbusButton(this.handleReadModbusButton);

        this.model.bindSocketEvents(this.handleSocketEvents);
    }

    handleSocketEvents = (data) => {
        switch (data.action){
            case "connect":
                this._handleConnectionResponse(data);
                break;
            case "disconnect":
                this._handleDisconnectResponse(data);
                break;
            case "read":
                this._handleReadResponse(data);
                break;
            default:
                console.log("Unknown action");
        }
    }

    handleIpInput = (ip) => {
        this.model.ip = ip;
        this.view.setConnectButtonState(this.model.canConnect());
        this.view.setReadButtonState(this.model.canRead());
    }

    handlePortInput = (port) => {
        this.model.port = port;
        this.view.setConnectButtonState(this.model.canConnect());
        this.view.setReadButtonState(this.model.canRead());
    }

    handleStartingAddrInput = (starting_addr) => {
        this.model.starting_addr = starting_addr;
        this.view.setReadButtonState(this.model.canRead());
    }

    handleCountInput = (count) => {
        this.model.count = count;
        this.view.setReadButtonState(this.model.canRead());
    }

    handleCfSelection = (cf) => {
        this.model.codeFunction = cf;
        this.view.setReadButtonState(this.model.canRead());
    }

    handleTypeSelection = (type) => {
        this.model.type = type;
        this.view.setReadButtonState(this.model.canRead());
    }

    handleConnectButton = () => {
        this.model.connect();
    }

    handleInvertByteOrder = () => {
        this.model.isInvert = !this.model.isInvert;
    }

    handleUnsigned = () => {
        this.model.isUnsigned = !this.model.isUnsigned;
    }

    handleReadModbusButton = () => {
        this.model.read();
    }

    _handleConnectionResponse = (data) =>{
        this.model.isConnected = data.status;
        this._addLog(data.data);
        this.view.setConnectButtonText(this.model.isConnected);
        this.view.setReadButtonState(this.model.canRead());
    }

    _handleDisconnectResponse = (data) => {
        this.model.isConnected = !data.status;
        this._addLog(data.data);
        this.view.setConnectButtonText(this.model.isConnected);
        this.view.setReadButtonState(this.model.canRead());
    }

    _handleReadResponse = (data) => {
        if(data.status){
            this._addData(data);
            this._addLog(`Read ${data.type} from ${data.address} and size of ${data.count}: ${data.data}`);
        }
        else
            this._addLog(data.data)
    }

    _addLog(data) {
        this.view.addLog(data);
        this.model.logs.push({date: this.view._formatDate(new Date()), data: data});
    }

    _addData(data) {
        this.view.addRow(data.address, data.count, data.value_type, !data.signed, data.invert, data.type, data.data);
        this.model.data.push(data);
    }

}