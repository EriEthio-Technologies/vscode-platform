// src/vs/workbench/contrib/ai/browser/aiPanel.ts
export class AIPanel extends ViewPane {
	private _chatWidget: AIChatWidget;

	constructor() {
		super(...);
		this._chatWidget = this._register(new AIChatWidget());
		this._chatWidget.onDidGenerateCode(e => this._applyCodeDiff(e));
	}
}


