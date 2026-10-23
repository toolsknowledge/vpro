const $ = (id) => document.getElementById(id);
const notice = $("notice");
const sampleBtn = $("sampleBtn");
const uploadBtn = $("uploadBtn");
const fileInput = $("fileInput");
const askBtn = $("askBtn");

function showNotice(message, type = "success") {
  notice.textContent = message;
  notice.className = `notice ${type}`;
}
function hideNotice() {
  notice.className = "notice hidden";
}
function setBusy(button, busy, busyText) {
  if (!button.dataset.originalText) button.dataset.originalText = button.textContent.trim();
  button.disabled = busy;
  button.textContent = busy ? busyText : button.dataset.originalText;
}
async function apiRequest(url, options = {}) {
  const response = await fetch(url, options);
  let data;
  try { data = await response.json(); } catch { data = {}; }
  if (!response.ok) throw new Error(data.detail || `Request failed (${response.status})`);
  return data;
}
async function refreshStatus() {
  try {
    const data = await apiRequest("/api/status");
    $("statusText").textContent = `${data.indexed_chunks} chunks indexed`;
    $("statusText").previousElementSibling.style.background = "#20a36b";
  } catch {
    $("statusText").textContent = "Backend unavailable";
  }
}
function showIndexResult(data) {
  const box = $("indexResult");
  const names = (data.files || []).map(f => `${f.filename}: ${f.chunks} chunks`).join("<br>");
  const errors = (data.errors || []).map(e => `⚠ ${escapeHtml(e)}`).join("<br>");
  box.innerHTML = `<b>Indexing completed</b><br>${names || "No files indexed"}<br><b>Total chunks added:</b> ${data.total_chunks_added || 0}<br><b>Chunks in database:</b> ${data.collection_count ?? "—"}${errors ? `<br>${errors}` : ""}`;
  box.classList.remove("hidden");
}
function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, ch => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" }[ch]));
}
sampleBtn.addEventListener("click", async () => {
  hideNotice(); setBusy(sampleBtn, true, "Indexing samples…");
  try {
    const data = await apiRequest("/api/index-samples", { method: "POST" });
    showIndexResult(data); showNotice("Sample documents have been indexed. You can ask a question now.");
    await refreshStatus();
  } catch (e) { showNotice(e.message, "error"); }
  finally { setBusy(sampleBtn, false); }
});
fileInput.addEventListener("change", () => {
  uploadBtn.disabled = !fileInput.files || fileInput.files.length === 0;
});
uploadBtn.addEventListener("click", async () => {
  if (!fileInput.files.length) return;
  hideNotice(); setBusy(uploadBtn, true, "Uploading and indexing…");
  const form = new FormData();
  Array.from(fileInput.files).forEach(file => form.append("files", file));
  try {
    const data = await apiRequest("/api/upload", { method: "POST", body: form });
    showIndexResult(data); showNotice("Your documents have been indexed.");
    fileInput.value = ""; uploadBtn.disabled = true; await refreshStatus();
  } catch (e) { showNotice(e.message, "error"); }
  finally { setBusy(uploadBtn, false); uploadBtn.disabled = !fileInput.files.length; }
});
function updateChoiceCards() {
  const selected = document.querySelector('input[name="retrieve"]:checked')?.value;
  $("yesCard").classList.toggle("selected", selected === "yes");
  $("noCard").classList.toggle("selected", selected === "no");
}
document.querySelectorAll('input[name="retrieve"]').forEach(input => input.addEventListener("change", updateChoiceCards));
askBtn.addEventListener("click", async () => {
  const question = $("question").value.trim();
  if (!question) { showNotice("Please enter a question first.", "error"); $("question").focus(); return; }
  hideNotice(); setBusy(askBtn, true, "Claude is thinking…");
  try {
    const retrieve = document.querySelector('input[name="retrieve"]:checked').value === "yes";
    const data = await apiRequest("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, retrieve, top_k: Number($("topK").value) })
    });
    $("answerText").textContent = data.answer;
    $("modeBadge").textContent = data.retrieval_used ? "RAG · RETRIEVAL ON" : "BASELINE · RETRIEVAL OFF";
    $("chunkCount").textContent = `${data.chunks_considered} chunk${data.chunks_considered === 1 ? "" : "s"}`;
    $("evidenceIntro").textContent = data.retrieval_used
      ? "These are the passages returned by ChromaDB and supplied to Claude as reference context. Distance is a similarity-search distance; lower is generally closer."
      : "Retrieval was skipped, so no indexed document chunks were sent to Claude.";
    const list = $("chunksList");
    list.replaceChildren();
    if (data.retrieved_chunks.length) {
      data.retrieved_chunks.forEach(chunk => {
        const card = document.createElement("article");
        card.className = "chunk-card";
        const meta = document.createElement("div"); meta.className = "chunk-meta";
        const source = document.createElement("span"); source.textContent = `${chunk.source} · Chunk ${chunk.chunk_number}`;
        const distance = document.createElement("span"); distance.textContent = chunk.distance == null ? "" : `Distance: ${chunk.distance}`;
        meta.append(source, distance);
        const body = document.createElement("p"); body.textContent = chunk.text;
        card.append(meta, body); list.append(card);
      });
    } else {
      const empty = document.createElement("p");
      empty.className = "muted";
      empty.textContent = data.retrieval_used ? "No matching chunks were returned." : "No chunks retrieved because you selected NO.";
      list.append(empty);
    }
    $("answerPanel").classList.remove("hidden");
    $("answerPanel").scrollIntoView({ behavior: "smooth", block: "start" });
    showNotice("Answer generated successfully.");
  } catch (e) { showNotice(e.message, "error"); }
  finally { setBusy(askBtn, false); }
});
refreshStatus();
