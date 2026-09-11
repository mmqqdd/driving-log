<script setup>
import { ref } from 'vue'

defineProps({ src: { type: String, required: true } })

const open = ref(false)
</script>

<template>
  <div class="pdf-viewer">
    <button type="button" class="pdf-toggle" @click="open = !open">
      {{ open ? '收起' : '预览' }}
    </button>
    <a class="pdf-link" :href="src" target="_blank" rel="noopener">在浏览器打开</a>
    <iframe v-if="open" class="pdf-frame" :src="src" loading="lazy" title="PDF 预览" />
  </div>
</template>

<style scoped>
.pdf-viewer {
  margin: 0.4rem 0 1.1rem;
}
.pdf-toggle {
  padding: 0.22rem 0.75rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  font-size: 0.85rem;
  cursor: pointer;
}
.pdf-toggle:hover {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}
.pdf-link {
  margin-left: 0.6rem;
  font-size: 0.85rem;
}
.pdf-frame {
  display: block;
  width: 100%;
  height: 520px;
  margin-top: 0.6rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background: var(--vp-c-bg-soft);
}
@media (max-width: 640px) {
  .pdf-frame {
    height: 420px;
  }
}
</style>
