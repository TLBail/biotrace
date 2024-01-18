export class View {
    constructor() {
        this.initEditor();
        this.windowResize();

        this.btn_mode = document.getElementById('diffButton');
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