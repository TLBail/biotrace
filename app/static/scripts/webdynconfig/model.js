export class Model {
    constructor() {
        this.originalContent = "";
        this.modifiedContent = "";
        this.editorMode = 0;
        this.configs = [];
        this.documentHaveChanged = false;
        this.configName = "";
    }

    async fetchConfigs() {
        const response = await fetch('/api/webdynconfigs', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const configs = await response.json();
        this.configs = [];
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

    async saveConfig(name, content) {
        const response = await fetch('/api/webdynconfigs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "name": name,
                "content": btoa(content)
            })
        });

        const result = await response.json();
    }
}