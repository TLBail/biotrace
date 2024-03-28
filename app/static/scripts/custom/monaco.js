export class CodeViewMonaco extends HTMLElement {
		_monacoEditor;
		/** @type HTMLElement */
		_editor;
		_monacoInteractions;
		_originalValue;
		_modifiedValue;
		_state;

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

			shadowRoot.appendChild(template.content.cloneNode(true));;

			this._state = false;
			this._editor = shadowRoot.querySelector(".editor");
			this._monacoInteractions = shadowRoot.querySelector("monaco-interactions");
			this._monacoEditor = monaco.editor.create(this._editor, {
				automaticLayout: true,
				language: "ini",

				value: "",
			});

			this._monacoEditor.onDidChangeModelContent(this.#handleContentChanged);
			this._monacoInteractions.addEventListener("save", this.#handleSave);
			this._monacoInteractions.addEventListener("diff", this.#handleDiff);
		}

		#showEditor = () => {
			this._monacoEditor.dispose();
			this._monacoEditor = monaco.editor.create(this._editor, {
				automaticLayout: true,
				language: "ini",
				value: this._modifiedValue
			});

			this._monacoEditor.onDidChangeModelContent(this.#handleContentChanged);
		}

		#showDiff = () => {
			const originalModel = monaco.editor.createModel(this._originalValue, "ini");
			const modifiedModel = monaco.editor.createModel(this._modifiedValue, "ini");

			this._monacoEditor.dispose();

			this._monacoEditor = monaco.editor.createDiffEditor(this._editor, {
				automaticLayout: true
			});

			this._monacoEditor.setModel({
				original: originalModel,
				modified: modifiedModel
			});

			this._monacoEditor.onDidUpdateDiff(this.#handleDiffContentChanged);
		}

		#handleContentChanged = () => {
			const interactions = this.shadowRoot.querySelector("monaco-interactions");

			this._modifiedValue =  this._monacoEditor.getValue();

			if(this._modifiedValue !== this._originalValue) {
				interactions.enabledSaveButton(true);
			}
			else {
				interactions.enabledSaveButton(false);
			}
		};

		#handleDiffContentChanged = () => {
			const interactions = this.shadowRoot.querySelector("monaco-interactions");

			this._modifiedValue =  this._monacoEditor.getModifiedEditor().getValue();

			if(this._modifiedValue !== this._originalValue) {
				interactions.enabledSaveButton(true);
			}
			else {
				interactions.enabledSaveButton(false);
			}
		}

		#handleSave = async (event) => {
			try {
				const promise = this.saveContent(this._monacoInteractions.getValue());
				promise.then((response) => {
					if(response.status === "success") {
						this._originalValue = this._monacoEditor.getMod;
						this._monacoInteractions.setValue("");
						this._monacoInteractions.enabledSaveButton(false);
						this.dispatchEvent(new CustomEvent("save", {
							detail: {
								config: response.data
							}
						}));
						this.setValue(response.data.content);
					}
				});
			}
			catch (err) {
				console.error(err);
			}
		};

		#handleDiff = (event) => {
			this._state = event.detail.state;

			if(this._state) { // Diff
				this.#showDiff();
			}
			else { // Editor
				this.#showEditor();
			}
		};

		async saveContent(name) {
			const response = await fetch('/api/webdynconfigs', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					"name": name,
					"content": this._modifiedValue
				})
			});

			return await response.json();
		}

		attributeChangedCallback(name, oldValue, newValue) {

			switch (name) {
				case "value":
					this.setValue(newValue);
					break;
				case "interactions":
					const interactions = this.shadowRoot.querySelector("monaco-interactions");
					interactions.setVisibility(true);
					break;
				default:
					break;
			}
		}

		setValue(value) {
			this._originalValue = value;
			this._modifiedValue = value;
			this.#showEditor();
			this._monacoEditor.setValue(value);
			this._monacoInteractions.init();
		}

		getValue() {
			return this._monacoEditor.getValue();
		}

		getModel() {
			return this._monacoEditor.getModel();
		}

	}

