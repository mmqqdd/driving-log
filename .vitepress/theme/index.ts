import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import Quiz from './Quiz.vue'
import Exam from './Exam.vue'
import Practice from './Practice.vue'
import JournalCalendar from './JournalCalendar.vue'
import HomePage from './HomePage.vue'
import PdfViewer from './PdfViewer.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('Quiz', Quiz)
    app.component('Exam', Exam)
    app.component('Practice', Practice)
    app.component('JournalCalendar', JournalCalendar)
    app.component('HomePage', HomePage)
    app.component('PdfViewer', PdfViewer)
  },
} satisfies Theme
