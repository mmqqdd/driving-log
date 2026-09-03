import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import Quiz from './Quiz.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('Quiz', Quiz)
  },
} satisfies Theme
