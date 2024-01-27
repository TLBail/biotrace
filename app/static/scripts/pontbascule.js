//text editors 
const inputExemple = `{
    "elements":[
        {
            "tonne": 12,
            "date": 123421552,
            "coordX": 22.234121,
            "coordY": 32.124141
        },
        {
            "tonne": 12,
            "date": 123421552,
            "coordX": 22.234121,
            "coordY": 32.124141
        },
        {
            "tonne": 12,
            "date": 123421552,
            "coordX": 22.234121,
            "coordY": 32.124141
        }
    ]
}`;
const inputDataContainer = document.getElementById('inputDataContainer');
const outputDataContainer = document.getElementById('outputDataContainer');
require.config({ paths: { vs: '/static/vs' } });
var inputEditor;
var outputEditor;
require(['vs/editor/editor.main'], () => {
    inputEditor = monaco.editor.create(inputDataContainer, {
        value: inputExemple,
        language: 'json',
        automaticLayout: true
    });
    inputEditor.onDidChangeModelContent(updateNodeInputGraph);
    updateNodeInputGraph();

    outputEditor = monaco.editor.create(outputDataContainer, {
        value: "[]",
        readOnly: true,
        language: 'json',
        automaticLayout: true
    });


});

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
InputPontBascule.title = "Input Pont Bascule Data";
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
inputDataNode.pos = [300, 200];
graph.add(inputDataNode);

var constString = LiteGraph.createNode("basic/string");
constString.pos = [0, 100];
graph.add(constString);

var jsonParser = LiteGraph.createNode("basic/jsonparse");
jsonParser.pos = [50, 250];
graph.add(jsonParser);


var objectPropertyNode = LiteGraph.createNode("basic/object_property");
objectPropertyNode.pos = [100, 400];
graph.add(objectPropertyNode);


//connect const string with json parser input
constString.connect(0, jsonParser, 1);
//connect json parser with object property node
jsonParser.connect(1, objectPropertyNode, 0);
//connect object property with input data node
objectPropertyNode.connect(0, inputDataNode, 0);



//output
function updateNodeInputGraph() {
    if (!inputEditor) return;
    constString.setValue(inputEditor.getValue());
    //parse with a delay
    setTimeout(() => {
        jsonParser.parse();
    }, 100);

}

function OutputPontBascule() {
    this.array = [];
    this.addInput("element Index", "number")
    this.addInput("poid", "number");
    this.addInput("timestamp", "number");
    this.addInput("X", "number");
    this.addInput("Y", "number");
}
OutputPontBascule.title = "Output Pont Bascule Data";
//trigger event when the input data of outputDataNode change
OutputPontBascule.prototype.onExecute = function () {
    let index = this.getInputData(0);
    let poid = this.getInputData(1);
    let timestamp = this.getInputData(2);
    let X = this.getInputData(3);
    let Y = this.getInputData(4);


    try {
        if (index == 0) {
            const string = JSON.stringify(this.array, null, 2);
            outputEditor.setValue(string);
            this.array = [];
        }


        let object = {};
        if (poid) {
            object.poid = poid;
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
outputDataNode.pos = [800, 200];
graph.add(outputDataNode);

//connect output data node with input data node
inputDataNode.connect(0, outputDataNode, 0);




graph.start()


