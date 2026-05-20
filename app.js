const examDate = new Date("2026-06-14T09:00:00+08:00");
const storageKeys = {
  tasks: "lxy_english_tasks",
  mistakes: "lxy_english_mistakes"
};

const tasks = [
  { id: "words", title: "背 20 个高频词", note: "重点看拼写、词性和中文意思", tag: "词汇" },
  { id: "grammar", title: "完成 8 道语法选择", note: "记录不会判断的语法点", tag: "语法" },
  { id: "cloze", title: "练 1 组完形填空", note: "先抓上下文，再看固定搭配", tag: "题型" },
  { id: "writing", title: "积累 3 句作文表达", note: "今天优先背开头和结尾句", tag: "作文" }
];

const practices = [
  {
    id: "grammar",
    name: "语法选择",
    title: "时态判断",
    stem: "My sister ______ English for five years. She can speak it very well now.",
    options: ["learns", "learned", "has learned", "will learn"],
    answer: 2,
    explain: "for five years 表示从过去持续到现在，使用现在完成时 has learned。"
  },
  {
    id: "cloze",
    name: "完形填空",
    title: "上下文推断",
    stem: "When we meet problems, we should not give up. A positive mind can help us become ______.",
    options: ["weaker", "stronger", "slower", "quieter"],
    answer: 1,
    explain: "前文说不要放弃，积极心态会让人更强大，所以选 stronger。"
  },
  {
    id: "reading",
    name: "阅读理解",
    title: "细节定位",
    stem: "If a notice says 'No food or drinks in the library', what should students do?",
    options: ["Eat quietly", "Drink water only", "Keep food outside", "Share snacks"],
    answer: 2,
    explain: "No food or drinks 表示食物和饮料都不能带入，应放在外面。"
  },
  {
    id: "phrase",
    name: "固定搭配",
    title: "短语辨析",
    stem: "It is important for us to ______ a good habit of reading.",
    options: ["develop", "borrow", "catch", "invite"],
    answer: 0,
    explain: "develop a habit 是常见搭配，意思是养成习惯。"
  }
];

const writingTemplates = {
  opening: [
    "Nowadays, more and more students pay attention to ...",
    "As we all know, ... plays an important role in our daily life.",
    "I am glad to share my ideas about ... with you."
  ],
  body: [
    "First of all, we should ...",
    "What's more, it is a good idea to ...",
    "In my opinion, practice makes a big difference."
  ],
  ending: [
    "All in all, if we keep trying, we will make progress.",
    "I hope everyone can take action from now on.",
    "Only in this way can we become better and better."
  ]
};

const resources = [
  { title: "2025 年安徽省中考英语真题", type: "真题", href: "./英语08-25/2025年安徽省中考英语真题.docx", desc: "最新年份真题，适合整卷限时训练。" },
  { title: "2024 年安徽省中考英语真题解析版", type: "真题解析", href: "./英语08-25/2024年安徽省中考英语真题（解析版）.docx", desc: "带解析，适合做完后精读订正。" },
  { title: "安徽省中考英语真题·完形填空合集", type: "专项", href: "./安徽省中考英语真题·完形填空合集.docx", desc: "集中训练完形填空的上下文和搭配。" },
  { title: "阅读理解训练", type: "专项", href: "./阅读理解.docx", desc: "适合练习定位、推断和主旨题。" },
  { title: "中考英语大纲 1600 词汇", type: "词汇", href: "./中考英语大纲1600词汇.doc", desc: "词汇背诵和查漏补缺基础资料。" },
  { title: "重点词汇、高分写作句型每日一练", type: "每日练", href: "./九年级（中考）英语重点词汇、高分写作句型每日一练.pdf", desc: "适合每天 10 分钟热身。" },
  { title: "冲刺 2026 中考英语解题技巧", type: "技巧", href: "./冲刺2026中考-初中英语解题技巧（无水印PDF打印版）.pdf", desc: "考前方法和题型技巧汇总。" },
  { title: "英语作文写作技巧", type: "作文", href: "./英语作文技巧/英语作文写作技巧.doc", desc: "写作提分方法和表达积累。" }
];

let vocab = [];
let currentPractice = practices[0];

function getJson(key, fallback) {
  try {
    return JSON.parse(localStorage.getItem(key)) ?? fallback;
  } catch {
    return fallback;
  }
}

function setJson(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function updateCountdown() {
  const diff = examDate.getTime() - Date.now();
  const days = Math.max(0, Math.ceil(diff / 86400000));
  document.querySelector("#daysLeft").textContent = days;
}

function renderTasks() {
  const saved = getJson(storageKeys.tasks, {});
  const panel = document.querySelector("#taskPanel");
  panel.innerHTML = tasks.map(task => `
    <label class="task">
      <input type="checkbox" data-task="${task.id}" ${saved[task.id] ? "checked" : ""}>
      <span><strong>${task.title}</strong><small>${task.note}</small></span>
      <em class="tag">${task.tag}</em>
    </label>
  `).join("");
  panel.addEventListener("change", event => {
    if (!event.target.matches("[data-task]")) return;
    const next = getJson(storageKeys.tasks, {});
    next[event.target.dataset.task] = event.target.checked;
    setJson(storageKeys.tasks, next);
  });
}

function renderPracticeTabs() {
  const tabs = document.querySelector("#practiceTabs");
  tabs.innerHTML = practices.map(item => `
    <button class="tab ${item.id === currentPractice.id ? "active" : ""}" data-practice="${item.id}">${item.name}</button>
  `).join("");
}

function renderQuestion(selectedIndex = null) {
  const card = document.querySelector("#questionCard");
  const answered = selectedIndex !== null;
  card.innerHTML = `
    <h3>${currentPractice.title}</h3>
    <p>${currentPractice.stem}</p>
    <div>
      ${currentPractice.options.map((option, index) => {
        const status = answered && index === currentPractice.answer ? "correct" : answered && index === selectedIndex ? "wrong" : "";
        return `<button class="option ${status}" data-option="${index}" ${answered ? "disabled" : ""}>${String.fromCharCode(65 + index)}. ${option}</button>`;
      }).join("")}
    </div>
    ${answered ? `<div class="explain">${currentPractice.explain}</div>` : ""}
    <div class="question-actions">
      <button class="btn small" id="nextQuestion">换一题</button>
      <button class="btn small" id="addMistake">加入错题本</button>
    </div>
  `;
}

function addMistake(item = currentPractice) {
  const mistakes = getJson(storageKeys.mistakes, []);
  if (!mistakes.some(mistake => mistake.id === item.id)) {
    mistakes.unshift({ ...item, savedAt: new Date().toLocaleDateString("zh-CN") });
    setJson(storageKeys.mistakes, mistakes);
  }
  renderMistakes();
}

function renderMistakes() {
  const list = document.querySelector("#mistakeList");
  const mistakes = getJson(storageKeys.mistakes, []);
  document.querySelector("#mistakeCount").textContent = mistakes.length;
  if (!mistakes.length) {
    list.innerHTML = `<p class="empty">还没有错题。练习时点“加入错题本”，这里会自动保存。</p>`;
    return;
  }
  list.innerHTML = mistakes.map(item => `
    <article class="mistake-item">
      <strong>${item.name} · ${item.title}</strong>
      <p>${item.stem}</p>
      <small>答案：${item.options[item.answer]} · ${item.savedAt}</small>
    </article>
  `).join("");
}

function renderWords(words) {
  const grid = document.querySelector("#wordGrid");
  const list = words.slice(0, 12);
  if (!list.length) {
    grid.innerHTML = `<p class="empty">没有找到相关词汇。</p>`;
    return;
  }
  grid.innerHTML = list.map(item => `
    <article class="word-card">
      <strong>${item.word}</strong>
      <small>${item.phonetic || ""} ${item.pos || ""}</small>
      <p>${item.meaning || ""}</p>
    </article>
  `).join("");
}

function randomWords() {
  const source = vocab.length ? vocab : fallbackWords;
  const mixed = [...source].sort(() => Math.random() - 0.5);
  renderWords(mixed);
}

function renderTemplate(type = "opening") {
  document.querySelector("#templateText").innerHTML = writingTemplates[type].map(line => `<p>${line}</p>`).join("");
  document.querySelectorAll(".template").forEach(button => {
    button.classList.toggle("active", button.dataset.template === type);
  });
}

function renderResources(list = resources) {
  document.querySelector("#resourceGrid").innerHTML = list.map(item => `
    <a class="resource-card" href="${item.href}">
      <strong>${item.title}</strong>
      <p>${item.desc}</p>
      <span class="resource-type">${item.type}</span>
    </a>
  `).join("");
}

function bindEvents() {
  document.querySelector("#practiceTabs").addEventListener("click", event => {
    const button = event.target.closest("[data-practice]");
    if (!button) return;
    currentPractice = practices.find(item => item.id === button.dataset.practice);
    renderPracticeTabs();
    renderQuestion();
  });

  document.querySelector("#questionCard").addEventListener("click", event => {
    const option = event.target.closest("[data-option]");
    if (option) {
      const selected = Number(option.dataset.option);
      renderQuestion(selected);
      if (selected !== currentPractice.answer) addMistake();
      return;
    }
    if (event.target.id === "nextQuestion") {
      const index = practices.findIndex(item => item.id === currentPractice.id);
      currentPractice = practices[(index + 1) % practices.length];
      renderPracticeTabs();
      renderQuestion();
    }
    if (event.target.id === "addMistake") addMistake();
  });

  document.querySelector("#resetPractice").addEventListener("click", () => renderQuestion());
  document.querySelector("#clearMistakes").addEventListener("click", () => {
    setJson(storageKeys.mistakes, []);
    renderMistakes();
  });
  document.querySelector("#wordSearch").addEventListener("input", event => {
    const keyword = event.target.value.trim().toLowerCase();
    const source = vocab.length ? vocab : fallbackWords;
    if (!keyword) {
      renderWords(source);
      return;
    }
    renderWords(source.filter(item => {
      return `${item.word} ${item.meaning} ${item.pos}`.toLowerCase().includes(keyword);
    }));
  });
  document.querySelector("#randomWords").addEventListener("click", randomWords);
  document.querySelectorAll(".template").forEach(button => {
    button.addEventListener("click", () => renderTemplate(button.dataset.template));
  });
  document.querySelector("#resourceSearch").addEventListener("input", event => {
    const keyword = event.target.value.trim().toLowerCase();
    renderResources(resources.filter(item => `${item.title} ${item.type} ${item.desc}`.toLowerCase().includes(keyword)));
  });
}

const fallbackWords = [
  { word: "ability", phonetic: "[əˈbɪlɪtɪ]", pos: "n", meaning: "能力；才能" },
  { word: "achieve", phonetic: "[əˈtʃiːv]", pos: "v", meaning: "达到；取得" },
  { word: "active", phonetic: "[ˈæktɪv]", pos: "adj", meaning: "积极的；主动的" },
  { word: "advantage", phonetic: "[ədˈvɑːntɪdʒ]", pos: "n", meaning: "优点；好处" },
  { word: "develop", phonetic: "[dɪˈveləp]", pos: "v", meaning: "发展；养成" },
  { word: "progress", phonetic: "[ˈprəʊɡres]", pos: "n", meaning: "进步；进展" }
];

async function init() {
  updateCountdown();
  renderTasks();
  renderPracticeTabs();
  renderQuestion();
  renderMistakes();
  renderTemplate();
  renderResources();
  bindEvents();

  if (Array.isArray(window.LXY_VOCAB_DATA)) {
    vocab = window.LXY_VOCAB_DATA;
    document.querySelector("#wordCount").textContent = vocab.length;
    renderWords(vocab);
    return;
  }

  try {
    const response = await fetch("./常见固定搭配/vocab_data.json");
    vocab = await response.json();
    document.querySelector("#wordCount").textContent = vocab.length;
    renderWords(vocab);
  } catch {
    document.querySelector("#wordCount").textContent = fallbackWords.length;
    renderWords(fallbackWords);
  }
}

init();
