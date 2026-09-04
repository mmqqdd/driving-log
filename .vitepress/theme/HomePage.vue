<template>
  <div class="home">
    <header class="hero">
      <p class="eyebrow">北京 · 自动挡</p>
      <h1>C2 速通指南</h1>
      <p class="lead">2026 年 9 月开的头。现在在科目一。</p>
      <p class="chips">
        <span>C2</span>
        <span class="now">科目一</span>
      </p>
    </header>

    <div class="grid">
      <section class="panel teach">
        <p class="kicker">教学</p>
        <h2>课、练、考分开走</h2>
        <p class="desc">四科都在。先看后练，看完一节就跟几道题。现在学到科目一。</p>
        <div class="paths">
          <a href="/subjects/k1/">
            <strong>课程</strong>
            <span>四科。先看后练</span>
          </a>
          <a href="/subjects/practice">
            <strong>练习</strong>
            <span>随机一题一对错</span>
          </a>
          <a href="/exam">
            <strong>考试</strong>
            <span>100 题，45 分钟</span>
          </a>
        </div>
      </section>

      <section class="panel daily">
        <p class="kicker">日常</p>
        <h2>完整过程</h2>
        <p class="desc">从报名到拿证怎么走的，一路记下来。</p>
        <a class="go" href="/journal/">看日常</a>
      </section>
    </div>
  </div>
</template>

<style scoped>
.home {
  max-width: 52rem;
  margin: 0.4rem auto 3rem;
}
.hero {
  padding: 0.4rem 0 1.6rem;
}
.eyebrow {
  margin: 0 0 0.45rem;
  color: var(--vp-c-text-2);
  font-size: 0.92rem;
  letter-spacing: 0.08em;
}
.hero h1 {
  margin: 0 0 0.55rem;
  font-size: clamp(2.1rem, 6vw, 3rem);
  line-height: 1.15;
  letter-spacing: -0.03em;
  border: none;
}
.lead {
  margin: 0 0 0.9rem;
  color: var(--vp-c-text-2);
  font-size: 1.05rem;
}
.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin: 0;
}
.chips span {
  padding: 0.15rem 0.6rem;
  border-radius: 999px;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-2);
  font-size: 0.8rem;
}
.chips .now {
  background: color-mix(in srgb, var(--vp-c-brand-1) 16%, var(--vp-c-bg-soft));
  color: var(--vp-c-brand-1);
}
.grid {
  display: grid;
  grid-template-columns: 1.35fr 1fr;
  gap: 0.9rem;
}
.panel {
  padding: 1.15rem 1.2rem 1.2rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 14px;
  background: var(--vp-c-bg-soft);
}
.kicker {
  margin: 0 0 0.35rem;
  color: var(--vp-c-text-3);
  font-size: 0.75rem;
  letter-spacing: 0.12em;
}
.panel h2 {
  margin: 0 0 0.4rem;
  font-size: 1.25rem;
  border: none;
  padding: 0;
}
.desc {
  margin: 0 0 1rem;
  color: var(--vp-c-text-2);
  font-size: 0.95rem;
  line-height: 1.55;
}
.paths {
  display: grid;
  gap: 0.45rem;
}
.paths a,
.go {
  display: block;
  padding: 0.7rem 0.8rem;
  border-radius: 10px;
  background: var(--vp-c-bg);
  color: inherit;
  text-decoration: none;
  box-shadow: inset 0 0 0 1px var(--vp-c-divider);
}
.paths a:hover,
.go:hover {
  box-shadow: inset 0 0 0 1px var(--vp-c-brand-1);
}
.paths strong {
  display: block;
  font-size: 0.98rem;
}
.paths span {
  color: var(--vp-c-text-3);
  font-size: 0.82rem;
}
.go {
  width: fit-content;
  font-weight: 650;
}
@media (max-width: 720px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
