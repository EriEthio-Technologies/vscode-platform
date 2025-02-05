import gulp from 'gulp';
import { exec } from 'node:child_process';

// AI Service Tasks
export const buildAIService = (done) => {
	exec('cd ai-service && docker build -t supercoder-ai .', (err, stdout, stderr) => {
		if (err) return done(err);
		console.log(stdout);
		done();
	});
};

// Packaging Task
export const packageWin32x64 = gulp.series(buildAIService, (done) => {
	// Original VS Code packaging logic
	// Add AI service binaries inclusion
	done();
});

// Default task
export default packageWin32x64;
