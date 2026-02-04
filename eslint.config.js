import markdown from 'eslint-plugin-markdown';

export default [
  {
    files: ['**/*.md'],
    plugins: {
      markdown,
    },
    processor: 'markdown/markdown',
  },
  {
    files: ['**/*.md/**'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
    },
    env: {
      node: true,
      es2022: true,
    },
    rules: {
      'no-console': 'off',
    },
  },
];




