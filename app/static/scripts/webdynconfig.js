const originalContent = `# This is a comment
[general]
# The name of the webdyn
name = "webdyn"
# The ip address of the webdyn
ip = "
# This is a comment
[general]
# The name of the webdyn
name = "webdyn"
# The ip address of the webdyn
ip = "
# This is a comment
[general]
# The name of the webdyn
name = "webdyn"
# The ip address of the webdyn
ip = "
# This is a comment
[general]
# The name of the webdyn
name = "webdyn"
# The ip address of the webdyn
ip = "
# This is a comment
[general]
# The name of the webdyn
name = "webdyn"
# The ip address of the webdyn
ip = "
# This is a comment
[general]
# The name of the webdyn
name = "webdyn"
# The ip address of the webdyn
ip = "
# This is a comment
[general]
# The name of the webdyn
name = "webdyn"
# The ip address of the webdyn
ip = "
# This is a comment
[general]
# The name of the webdyn
name = "webdyn"
# The ip address of the webdyn
ip = "
# This is a comment
[general]
# The name of the webdyn
name = "webdyn"
# The ip address of the webdyn
ip = "`;


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