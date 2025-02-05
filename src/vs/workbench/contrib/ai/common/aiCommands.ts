// src/vs/workbench/contrib/ai/common/aiCommands.ts
registerCommand('supercoder.generate', async (context: CodeContext) => {
	const prompt = await getActiveEditorPrompt();
	const generated = await aiService.generateCode(prompt, context);
	applyInPlaceDiff(generated);
});
