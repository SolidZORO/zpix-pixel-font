const fs = require('fs');
const path = require('path');

module.exports = {
  types: [
    { type: 'feat', section: 'Features' },
    { type: 'fix', section: 'Bug Fixes' },
    { type: 'perf', section: 'Performance' },
    { type: 'refactor', section: 'Refactor' },
    { type: 'docs', hidden: 'Docs' },
    { type: 'style', hidden: 'Style' },
    { type: 'test', hidden: 'Test' },
    { type: 'chore', hidden: true },
  ],
  lifecycle: {
    postbump: (version) => {
      const readmePath = path.resolve(__dirname, './dist/README.md');
      if (fs.existsSync(readmePath)) {
        let content = fs.readFileSync(readmePath, 'utf-8');
        content = content.replace(/\| v\d+\.\d+\.\d+ \|/g, `| v${version} |`);
        fs.writeFileSync(readmePath, content, 'utf-8');
        console.log(`Updated dist/README.md to v${version}`);
      }
    },
  },
};
