<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  src: { type: String, required: true },
  count: { type: [Number, String], default: 10 },
})

const pack = ref(null)
const error = ref('')
const deck = ref([])
const i = ref(0)
const picked = ref(null)
const revealed = ref(false)
const score = ref(0)
const done = ref(false)

const item = computed(() => deck.value[i.value] ?? null)
const total = computed(() => deck.value.length)
const take = computed(() => {
  const n = Number(props.count)
  return Number.isFinite(n) && n > 0 ? n : 0
})

function shuffle(list) {
  const a = list.slice()
  for (let k = a.length - 1; k > 0; k--) {
    const j = Math.floor(Math.random() * (k + 1))
    ;[a[k], a[j]] = [a[j], a[k]]
  }
  return a
}

function deal() {
  const items = pack.value?.items ?? []
  const n = take.value ? Math.min(take.value, items.length) : items.length
  deck.value = shuffle(items).slice(0, n)
  i.value = 0
  picked.value = null
  revealed.value = false
  score.value = 0
  done.value = false
}

async function load() {
  try {
    const res = await fetch(props.src)
    if (!res.ok) throw new Error(String(res.status))
    pack.value = await res.json()
    deal()
  } catch {
    error.value = '练习题没加载上来，刷新试试。'
  }
}

load()
watch(() => props.src, load)

function choose(val) {
  if (revealed.value || !item.value) return
  picked.value = val
  revealed.value = true
  if (val === item.value.answer) score.value += 1
}

function next() {
  if (i.value + 1 >= total.value) {
    done.value = true
    return
  }
  i.value += 1
  picked.value = null
  revealed.value = false
}

function label(val) {
  if (item.value?.type === 'tf') return val ? '对' : '错'
  return String(val)
}
</script>

<template>
  <div class="quiz" v-if="error">{{ error }}</div>
  <div class="quiz" v-else-if="!pack">加载练习…</div>
  <div class="quiz" v-else-if="done">
    <p class="quiz-score">{{ score }} / {{ total }}</p>
    <p>{{ score === total ? '这节过了。' : '错的看完解析，再来一组。' }}</p>
    <button type="button" class="quiz-btn primary" @click="deal">再来 {{ total }} 道</button>
  </div>
  <div class="quiz" v-else-if="item">
    <p class="quiz-meta">{{ pack.title }} · 随机 {{ i + 1 }} / {{ total }}</p>
    <p class="quiz-q">{{ item.q }}</p>
    <p v-if="item.image" class="quiz-pic">
      <img :src="item.image" :alt="item.q" />
    </p>
    <div class="quiz-opts">
      <button
        v-if="item.type === 'tf'"
        type="button"
        class="quiz-btn"
        :class="{ on: picked === true, ok: revealed && item.answer === true, bad: revealed && picked === true && item.answer !== true }"
        :disabled="revealed"
        @click="choose(true)"
      >对</button>
      <button
        v-if="item.type === 'tf'"
        type="button"
        class="quiz-btn"
        :class="{ on: picked === false, ok: revealed && item.answer === false, bad: revealed && picked === false && item.answer !== false }"
        :disabled="revealed"
        @click="choose(false)"
      >错</button>
      <button
        v-for="opt in item.options || []"
        :key="opt"
        type="button"
        class="quiz-btn"
        :class="{ on: picked === opt, ok: revealed && item.answer === opt, bad: revealed && picked === opt && item.answer !== opt }"
        :disabled="revealed"
        @click="choose(opt)"
      >{{ opt }}</button>
    </div>
    <div v-if="revealed" class="quiz-why" :class="{ miss: picked !== item.answer }">
      <p class="quiz-verdict">{{ picked === item.answer ? '对。' : `错了。答案是「${label(item.answer)}」。` }}</p>
      <p>{{ item.why }}</p>
      <button type="button" class="quiz-btn primary" @click="next">
        {{ i + 1 >= total ? '看结果' : '下一题' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.quiz {
  margin: 1.5rem 0;
  padding: 1.1rem 1.2rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg-soft);
}
.quiz-meta {
  margin: 0 0 0.6rem;
  color: var(--vp-c-text-2);
  font-size: 0.85rem;
}
.quiz-q {
  margin: 0 0 1rem;
  font-size: 1.05rem;
  line-height: 1.6;
}
.quiz-pic {
  margin: 0 0 1rem;
}
.quiz-pic img {
  max-width: min(100%, 280px);
  height: auto;
  border-radius: 8px;
  background: #fff;
}
.quiz-opts {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}
.quiz-btn {
  padding: 0.4rem 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background: var(--vp-c-bg);
  cursor: pointer;
}
.quiz-btn:disabled {
  cursor: default;
}
.quiz-btn.primary {
  margin-top: 0.8rem;
  border-color: var(--vp-c-brand-1);
}
.quiz-btn.ok {
  border-color: #3d9a5b;
  background: color-mix(in srgb, #3d9a5b 16%, var(--vp-c-bg));
}
.quiz-btn.bad {
  border-color: #c45c5c;
  background: color-mix(in srgb, #c45c5c 16%, var(--vp-c-bg));
}
.quiz-why {
  margin-top: 1rem;
}
.quiz-why.miss {
  padding: 0.7rem 0.8rem;
  border-radius: 8px;
  background: color-mix(in srgb, #c45c5c 10%, var(--vp-c-bg-soft));
}
.quiz-verdict {
  font-weight: 600;
  margin: 0 0 0.4rem;
}
.quiz-score {
  font-size: 1.6rem;
  font-weight: 600;
  margin: 0 0 0.4rem;
}
</style>
