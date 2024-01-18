export class Model {
    constructor() {
        this.originalContent = "";
        this.modifiedContent = "";
        this.editorMode = 0;
        this.configs = [];
        this.documentHaveChanged = false;
    }

    async fetchConfigs() {
        const response = await fetch('/api/webdynconfigs', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const configs = await response.json();
        configs.forEach(config => {
            this.configs.push({
                "id": config.id,
                "name": config.name,
                "date": config.date,
                "content": atob(config.content)
            });
        });
        return this.configs;
    }
}