import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import Quiz from './Quiz.vue'
import Exam from './Exam.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('Quiz', Quiz)
    app.component('Exam', Exam)
  },
} satisfies Theme
