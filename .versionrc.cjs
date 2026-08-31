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
  bumpFiles: [
    { filename: 'package.json', type: 'json' },
    {
      filename: 'dist/README.md',
      updater: {
        readVersion(contents) {
          const m = contents.match(/\| v([\d.]+) \|/);
          return m ? m[1] : '0.0.0';
        },
        writeVersion(contents, version) {
          return contents.replace(/\| v[\d.]+ \|/g, `| v${version} |`);
        },
      },
    },
  ],
};
