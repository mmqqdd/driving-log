<script setup>
import { computed, onMounted, ref } from 'vue'

const BANK = '/practice/exam/k1/bank.json'

const SUBJECTS = [
  { id: 'k1', label: '科目一', open: true },
  { id: 'k2', label: '科目二', open: false },
  { id: 'k3', label: '科目三', open: false },
  { id: 'k4', label: '科目四', open: false },
]

const K1_PARTS = [
  { id: 'all', label: '全部' },
  { id: '01', label: '考试须知' },
  { id: '02', label: '违法记分' },
  { id: '03', label: '超速超员' },
  { id: '04', label: '限速停车' },
  { id: '05', label: '标志标线' },
  { id: '06', label: '灯光手势' },
  { id: '07', label: '通行让行' },
  { id: '08', label: '准驾证件' },
  { id: '09', label: '酒驾急救' },
]

const subject = ref('k1')
const chapter = ref('all')
const error = ref('')
const loading = ref(true)
const source = ref('')
const deck = ref([])
const i = ref(0)
const picked = ref(null)
const revealed = ref(false)
const seen = ref(0)
const correct = ref(0)
const loops = ref(0)

const item = computed(() => deck.value[i.value] ?? null)
const subjectOpen = computed(() => SUBJECTS.find((s) => s.id === subject.value)?.open)

function shuffle(list) {
  const a = list.slice()
  for (let k = a.length - 1; k > 0; k--) {
    const j = Math.floor(Math.random() * (k + 1))
    ;[a[k], a[j]] = [a[j], a[k]]
  }
  return a
}

function fromBank(item) {
  return {
    id: item.id,
    q: item.q,
    image: item.image,
    why: item.why || '',
    choices: (item.options || []).map((o) => ({
      key: o.key,
      text: o.text,
      value: o.key,
    })),
    answer: item.answer,
  }
}

function fromChapter(item) {
  if (item.type === 'tf') {
    return {
      id: item.id,
      q: item.q,
      image: item.image,
      why: item.why || '',
      choices: [
        { key: '对', text: '对', value: true },
        { key: '错', text: '错', value: false },
      ],
      answer: item.answer,
    }
  }
  return {
    id: item.id,
    q: item.q,
    image: item.image,
    why: item.why || '',
    choices: (item.options || []).map((text, n) => ({
      key: 'ABCD'[n],
      text,
      value: text,
    })),
    answer: item.answer,
  }
}

function deal(items) {
  deck.value = shuffle(items)
  i.value = 0
  picked.value = null
  revealed.value = false
}

function resetScore() {
  seen.value = 0
  correct.value = 0
  loops.value = 0
  error.value = ''
}

function pickSubject(id) {
  if (subject.value === id) return
  subject.value = id
  chapter.value = 'all'
  resetScore()
  load()
}

function pickChapter(id) {
  if (chapter.value === id) return
  chapter.value = id
  resetScore()
  load()
}

function label(val) {
  const hit = item.value?.choices.find((c) => c.value === val)
  return hit ? (hit.text === hit.key ? hit.key : `${hit.key}. ${hit.text}`) : String(val)
}

function choose(val) {
  if (revealed.value || !item.value) return
  picked.value = val
  revealed.value = true
  seen.value += 1
  if (val === item.value.answer) correct.value += 1
}

function next() {
  picked.value = null
  revealed.value = false
  if (i.value + 1 >= deck.value.length) {
    loops.value += 1
    deal(deck.value)
    return
  }
  i.value += 1
}

async function loadChapters(ids) {
  const packs = await Promise.all(
    ids.map((id) =>
      fetch(`/practice/k1/${id}.json`).then((r) => (r.ok ? r.json() : null))
    )
  )
  const items = []
  for (const pack of packs) {
    if (!pack?.items) continue
    for (const it of pack.items) items.push(fromChapter(it))
  }
  return items
}

async function load() {
  loading.value = true
  deck.value = []
  if (!subjectOpen.value) {
    loading.value = false
    return
  }
  try {
    if (chapter.value === 'all') {
      const bank = await fetch(BANK)
      if (bank.ok) {
        const data = await bank.json()
        if (data.items?.length) {
          source.value = 'bank'
          deal(data.items.map(fromBank))
          loading.value = false
          return
        }
      }
      const items = await loadChapters(K1_PARTS.filter((p) => p.id !== 'all').map((p) => p.id))
      if (!items.length) throw new Error('empty')
      source.value = 'chapters'
      deal(items)
    } else {
      const items = await loadChapters([chapter.value])
      if (!items.length) throw new Error('empty')
      source.value = 'chapter'
      deal(items)
    }
  } catch {
    error.value = '练习题没加载上来，刷新试试。'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="pick">
    <p class="pick-label">练哪一科</p>
    <div class="chips">
      <button
        v-for="s in SUBJECTS"
        :key="s.id"
        type="button"
        class="chip"
        :class="{ on: subject === s.id, wait: !s.open }"
        @click="pickSubject(s.id)"
      >{{ s.label }}</button>
    </div>
    <template v-if="subject === 'k1'">
      <p class="pick-label">练哪一块</p>
      <div class="chips">
        <button
          v-for="p in K1_PARTS"
          :key="p.id"
          type="button"
          class="chip"
          :class="{ on: chapter === p.id }"
          @click="pickChapter(p.id)"
        >{{ p.label }}</button>
      </div>
    </template>
  </div>

  <div class="drill" v-if="!subjectOpen">这一科还没开。先看书里的占位页。</div>
  <div class="drill" v-else-if="error">{{ error }}</div>
  <div class="drill" v-else-if="loading">加载练习…</div>
  <div class="drill" v-else-if="item">
    <p class="meta">
      已做 {{ seen }} · 对 {{ correct }}
      <span v-if="source === 'bank'"> · 精选题库</span>
      <span v-else-if="source === 'chapter'"> · 这一块的跟测</span>
      <span v-else> · 九章随堂题</span>
      <span v-if="loops"> · 第 {{ loops + 1 }} 轮</span>
    </p>
    <p class="q">{{ item.q }}</p>
    <p v-if="item.image" class="pic">
      <img :src="item.image" :alt="item.q" />
    </p>
    <div class="opts">
      <button
        v-for="c in item.choices"
        :key="String(c.value)"
        type="button"
        class="btn"
        :class="{
          on: picked === c.value,
          ok: revealed && c.value === item.answer,
          bad: revealed && picked === c.value && c.value !== item.answer,
        }"
        :disabled="revealed"
        @click="choose(c.value)"
      >
        <template v-if="c.text === c.key">{{ c.key }}</template>
        <template v-else><b>{{ c.key }}</b> {{ c.text }}</template>
      </button>
    </div>
    <div v-if="revealed" class="why" :class="{ miss: picked !== item.answer }">
      <p class="verdict">
        {{ picked === item.answer ? '对。' : `错了。答案是「${label(item.answer)}」。` }}
      </p>
      <p v-if="item.why">{{ item.why }}</p>
      <button type="button" class="btn primary" @click="next">下一题</button>
    </div>
  </div>
</template>

<style scoped>
.pick {
  margin: 1.1rem 0 0.8rem;
}
.pick-label {
  margin: 0.7rem 0 0.35rem;
  color: var(--vp-c-text-2);
  font-size: 0.82rem;
}
.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}
.chip {
  padding: 0.22rem 0.65rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  background: var(--vp-c-bg);
  color: inherit;
  font-size: 0.84rem;
  cursor: pointer;
}
.chip.on {
  border-color: var(--vp-c-brand-1);
  background: color-mix(in srgb, var(--vp-c-brand-1) 14%, var(--vp-c-bg));
}
.chip.wait {
  color: var(--vp-c-text-3);
}
.drill {
  margin: 0.8rem 0 1.5rem;
  padding: 1.1rem 1.2rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg-soft);
}
.meta {
  margin: 0 0 0.6rem;
  color: var(--vp-c-text-2);
  font-size: 0.85rem;
}
.q {
  margin: 0 0 1rem;
  font-size: 1.05rem;
  line-height: 1.6;
}
.pic {
  margin: 0 0 1rem;
}
.pic img {
  max-width: min(100%, 280px);
  height: auto;
  border-radius: 8px;
  background: #fff;
}
.opts {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 0.55rem;
}
.btn {
  padding: 0.45rem 0.9rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background: var(--vp-c-bg);
  color: inherit;
  text-align: left;
  cursor: pointer;
}
.btn:disabled {
  cursor: default;
}
.btn.primary {
  margin-top: 0.8rem;
  width: fit-content;
  border-color: var(--vp-c-brand-1);
}
.btn.ok {
  border-color: #3d9a5b;
  background: color-mix(in srgb, #3d9a5b 16%, var(--vp-c-bg));
}
.btn.bad {
  border-color: #c45c5c;
  background: color-mix(in srgb, #c45c5c 16%, var(--vp-c-bg));
}
.why {
  margin-top: 1rem;
}
.why.miss {
  padding: 0.7rem 0.8rem;
  border-radius: 8px;
  background: color-mix(in srgb, #c45c5c 10%, var(--vp-c-bg-soft));
}
.verdict {
  font-weight: 600;
  margin: 0 0 0.4rem;
}
</style>
