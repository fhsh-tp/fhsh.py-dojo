import js from '@eslint/js'
import tseslint from 'typescript-eslint'
import pluginVue from 'eslint-plugin-vue'
import prettier from 'eslint-config-prettier'
import globals from 'globals'

// Conservative lint gate: it exists to catch obvious bugs (undefined vars,
// unreachable code, broken Vue templates), NOT to enforce a full style guide or
// clear pre-existing lint debt. Noise-prone rules are downgraded to warnings and
// buffered by `--max-warnings` in the `lint` script. Formatting is owned by
// Prettier (`eslint-config-prettier` disables conflicting stylistic rules).
export default tseslint.config(
  {
    ignores: [
      '**/dist/**',
      '**/node_modules/**',
      'docs/public/**',
      '.vitepress/cache/**',
      'refs/**',
      '**/*.d.ts',
    ],
  },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  ...pluginVue.configs['flat/essential'],
  {
    files: ['**/*.vue'],
    languageOptions: {
      parserOptions: { parser: tseslint.parser },
    },
  },
  {
    languageOptions: {
      globals: { ...globals.browser, ...globals.node },
    },
    rules: {
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/no-unused-vars': [
        'warn',
        { argsIgnorePattern: '^_', varsIgnorePattern: '^_' },
      ],
      'no-empty': ['warn', { allowEmptyCatch: true }],
      // VitePress theme components use framework-convention single-word names
      // (Layout, Content). This is not a bug.
      'vue/multi-word-component-names': 'off',
    },
  },
  {
    // Test files legitimately use mock patterns the base rules flag:
    // `while (true)` polling loops, `this` aliasing in fakes, and dynamic
    // `require()` for module mocking. Do not gate on these in tests.
    files: ['**/*.spec.ts', '**/*.test.ts', '**/__tests__/**'],
    rules: {
      'no-constant-condition': 'off',
      '@typescript-eslint/no-this-alias': 'off',
      '@typescript-eslint/no-require-imports': 'off',
    },
  },
  prettier,
)
