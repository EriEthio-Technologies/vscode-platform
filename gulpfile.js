/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
require('./build/gulpfile');

// In gulpfile.js
gulp.task('build-ai-service', done => {
	exec('cd ai-service && docker build -t supercoder-ai .', done);
});

gulp.task('package-win32-x64', ['build-ai-service'], () => {
	// Original VS Code packaging logic
	// + Include AI service binaries
});
