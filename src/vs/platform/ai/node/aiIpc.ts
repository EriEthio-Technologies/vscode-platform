// src/vs/platform/ai/node/aiIpc.ts
export class AIIPCChannel {
	constructor(private service: AIService) { }

	async call(method: string, args: any[]) {
		switch (method) {
			case 'generateCode':
				return this.service.generate(args[0], args[1]);
		}
	}
}
