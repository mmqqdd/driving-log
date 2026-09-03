<script setup>
import { computed, onUnmounted, ref } from 'vue'

const SRC = '/practice/exam/k1/bank.json'
const TOTAL = 100
const MINUTES = 45
const PASS = 90
const QUOTA = { license: 20, traffic: 35, penalty: 25, accident: 10, vehicle: 10 }

const pack = ref(null)
const error = ref('')
const phase = ref('start')
const paper = ref([])
const answers = ref({})
const i = ref(0)
const left = ref(MINUTES * 60)
const startedAt = ref(0)
const used = ref(0)
let tick = null

const item = computed(() => paper.value[i.value] ?? null)
const answered = computed(() => Object.keys(answers.value).length)
const blank = computed(() => paper.value.length - answered.value)
const score = computed(() =>
  paper.value.filter((q) => answers.value[q.id] === q.answer).length
)
const passed = computed(() => score.value >= PASS)
const wrongs = computed(() =>
  paper.value.filter((q) => answers.value[q.id] && answers.value[q.id] !== q.answer)
)
const clock = computed(() => {
  const m = Math.floor(left.value / 60)
  const s = left.value % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
})
const usedClock = computed(() => {
  const m = Math.floor(used.value / 60)
  const s = used.value % 60
  return `${m} 分 ${String(s).padStart(2, '0')} 秒`
})

function shuffle(list) {
  const a = list.slice()
  for (let k = a.length - 1; k > 0; k--) {
    const j = Math.floor(Math.random() * (k + 1))
    ;[a[k], a[j]] = [a[j], a[k]]
  }
  return a
}

function takeByType(pool, type, n) {
  return shuffle(pool.filter((q) => q.type === type)).slice(0, n)
}

function draw(items) {
  const byGa = {}
  for (const q of items) {
    const g = QUOTA[q.ga] ? q.ga : 'traffic'
    ;(byGa[g] ||= []).push(q)
  }
  const picked = []
  const usedIds = new Set()
  for (const [ga, n] of Object.entries(QUOTA)) {
    const chunk = shuffle(byGa[ga] || []).slice(0, n)
    for (const q of chunk) {
      picked.push(q)
      usedIds.add(q.id)
    }
  }
  if (picked.length < TOTAL) {
    const rest = shuffle(items.filter((q) => !usedIds.has(q.id)))
    picked.push(...rest.slice(0, TOTAL - picked.length))
  }
  let paper = shuffle(picked).slice(0, TOTAL)
  const tfN = paper.filter((q) => q.type === 'tf').length
  if (tfN > 40) {
    const extra = paper.filter((q) => q.type === 'tf').slice(40)
    const fill = takeByType(
      items.filter((q) => !paper.some((p) => p.id === q.id)),
      'choice',
      extra.length
    )
    paper = paper.filter((q) => !extra.some((e) => e.id === q.id)).concat(fill)
  } else if (tfN < 40) {
    const extra = paper.filter((q) => q.type === 'choice').slice(0, 40 - tfN)
    const fill = takeByType(
      items.filter((q) => !paper.some((p) => p.id === q.id)),
      'tf',
      extra.length
    )
    paper = paper.filter((q) => !extra.some((e) => e.id === q.id)).concat(fill)
  }
  return shuffle(paper).slice(0, TOTAL)
}

async function load() {
  try {
    const res = await fetch(SRC)
    if (!res.ok) throw new Error(String(res.status))
    pack.value = await res.json()
    if (!pack.value.items?.length) throw new Error('empty')
  } catch {
    error.value = '题库没加载上来。刷新试试。'
  }
}

function startTimer() {
  stopTimer()
  tick = setInterval(() => {
    if (left.value <= 1) {
      finish(true)
      return
    }
    left.value -= 1
  }, 1000)
}

function stopTimer() {
  if (tick) {
    clearInterval(tick)
    tick = null
  }
}

function start() {
  paper.value = draw(pack.value.items)
  answers.value = {}
  i.value = 0
  left.value = MINUTES * 60
  startedAt.value = Date.now()
  phase.value = 'exam'
  startTimer()
}

function pick(key) {
  if (phase.value !== 'exam' || !item.value) return
  answers.value = { ...answers.value, [item.value.id]: key }
}

function go(n) {
  if (n < 0 || n >= paper.value.length) return
  i.value = n
}

function askFinish() {
  if (blank.value && !window.confirm(`还有 ${blank.value} 道没答。现在交卷？`)) return
  finish(false)
}

function finish(timeout) {
  stopTimer()
  used.value = Math.max(1, Math.round((Date.now() - startedAt.value) / 1000))
  if (timeout) left.value = 0
  phase.value = 'result'
}

function again() {
  phase.value = 'start'
}

onUnmounted(stopTimer)
load()
</script>

<template>
  <div class="exam" v-if="error">{{ error }}</div>
  <div class="exam" v-else-if="!pack">加载题库…</div>

  <div class="exam" v-else-if="phase === 'start'">
    <p class="lead">100 题，45 分钟，90 过。从精选 500 里抽，判断大约 40，单选大约 60。带图的题图在题目下面。</p>
    <p class="note">没有北京地方题，那一成用通行规定补上。选项没读全的题不进卷。整本 100 题仍以东方时尚 / 12123 为准。</p>
    <p class="meta">题库 {{ pack.pool }} 道可抽。</p>
    <button type="button" class="btn primary" @click="start">开始考试</button>
  </div>

  <div class="exam" v-else-if="phase === 'exam' && item">
    <div class="bar">
      <span>{{ i + 1 }} / {{ paper.length }}</span>
      <span :class="{ hurry: left < 300 }">{{ clock }}</span>
      <span>已答 {{ answered }}</span>
    </div>
    <p class="kind">{{ item.type === 'tf' ? '判断' : '单选' }}</p>
    <p class="q">{{ item.q }}</p>
    <img v-if="item.image" class="pic" :src="item.image" :alt="'第 ' + (i + 1) + ' 题图'" />
    <div class="opts">
      <button
        v-for="opt in item.options"
        :key="opt.key"
        type="button"
        class="btn opt"
        :class="{ on: answers[item.id] === opt.key }"
        @click="pick(opt.key)"
      >
        <b>{{ opt.key }}</b>
        <span>{{ opt.text }}</span>
      </button>
    </div>
    <div class="nav">
      <button type="button" class="btn" :disabled="i === 0" @click="go(i - 1)">上一题</button>
      <button type="button" class="btn" :disabled="i + 1 >= paper.length" @click="go(i + 1)">下一题</button>
      <button type="button" class="btn primary" @click="askFinish">交卷</button>
    </div>
    <div class="grid">
      <button
        v-for="(q, n) in paper"
        :key="q.id"
        type="button"
        class="dot"
        :class="{ here: n === i, done: answers[q.id] }"
        @click="go(n)"
      >{{ n + 1 }}</button>
    </div>
  </div>

  <div class="exam" v-else-if="phase === 'result'">
    <p class="score">{{ score }} 分</p>
    <p class="verdict">{{ passed ? '过了。' : '没过。' }} 用时 {{ usedClock }}。90 过。</p>
    <button type="button" class="btn primary" @click="again">再考一套</button>
    <div v-if="wrongs.length" class="review">
      <h3>错了这些</h3>
      <article v-for="q in wrongs" :key="q.id" class="miss">
        <p class="q">{{ q.q }}</p>
        <img v-if="q.image" class="pic" :src="q.image" alt="" />
        <p>你选了 {{ answers[q.id] }}，答案是 {{ q.answer }}。</p>
        <p v-if="q.why">{{ q.why }}</p>
      </article>
    </div>
  </div>
</template>

<style scoped>
.exam {
  margin: 1.2rem 0 2rem;
}
.lead, .q {
  line-height: 1.65;
}
.note, .meta, .kind {
  color: var(--vp-c-text-2);
  font-size: 0.92rem;
}
.bar {
  display: flex;
  justify-content: space-between;
  gap: 0.8rem;
  margin-bottom: 0.8rem;
  font-variant-numeric: tabular-nums;
}
.hurry {
  color: #c45c5c;
  font-weight: 600;
}
.pic {
  display: block;
  max-width: min(100%, 36rem);
  height: auto;
  margin: 0 0 1rem;
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
}
.opts {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
}
.btn {
  padding: 0.45rem 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background: var(--vp-c-bg);
  cursor: pointer;
}
.btn:disabled {
  opacity: 0.45;
  cursor: default;
}
.btn.primary {
  border-color: var(--vp-c-brand-1);
}
.btn.opt {
  display: flex;
  gap: 0.7rem;
  text-align: left;
}
.btn.opt b {
  flex: 0 0 1.2rem;
}
.btn.on {
  border-color: var(--vp-c-brand-1);
  background: color-mix(in srgb, var(--vp-c-brand-1) 14%, var(--vp-c-bg));
}
.nav {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin: 1.1rem 0;
}
.grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}
.dot {
  width: 2rem;
  height: 2rem;
  padding: 0;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  font-size: 0.75rem;
  cursor: pointer;
}
.dot.done {
  background: color-mix(in srgb, var(--vp-c-brand-1) 18%, var(--vp-c-bg));
}
.dot.here {
  border-color: var(--vp-c-brand-1);
  font-weight: 600;
}
.score {
  font-size: 2rem;
  font-weight: 650;
  margin: 0 0 0.3rem;
}
.verdict {
  margin: 0 0 1rem;
}
.review {
  margin-top: 2rem;
}
.miss {
  margin: 0 0 1.2rem;
  padding: 0.9rem 1rem;
  border-radius: 8px;
  background: color-mix(in srgb, #c45c5c 9%, var(--vp-c-bg-soft));
}
.miss .q {
  margin: 0 0 0.6rem;
}
</style>
