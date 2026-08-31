/* eslint-disable import-x/no-dynamic-require */
const path = require('path');

const pkg = require(path.resolve(__dirname, '../../package.json'));
const name = (pkg && pkg.name) || 'NA';

console.log(name);
return name;
