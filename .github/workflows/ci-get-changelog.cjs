/* eslint-disable prefer-destructuring */
const fs = require('fs');
const path = require('path');

// usage: `node ./.github/workflows/get-tag-changelog.js --tag=0.2.1`

const CHANGELOG_PATH = path.resolve(__dirname, '../../CHANGELOG.md');

let log = '-';
if (!fs.existsSync(CHANGELOG_PATH)) {
  console.log(log);
  return log;
}

// use JSON.stringify keep ALL \n\r enter / newline
const CHANGELOG_TEXT = JSON.stringify(fs.readFileSync(CHANGELOG_PATH, 'utf-8'));

const getTagName = () => {
  let tagName = '';

  const argvs = process.argv.slice(2);
  if (argvs && Array.isArray(argvs)) {
    argvs.forEach((arg) => {
      const kv = `${arg}`.split('=');
      if (kv && kv[1] && kv[0] === '--tag' && kv[1]) tagName = kv[1];
    });
  }

  return tagName;
};

const __VERSION_NUM__ = getTagName();

// Compatible 2 styles
//   - ### 0.0.5 (2022-03-22)
//   - ### [0.0.7](https://URL) (2022-03-22)
const logRegx = new RegExp(
  String.raw`(###?\s\[${__VERSION_NUM__}][\s\S]*?)(###?\s\[?\d{1,3}\.\d{1,3}\.\d{1,3}\]?)`,
  'ig',
);

const logMatchs = logRegx.exec(CHANGELOG_TEXT);
if (logMatchs && logMatchs[1]) log = logMatchs[1];

log = log.replaceAll('\\n', '\n\r');

// this `console.log` is used by CI, dont comment it
console.log(log);

return log;
