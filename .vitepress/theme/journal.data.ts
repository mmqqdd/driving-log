import { createContentLoader } from 'vitepress'

export interface JournalDay {
  url: string
  date: string
  title: string
  doing: string
  when: string
  items: string[]
}

function ymd(url: string, value: unknown): string {
  const fromUrl = url.match(/\d{4}-\d{2}-\d{2}/)?.[0]
  if (fromUrl) return fromUrl
  if (value instanceof Date && !Number.isNaN(value.getTime())) {
    const y = value.getUTCFullYear()
    const m = String(value.getUTCMonth() + 1).padStart(2, '0')
    const d = String(value.getUTCDate()).padStart(2, '0')
    return `${y}-${m}-${d}`
  }
  return String(value ?? '').match(/\d{4}-\d{2}-\d{2}/)?.[0] ?? ''
}

export default createContentLoader('journal/*.md', {
  transform(raw): JournalDay[] {
    return raw
      .filter((p) => /\/journal\/\d{4}-\d{2}-\d{2}/.test(p.url))
      .map((p) => {
        const fm = p.frontmatter
        const items = Array.isArray(fm.items) ? fm.items.map(String) : []
        const doing = String(fm.doing || items[0] || '有记')
        return {
          url: p.url.replace(/\.html$/, ''),
          date: ymd(p.url, fm.date),
          title: String(fm.title ?? ''),
          doing,
          when: typeof fm.when === 'string' ? fm.when.trim() : '',
          items,
        }
      })
      .filter((d) => /^\d{4}-\d{2}-\d{2}$/.test(d.date))
      .sort((a, b) => a.date.localeCompare(b.date))
  },
})
