export class View {
    constructor() {
        this.initEditor();
        this.windowResize();

        this.btn_mode = document.getElementById('diffButton');
        this.save_btn = document.getElementById('saveButton');
        this.save_input = document.getElementById('saveInput');
    }

    initEditor(){
        require.config({ paths: { vs: '/static/vs' } });

        this.editor = monaco.editor.create(document.getElementById('container'), {
            value: "Your content here",
            language: 'shell',
            automaticLayout: true
        });

        this.resizeEditor();
    }

    displayConfigs(configs){
        const sampleCard = document.getElementById('cardConfigScript');
        const configs_container = document.getElementById('configs_container');

        // Remove all cards that are not the sample card
        const cards = configs_container.querySelectorAll('.card');
        cards.forEach(card => {
            if(card.id !== 'cardConfigScript') card.remove();
        });


        configs.forEach(config => {
            const card = sampleCard.cloneNode(true);
            const cardBody = card.querySelector('.card-body');
            cardBody.id = config.id;
            card.id = config.id;
            card.style.display = 'block';

            const cardTitle = card.querySelector('h6');
            cardTitle.innerText = config.name;
            cardTitle.id = config.id;
            const cardDate = card.querySelector('.card-text');
            cardDate.id = config.id;
            cardDate.innerText = config.date;

            configs_container.appendChild(card);
        });
    }

    displaySaveForm(p){
        const saveButton = document.getElementById('save_form');
        saveButton.style.display = p ? 'flex' : 'none';
    }

    enableSaveButton(p){
        this.save_btn.disabled = !p;
    }

    bindConfigClick(handler) {
        const configs = document.getElementById('configs_container');
        configs.addEventListener('click', event => {
            const id = parseInt(event.target.parentElement.id);
            handler(id);
        });
    }

    bindModeClick(handler) {
        this.btn_mode.addEventListener('click', event => {
            handler();
        });
    }

    bindContentChange(handler, editorMode) {
        if(editorMode === 0){
            this.editor.onDidChangeModelContent(() => {
                handler(this.editor.getValue());
            });
        }
        else{
            this.editor.onDidUpdateDiff(() => {
                handler(this.editor.getModel().modified.getValue());
            });
        }
    }

    bindInputSaveChange(handler) {
        this.save_input.addEventListener('input', event => {
            handler(this.save_input.value);
        });
    }

    bindSaveClick(handler) {
        this.save_btn.addEventListener('click', event => {
            handler();
        });
    }

    showEditor(content) {
        this.editor.dispose();

        this.editor = monaco.editor.create(document.getElementById('container'), {
            value: content,
            language: 'shell',
            automaticLayout: true
        });

        this.resizeEditor();

    }

    showDiffEditor(originalContent, modifiedContent) {
        const originalModel = monaco.editor.createModel(originalContent, 'shell');
        const modifiedModel = monaco.editor.createModel(modifiedContent, 'shell');

        this.editor.dispose();

        this.editor = monaco.editor.createDiffEditor(document.getElementById('container'), {
            automaticLayout: true
        });

        this.editor.setModel({
            original: originalModel,
            modified: modifiedModel
        });

        this.resizeEditor();
    }

    setModeButtonText(text) {
        this.btn_mode.innerText = text;
    }

    displayContent(content) {
        this.editor.setValue(content);
        this.resizeEditor();
    }

    windowResize() {
        window.addEventListener('resize', this.resizeEditor);
    }

    resizeEditor() {
        const container = document.getElementById('container');
        container.style.height = (container.parentElement.clientHeight * 0.98) + 'px';
    }
}