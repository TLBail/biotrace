export class InteractionsView extends HTMLElement {

    constructor() {
        super();

        const shadowRoot = this.attachShadow({ mode: "open" });

        const bootstrapCSS = document.createElement("link");
        bootstrapCSS.setAttribute("rel", "stylesheet");
        bootstrapCSS.setAttribute("href", "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css");
        shadowRoot.appendChild(bootstrapCSS);

        const bootstrapJS = document.createElement("script");
        bootstrapJS.setAttribute("script", "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js");
        shadowRoot.appendChild(bootstrapJS);

        const template = /** @type HTMLTemplateElement */ (
            document.getElementById("interactions-template")
        );


        shadowRoot.appendChild(template.content.cloneNode(true));

        const saveButton = shadowRoot.querySelector("#saveButton");
        const diffButton = shadowRoot.querySelector("#diffButton");

        saveButton.addEventListener("click", () => {
            this.dispatchEvent(new CustomEvent("save"));
        });

        diffButton.addEventListener("click", () => {
            this.dispatchEvent(new CustomEvent("diff"));
        });
    }

    connectedCallback() {
        console.log("Connected");
    }

    setVisibility(visible) {
        const interactions = this.shadowRoot.querySelector(".editor-interactions")
        interactions.hidden = !visible;
    }

    enabledSaveButton(enabled) {
        const saveButton = this.shadowRoot.querySelector("#saveButton");
        saveButton.disabled = !enabled;
    }

    setValue(value) {
        this.shadowRoot.querySelector("#saveInput").value = value;
    }

    getValue() {
        return this.shadowRoot.querySelector("#saveInput").value;
    }
}