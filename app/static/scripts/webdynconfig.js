const configs_container = document.getElementById('configs_container')

let originalContent = "";

const files = []

require.config({ paths: { vs: '/static/vs' } });
var editor;
var documentHaveChanged = false;
var diffEditor;
require(['vs/editor/editor.main'], showEditor);


function showEditor() {
    editor = monaco.editor.create(document.getElementById('container'), {
        value: originalContent,
        language: 'shell',
        automaticLayout: true
    });
    editor.onDidChangeModelContent(function () {
        if (documentHaveChanged) {
            return;
        }
        documentHaveChanged = true;
        const saveButton = document.getElementById('saveButton');
        saveButton.style.display = 'block';
        saveButton.classList.add('coolAnimButton');
        //remove the animation after 1s
        setTimeout(() => {
            saveButton.classList.remove('coolAnimButton');
        }, 1000);
    });

}

function showDiffEditor() {
    const originalModel = monaco.editor.createModel(originalContent);
    const modifiedModel = monaco.editor.createModel(editor.getValue())
    editor.dispose();
    diffEditor = monaco.editor.createDiffEditor(document.getElementById('container'), {
        automaticLayout: true
    });
    diffEditor.setModel({
        original: originalModel,
        modified: modifiedModel
    });


}

diffButton.addEventListener('click', () => {
    const diffButton = document.getElementById('diffButton');
    if (diffEditor) {
        showEditor();
        diffEditor.dispose();
        diffEditor = null;
        diffButton.innerText = 'Diff';
    } else {
        showDiffEditor();

        editor = null;
        diffButton.innerText = 'Editor';
    }
});


const saveButton = document.getElementById('saveButton');
saveButton.addEventListener('click', () => {
    documentHaveChanged = false;

    var content;
    if (editor) {
        content = editor.getValue();
    } else if (diffEditor) {
        content = diffEditor.getModifiedEditor().getValue();
    } else {
        //throw error
        throw new Error('No editor found');
    }
    console.log(content);

    //fade out the button
    saveButton.classList.add('coolFadeOut');
    //remove the button after 1s
    setTimeout(() => {
        saveButton.style.display = 'none';
        saveButton.classList.remove('coolFadeOut');
    }, 1000);
});


function resize() {
    const container = document.getElementById('container');
    //set height to 80% of parent
    container.style.height = (container.parentElement.clientHeight * 0.8) + 'px';
}

resize();
window.addEventListener('resize', () => {
    resize();
});

function displayContent(id){
    files.forEach(file => {
        if(file.id === id) originalContent = file.content;
    })
    editor.dispose();
    showEditor();
}

function createCard(data){
    let card = document.createElement('div');
    card.className = "card"
    let card_body = document.createElement('div');
    card_body.className = "card-body";
    let name = document.createElement('h6');
    name.className = "card-subtitle mb-2 text-body-secondary";
    let date = document.createElement('p');
    date.className = "card-text";
    let button = document.createElement('a');
    button.className = "card-link";

    card.id = data.id
    name.innerHTML = data.name;
    date.innerHTML = data.date;
    button.innerHTML = "Visionner"

    button.addEventListener('click', () => {
        displayContent(data.id)
    })

    card_body.appendChild(name);
    card_body.appendChild(date);
    card_body.appendChild(button);
    card.appendChild(card_body);

    return card;
}

async function getConfigs() {
    const response = await fetch('/api/webdynconfigs', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const config = await response.json();
    return config;
}

result = getConfigs();

result.then((value) => {
    value.forEach(element => {

        const data = {
            "id": element.id,
            "name": element.name,
            "date": element.date,
            "content": atob(element.content)
        }
        configs_container.appendChild(createCard(data));
        files.push(data);
    });

    originalContent = files[0].content ?? "";
});