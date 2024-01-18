import { View } from "./view.js";
import { Model } from "./model.js";

export class Controller {
    constructor() {
        this.model = new Model();
        this.view = new View();

        this.view.displayContent(this.model.originalContent);

        this.view.bindConfigClick(this.handleConfigClick);
        this.view.bindModeClick(this.handleModeClick);
        this.view.bindContentChange(this.handleContentChange, this.model.editorMode);

        this.fetchConfigs();
    }

    handleContentChange = content => {
        if (this.model.originalContent === content) this.model.documentHaveChanged = false;
        else this.model.documentHaveChanged = true;

        this.model.modifiedContent = content;
    }

    handleModeClick = () => {
        if (this.model.editorMode === 0) {
            this.view.showDiffEditor(this.model.originalContent, this.model.modifiedContent);
            this.model.editorMode = 1;
            this.view.bindContentChange(this.handleContentChange, this.model.editorMode);

        } else {
            this.view.showEditor(this.model.modifiedContent);
            this.model.editorMode = 0;
            this.view.bindContentChange(this.handleContentChange, this.model.editorMode);
        }

        this.view.setModeButtonText(this.model.editorMode ? "Editor" : "Diff");
    }

    handleConfigClick = id => {
        this.model.configs.forEach(config => {
            if (config.id === id){
                if(this.model.editorMode === 1) this.handleModeClick();
                this.model.originalContent = config.content;
                this.view.displayContent(config.content);
            }
        });
    }

    fetchConfigs() {
        this.model.fetchConfigs().then(configs => {
            this.model.originalContent = configs[0].content;
            this.view.displayContent(this.model.originalContent);
            this.view.displayConfigs(configs);
        });
    }
}