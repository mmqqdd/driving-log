<script setup>
import { computed, ref } from 'vue'
import { data as days } from './journal.data'

const WEEK = ['一', '二', '三', '四', '五', '六', '日']

const TONE = {
  报名: 'signup',
  听课: 'class',
  刷题: 'quiz',
  练车: 'drive',
  约考: 'book',
  上场: 'exam',
  考试: 'exam',
  科目二VR: 'drive',
  科目二实车: 'drive',
  约科目二: 'book',
}

const list = computed(() => (Array.isArray(days) ? days : []))

const byDate = computed(() => {
  const m = new Map()
  for (const d of list.value) m.set(d.date, d)
  return m
})

const months = computed(() => {
  const s = new Set()
  for (const d of list.value) s.add(d.date.slice(0, 7))
  return [...s].sort()
})

function monthKey(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`
}

const now = new Date()
const todayKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`

// 默认打开这个月；这个月还没记就打开最后一个月有记录的日子
const cursor = ref(
  months.value.includes(todayKey.slice(0, 7)) ? todayKey.slice(0, 7) : (months.value.at(-1) ?? todayKey.slice(0, 7)),
)

const today = computed(() => todayKey)

const label = computed(() => {
  const [y, m] = cursor.value.split('-')
  return `${y} 年 ${Number(m)} 月`
})

const story = computed(() => {
  const entries = list.value
    .filter((d) => d.date.startsWith(cursor.value))
    .map((d) => `${Number(d.date.slice(8))}日${d.doing}${d.when ? ` ${d.when}` : ''}`)
  return entries.length ? entries.join(' · ') : '这个月还没记。'
})

const cells = computed(() => {
  const [ys, ms] = cursor.value.split('-')
  const y = Number(ys)
  const m = Number(ms)
  const first = new Date(y, m - 1, 1)
  const lead = (first.getDay() + 6) % 7
  const lastDate = new Date(y, m, 0).getDate()
  const out = []
  for (let i = 0; i < lead; i++) out.push(null)
  for (let d = 1; d <= lastDate; d++) {
    const key = `${ys}-${ms}-${String(d).padStart(2, '0')}`
    out.push({ n: d, date: key, entry: byDate.value.get(key) ?? null })
  }
  return out
})

// 按自然月翻页：下个月永远可以点（哪怕还没记），上个月最多翻到第一条记录那个月
const canPrev = computed(() => {
  const [y, m] = cursor.value.split('-').map(Number)
  const key = monthKey(new Date(y, m - 2, 1))
  return months.value.length > 0 && key >= months.value[0]
})
const canNext = computed(() => true)

function prev() {
  const [y, m] = cursor.value.split('-').map(Number)
  cursor.value = monthKey(new Date(y, m - 2, 1))
}

function next() {
  const [y, m] = cursor.value.split('-').map(Number)
  cursor.value = monthKey(new Date(y, m, 1))
}

function tone(doing) {
  const name = String(doing || '')
  if (TONE[name]) return TONE[name]
  if (name.includes('考试')) return 'exam'
  if (name.includes('VR') || name.includes('实车')) return 'drive'
  if (name.includes('约')) return 'book'
  return 'other'
}
</script>

<template>
  <div class="cal">
    <div class="cal-bar">
      <button type="button" class="cal-nav" :disabled="!canPrev" @click="prev">上个月</button>
      <p class="cal-month">{{ label }}</p>
      <button type="button" class="cal-nav" :disabled="!canNext" @click="next">下个月</button>
    </div>
    <p v-if="story" class="cal-story">{{ story }}</p>
    <p class="cal-hint">有字的格子是我那天在干的事。点进去看经过。空着就是没记。</p>
    <div class="cal-week">
      <span v-for="w in WEEK" :key="w">{{ w }}</span>
    </div>
    <div class="cal-grid">
      <template v-for="(c, i) in cells" :key="i">
        <span v-if="!c" class="cal-cell empty" />
        <a
          v-else-if="c.entry"
          class="cal-cell on"
          :class="[`tone-${tone(c.entry.doing)}`, { today: c.date === today }]"
          :href="c.entry.url"
        >
          <span class="cal-do">{{ c.entry.doing }}</span>
          <span v-if="c.entry.when" class="cal-when">{{ c.entry.when }}</span>
          <span class="cal-n">{{ c.n }}日</span>
        </a>
        <span v-else class="cal-cell" :class="{ today: c.date === today }">
          <span class="cal-n">{{ c.n }}</span>
        </span>
      </template>
    </div>
  </div>
</template>

<style scoped>
.cal {
  margin: 1.2rem 0 1.8rem;
}
.cal-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.6rem;
  margin-bottom: 0.35rem;
}
.cal-month {
  margin: 0;
  font-weight: 650;
  font-size: 1.05rem;
}
.cal-nav {
  padding: 0.2rem 0.55rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-2);
  font-size: 0.8rem;
  cursor: pointer;
}
.cal-nav:disabled {
  opacity: 0.35;
  cursor: default;
}
.cal-story {
  margin: 0 0 0.25rem;
  font-size: 1.02rem;
  font-weight: 650;
  line-height: 1.45;
}
.cal-hint {
  margin: 0 0 0.8rem;
  color: var(--vp-c-text-2);
  font-size: 0.9rem;
}
.cal-week,
.cal-grid {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  gap: 0.35rem;
}
.cal-week {
  margin-bottom: 0.35rem;
  color: var(--vp-c-text-3);
  font-size: 0.75rem;
  text-align: center;
}
.cal-cell {
  min-height: 4.4rem;
  padding: 0.4rem 0.3rem 0.35rem;
  border-radius: 8px;
  background: var(--vp-c-bg-soft);
  color: inherit;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
}
.cal-cell.empty {
  background: transparent;
  min-height: 0;
}
.cal-cell.today:not(.on) {
  box-shadow: inset 0 0 0 1px var(--vp-c-divider);
}
.cal-cell.on {
  box-shadow: inset 0 0 0 1px color-mix(in srgb, currentColor 22%, transparent);
}
.cal-cell.on:hover {
  filter: brightness(0.98);
}
.cal-do {
  font-size: 0.92rem;
  font-weight: 700;
  line-height: 1.25;
  letter-spacing: 0.02em;
}
.cal-when {
  font-size: 0.72rem;
  font-weight: 650;
  line-height: 1.2;
  opacity: 0.88;
}
.cal-n {
  font-size: 0.72rem;
  color: var(--vp-c-text-3);
  line-height: 1.2;
}
.cal-cell.on .cal-n {
  color: inherit;
  opacity: 0.62;
}
.tone-signup {
  background: color-mix(in srgb, #2f9e73 18%, var(--vp-c-bg-soft));
  color: #1f7a58;
}
.tone-class {
  background: color-mix(in srgb, var(--vp-c-brand-1) 18%, var(--vp-c-bg-soft));
  color: var(--vp-c-brand-1);
}
.tone-quiz {
  background: color-mix(in srgb, #d97706 18%, var(--vp-c-bg-soft));
  color: #b45309;
}
.tone-drive {
  background: color-mix(in srgb, #2563eb 18%, var(--vp-c-bg-soft));
  color: #1d4ed8;
}
.tone-book {
  background: color-mix(in srgb, #7c3aed 18%, var(--vp-c-bg-soft));
  color: #6d28d9;
}
.tone-exam {
  background: color-mix(in srgb, #dc2626 18%, var(--vp-c-bg-soft));
  color: #b91c1c;
}
.tone-other {
  background: color-mix(in srgb, var(--vp-c-brand-1) 16%, var(--vp-c-bg-soft));
  color: var(--vp-c-brand-1);
}
:global(.dark) .tone-signup { color: #4ade80; }
:global(.dark) .tone-quiz { color: #fbbf24; }
:global(.dark) .tone-drive { color: #93c5fd; }
:global(.dark) .tone-book { color: #c4b5fd; }
:global(.dark) .tone-exam { color: #fca5a5; }
@media (max-width: 520px) {
  .cal-cell {
    min-height: 3.7rem;
    padding: 0.28rem 0.18rem;
  }
  .cal-do {
    font-size: 0.82rem;
  }
  .cal-story {
    font-size: 0.95rem;
  }
}
</style>
