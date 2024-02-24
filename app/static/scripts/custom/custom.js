import { CodeViewMonaco } from "./monaco.js";
import { InteractionsView } from "./monaco-interactions.js";

customElements.define("monaco-interactions", InteractionsView);
customElements.define("monaco-editor", CodeViewMonaco);
