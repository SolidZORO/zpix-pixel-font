/** @type {import('cz-git').UserConfig} */
module.exports = {
  // commitlint 校验规则：继承 conventional，缺省此字段会导致 `yarn commitlint --edit` 报错
  // "Please add rules to your commitlint.config.js"（commitlint 要求至少有一条 rules）
  // extends: ['@commitlint/config-conventional'],
  rules: {
    // 中文 subject（如 "mock 更新"）无法套用英文大小写规则，关闭 subject 大小写校验
    'subject-case': [0],
  },
  // cz-git 的交互式提问配置（yarn cz / cz 触发）
  prompt: {
    useEmoji: false,
    // 只保留 type + subject，跳过 scope/body/footer/breaking/issue 等多余提问
    // 空 scopes + skipQuestions 可让 `cz` 直接从 type → subject，无 empty/custom 二选一
    scopes: [],
    rules: [],
    allowCustomScopes: false,
    allowEmptyScopes: true,
    skipQuestions: ['scope', 'body', 'footer', 'footerPrefix', 'breaking'],
  },
};
