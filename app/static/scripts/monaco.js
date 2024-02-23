class CodeViewMonaco extends HTMLElement {
		_monacoEditor;
		/** @type HTMLElement */
		_editor;

		static get observedAttributes() {
			return ["value", "interactions"];
		}

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

			// Copy over editor styles
			const styles = document.querySelectorAll(
				"link[rel='stylesheet'][data-name^='vs/']"
			);

			for (const style of styles) {
				shadowRoot.appendChild(style.cloneNode(true));
			}

			const template = /** @type HTMLTemplateElement */ (
				document.getElementById("editor-template")
			);
			
			shadowRoot.appendChild(template.content.cloneNode(true));

			const interactions = /** @type HTMLTemplateElement */ (
				document.getElementById("editor-interactions")
			);
				
			this._editor = shadowRoot.querySelector(".editor");
			this._monacoEditor = monaco.editor.create(this._editor, {
				automaticLayout: true,
				language: "ini",

				value: "",
			});
		}

		async saveContent(name) {
			const response = await fetch('/api/webdynconfigs', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					"name": name,
					"content": this._monacoEditor.getValue()
				})
			});

			return await response.json();
		}

		connectedCallback() {
			// Additional setup when the element is connected to the DOM.
			// This might include initializations or other tasks.
			console.log("Editor loaded");
		}

		 attributeChangedCallback(name, oldValue, newValue) {

			switch (name) {
				case "value":
					this.setValue(newValue);
					break;
				case "interactions":
					const interactions = this.shadowRoot.querySelector(".editor-interactions");
					interactions.hidden = !newValue;
					break;
				default:
					break;
			}
		}

		setValue(value) {
			this._monacoEditor.setValue(value);
		}
	}

customElements.define("monaco-editor", CodeViewMonaco);