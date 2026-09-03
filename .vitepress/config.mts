import { defineConfig, type DefaultTheme } from 'vitepress'
import fs from 'node:fs'
import path from 'node:path'

const root = path.resolve(__dirname, '..')

/** 从 markdown 里取标题：优先 frontmatter 的 title，其次第一个一级标题，最后退回文件名 */
function readTitle(file: string, fallback: string): string {
  const raw = fs.readFileSync(file, 'utf-8')
  const fm = raw.match(/^---\r?\n([\s\S]*?)\r?\n---/)
  const title = fm?.[1].match(/^title:\s*(.+)$/m)?.[1]
  if (title) return title.trim().replace(/^['"]|['"]$/g, '')
  return raw.match(/^#\s+(.+)$/m)?.[1].trim() ?? fallback
}

/**
 * 扫描目录生成侧边栏。日志会持续增长，手写 sidebar 迟早失控，
 * 所以这里按文件系统自动生成，新建一个 .md 就自动出现在导航里。
 */
function autoItems(dir: string, opts: { desc?: boolean; onlyDates?: boolean } = {}): DefaultTheme.SidebarItem[] {
  const abs = path.join(root, dir)
  if (!fs.existsSync(abs)) return []

  const items = fs
    .readdirSync(abs)
    .filter((f) => {
      if (!f.endsWith('.md') || f === 'index.md' || f.startsWith('_')) return false
      if (opts.onlyDates) return /^\d{4}-\d{2}-\d{2}/.test(f)
      return true
    })
    .sort()
    .map((f) => ({
      text: readTitle(path.join(abs, f), f.replace(/\.md$/, '')),
      link: `/${dir}/${f.replace(/\.md$/, '')}`,
    }))

  return opts.desc ? items.reverse() : items
}

/** 目录为空时不生成空分组，否则侧边栏会露出一个空标题 */
function group(
  text: string,
  dir: string,
  opts: { desc?: boolean; onlyDates?: boolean } = {}
): DefaultTheme.SidebarItem[] {
  const items = autoItems(dir, opts)
  return items.length ? [{ text, items }] : []
}

export default defineConfig({
  lang: 'zh-CN',
  title: '我在北京考驾照',
  description: '一个完全没考过的人，从选驾校开始记下的考试记录和攻略',

  srcExclude: ['README.md', 'AGENTS.md', 'node_modules/**', '**/_template.md'],

  cleanUrls: true,
  lastUpdated: true,

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '考试记录', link: '/journal/' },
      { text: '考试攻略', link: '/subjects/' },
    ],

    sidebar: {
      '/subjects/': [
        { text: '考试攻略', items: [{ text: '各科', link: '/subjects/' }, { text: '差点搞错的地方', link: '/system/pits' }] },
        ...group('按科目', 'subjects'),
      ],
      '/system/': [
        {
          text: '考试攻略',
          items: [
            { text: '差点搞错的地方', link: '/system/pits' },
            { text: '驾考档案', link: '/system/profile' },
          ],
        },
      ],
      '/journal/': [
        { text: '考试记录', items: [{ text: '故事', link: '/journal/' }, { text: '从报名到拿证', link: '/journal/process' }] },
        ...group('按日期', 'journal', { desc: true, onlyDates: true }),
      ],
    },

    outline: { level: [2, 3], label: '本页大纲' },
    docFooter: { prev: '上一篇', next: '下一篇' },
    lastUpdatedText: '最后更新',

    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜笔记', buttonAriaLabel: '搜索笔记' },
          modal: {
            displayDetails: '显示详情',
            resetButtonTitle: '清空',
            backButtonTitle: '返回',
            noResultsText: '没有找到相关笔记',
            footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' },
          },
        },
      },
    },

    footer: {
      message: '我在北京考驾照 · 考试记录 / 考试攻略',
      copyright: '© 2026 孟强定',
    },
  },
})
