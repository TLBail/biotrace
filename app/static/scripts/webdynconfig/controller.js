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
        this.view.bindInputSaveChange(this.handleSaveInputChange);
        this.view.bindSaveClick(this.handleSaveClick);

        this.fetchConfigs();
    }

    handleSaveInputChange = value => {
        this.model.configName = value;
        this.view.enableSaveButton(value.length > 0);
    }

    handleSaveClick = () => {
        this.model.saveConfig(this.model.configName, this.model.modifiedContent).then(e => {
            this.fetchConfigs();

            this.model.configName = "";
            this.view.enableSaveButton(false);
            this.model.documentHaveChanged = false;
            this.view.displaySaveForm(this.model.documentHaveChanged);
        });
    }

    handleContentChange = content => {
        if (this.model.originalContent === content) this.model.documentHaveChanged = false;
        else this.model.documentHaveChanged = true;

        this.model.modifiedContent = content;
        this.view.displaySaveForm(this.model.documentHaveChanged);
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