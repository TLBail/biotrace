const inputEditor = document.getElementById("inputDataContainer");
const outputEditor = document.getElementById("outputDataContainer");

function attachEvent() {
	if (inputEditor.shadowRoot) {
		console.log("ShadowRoot attached")
		inputEditor.getModel().onDidChangeContent(() => updateNodeInputGraph());
	} else {
		console.log("ShadowRoot not attached, retrying")
		setTimeout(attachEvent, 200); // Retry after a short delay if shadowRoot is not yet available
	}
}

attachEvent();

//node graph editor
var graph = new LGraph();
var canvas = new LGraphCanvas("#litegraph-canvas", graph);

//resize auto canvas
window.onresize = () => canvas.resize();
canvas.resize();

function InputPontBascule() {
    this.InputIndex = 0;
    this.addInput("array", "array");
    this.addOutput("element Index", "number")
}
InputPontBascule.title = "Tableau d'entrée";
InputPontBascule.prototype.onExecute = function () {
    if (this.getInputData(0) == null) return;

    try {
        const array = this.getInputData(0);
        const input = array[this.InputIndex];
        if (this.InputIndex >= array.length) this.InputIndex = 0;
        if (!input) return;

        // iterate over the keys of the object
        for (const key in input) {
            if (input.hasOwnProperty(key)) {
                const element = input[key];
                //if the output already exist i.e outputs[i].name == key
                if (!this.outputs || !this.outputs.find(output => output.name == key)) {
                    this.addOutput(key, typeof element);
                }
            }
        }

        //remove the output that are not in the input
        if (this.outputs) {
            for (let i = this.outputs.length - 1; i >= 1; i--) {
                var output = this.outputs[i];
                if (!input[output.name]) {
                    this.removeOutput(i);
                }
            }
        }

        for (const key in input) {
            //get the output index of key
            let i = this.outputs.findIndex(output => output.name == key);
            this.setOutputData(i, input[key]);
        }
        this.setOutputData(0, this.InputIndex);
        this.InputIndex++;
    } catch (error) {
        console.log(error);
    }
}

LiteGraph.registerNodeType("pontbascule/input", InputPontBascule);
var inputDataNode = LiteGraph.createNode("pontbascule/input");
inputDataNode.pos = [750, 200];
graph.add(inputDataNode);

var constString = LiteGraph.createNode("basic/string");
constString.pos = [50, 250];
constString.title = "Données d'entrée"
graph.add(constString);

var jsonParser = LiteGraph.createNode("basic/jsonparse");
jsonParser.pos = [300, 100];
jsonParser.title = "Parser JSON"
graph.add(jsonParser);

var objectPropertyNode = LiteGraph.createNode("basic/object_property");
objectPropertyNode.pos = [550, 100];
objectPropertyNode.title = "Objet à parser"
graph.add(objectPropertyNode);

//output
function updateNodeInputGraph() {
    if (!inputEditor) return;
	console.log(inputEditor.getValue());
    constString.setValue(inputEditor.getValue());
    //parse with a delay
    setTimeout(() => {
        jsonParser.parse();
    }, 100);

}

function OutputPontBascule() {
    this.array = [];
    this.addInput("element Index", "number")
    this.addInput("poids", "number");
    this.addInput("timestamp", "number");
    this.addInput("X", "number");
    this.addInput("Y", "number");
}
OutputPontBascule.title = "Sortie";
//trigger event when the input data of outputDataNode change
OutputPontBascule.prototype.onExecute = function () {
    let index = this.getInputData(0);
    let poids = this.getInputData(1);
    let timestamp = this.getInputData(2);
    let X = this.getInputData(3);
    let Y = this.getInputData(4);

    try {
        if (index == 0) {
            const string = JSON.stringify(this.array, null, 2);

            outputEditor.getModel().setValue(string);
            this.array = [];
        }

        let object = {};
        if (poids) {
            object.poids = poids;
        }
        if (timestamp) {
            object.timestamp = timestamp;
        }
        if (X) {
            object.X = X;
        }
        if (Y) {
            object.Y = Y;
        }
        this.array.push(object);

    } catch (error) {
        console.log(error);
    }
}
LiteGraph.registerNodeType("pontbascule/output", OutputPontBascule);
var outputDataNode = LiteGraph.createNode("pontbascule/output");
outputDataNode.pos = [1000, 200];
graph.add(outputDataNode);

//connect output data node with input data node
inputDataNode.connect(0, outputDataNode, 0);

function CSVParser() {
    this.array = [];
    this.addInput("csv string", "string")
    this.addOutput("elements array", "array")
}
CSVParser.title = "CSV Parser";

CSVParser.prototype.onExecute = function () {
    let csvString = this.getInputData(0);
    let csvObjet = CSVToArray(csvString).map(row => {
        let object = {};
        for (let i = 0; i < row.length; i++) {
            if (!isNaN(row[i])) {
                object[i] = Number(row[i]);
            } else {
                object[i] = row[i];
            }
        }
        return object;
    });
    this.setOutputData(0, csvObjet);
}
LiteGraph.registerNodeType("pontbascule/csvParser", CSVParser);
var csvParserNode = LiteGraph.createNode("pontbascule/csvParser");
csvParserNode.pos = [300, 400];
graph.add(csvParserNode);

graph.start();