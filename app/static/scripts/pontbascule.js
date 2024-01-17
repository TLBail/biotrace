//text editors 
const inputExemple = `
{
    "tonne": 12,
    "date": 123421552,
    "coordX": 22.234121,
    "coordY": 32.124141
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
        value: inputExemple,
        readOnly: true,
        language: 'json',
        automaticLayout: true
    });


});

//node graph editor
var graph = new LGraph();
var canvas = new LGraphCanvas("#litegraph-canvas", graph);

function InputPontBascule() { }
InputPontBascule.title = "Input Pont Bascule Data";
InputPontBascule.prototype.onExecute = function () {
    //try to parse the input data
    try {
        const input = JSON.parse(inputEditor.getValue());
        // iterate over the keys of the object
        let i = 0;
        for (const key in input) {
            if (input.hasOwnProperty(key)) {
                const element = input[key];
                //set the value of the output
                this.setOutputData(i, element);
                i++;
            }
        }
    } catch (error) {
        console.log(error);
    }

}
LiteGraph.registerNodeType("pontbascule/input", InputPontBascule);
var inputDataNode = LiteGraph.createNode("pontbascule/input");
inputDataNode.pos = [200, 200];
graph.add(inputDataNode);


function updateNodeInputGraph() {
    if (!inputEditor) return;
    try {
        const input = JSON.parse(inputEditor.getValue());

        // iterate over the keys of the object
        for (const key in input) {
            if (input.hasOwnProperty(key)) {
                const element = input[key];
                console.log(key, typeof element);

                //if the output already exist i.e outputs[i].name == key
                if (!inputDataNode.outputs || !inputDataNode.outputs.find(output => output.name == key)) {
                    inputDataNode.addOutput(key, typeof element);
                    console.log("add output", key, typeof element);
                }
            }
        }

        //remove the output that are not in the input
        for (var i = inputDataNode.outputs.length - 1; i >= 0; i--) {
            var output = inputDataNode.outputs[i];
            if (!input[output.name]) {
                inputDataNode.removeOutput(i);
            }
        }


    } catch (error) {
        console.log(error);
    }

}

function OutputPontBascule() {
    this.addInput("poid", "number");
    this.addInput("timestamp", "number");
    this.addInput("X", "number");
    this.addInput("Y", "number");
}
OutputPontBascule.title = "Output Pont Bascule Data";
//trigger event when the input data of outputDataNode change
OutputPontBascule.prototype.onExecute = function () {
    var poid = this.getInputData(0);
    var timestamp = this.getInputData(1);
    var X = this.getInputData(2);
    var Y = this.getInputData(3);

    try {
        const string = JSON.stringify({
            poid: poid,
            timestamp: timestamp,
            X: X,
            Y: Y
        }, null, 2);
        outputEditor.setValue(string);

    } catch (error) {
        console.log(error);

    }
}
LiteGraph.registerNodeType("pontbascule/output", OutputPontBascule);
var outputDataNode = LiteGraph.createNode("pontbascule/output");
outputDataNode.pos = [500, 200];
graph.add(outputDataNode);




graph.start()


