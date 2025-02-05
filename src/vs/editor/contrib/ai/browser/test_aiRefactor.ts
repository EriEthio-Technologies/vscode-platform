import * as assert from 'assert';
import { AIRefactorContribution, refactorCode } from './aiRefactor.js';
import { TextDocument, Range } from 'vscode';

suite('AIRefactorContribution Tests', () => {
    test('should provide code actions', () => {
        const aiRefactor = new AIRefactorContribution();
        const doc = {
            getText: () => 'var a = 1;'
        } as TextDocument;
        const range = {} as Range;
        const actions = aiRefactor.provideCodeActions(doc, range);
        assert.strictEqual(actions.length, 1);
        assert.strictEqual(actions[0].title, 'Optimize with AI');
    });

    test('should refactor code', () => {
        const code = 'var a = 1;';
        const refactoredCode = refactorCode(code);
        assert.strictEqual(refactoredCode, 'let a = 1;');
    });
});
