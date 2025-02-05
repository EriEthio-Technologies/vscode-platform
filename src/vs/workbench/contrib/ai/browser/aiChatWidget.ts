// src/vs/workbench/contrib/ai/browser/aiChatWidget.ts
getCodeContext() {
	return this.editorService.activeEditor?.getModel()?.getValue() || '';
}
