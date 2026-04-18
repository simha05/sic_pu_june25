// ── Config ────────────────────────────────────────────────
const API_BASE = "http://localhost:8000"; // Change to your backend URL

// ── State ─────────────────────────────────────────────────
let token = localStorage.getItem("mv_token") || null;
let currentUser = JSON.parse(localStorage.getItem("mv_user") || "null");
let selectedFile = null;
let lastResult = null;

// ── Init ──────────────────────────────────────────────────
window.addEventListener("DOMContentLoaded", () => {
  if (token && currentUser) {
    showDashboard();
  }

  // Enter key on login
  document.getElementById("loginPass").addEventListener("keydown", (e) => {
    if (e.key === "Enter") doLogin();
  });
  document.getElementById("loginEmail").addEventListener("keydown", (e) => {
    if (e.key === "Enter") doLogin();
  });
});

// ── Auth ──────────────────────────────────────────────────
async function doLogin() {
  const email = document.getElementById("loginEmail").value.trim();
  const pass = document.getElementById("loginPass").value;
  const btn = document.getElementById("btnLogin");
  const errEl = document.getElementById("loginError");

  errEl.classList.remove("show");
  if (!email || !pass) {
    showLoginError("Please enter your email and password.");
    return;
  }

  btn.disabled = true;
  btn.textContent = "Signing in…";

  try {
    const res = await fetch(`${API_BASE}/api/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password: pass }),
    });
    const data = await res.json();

    if (!res.ok) {
      showLoginError(data.detail || "Invalid credentials.");
      return;
    }

    token = data.token;
    currentUser = data.user;
    localStorage.setItem("mv_token", token);
    localStorage.setItem("mv_user", JSON.stringify(currentUser));
    showDashboard();
  } catch (err) {
    showLoginError("Cannot reach server. Is the backend running?");
  } finally {
    btn.disabled = false;
    btn.textContent = "Sign In →";
  }
}

function logout() {
  token = null;
  currentUser = null;
  localStorage.removeItem("mv_token");
  localStorage.removeItem("mv_user");
  selectedFile = null;
  lastResult = null;
  showPage("pageLogin");
  document.getElementById("facultyBadge").style.display = "none";
  document.getElementById("btnLogout").style.display = "none";
  document.getElementById("loginEmail").value = "";
  document.getElementById("loginPass").value = "";
}

function showLoginError(msg) {
  const el = document.getElementById("loginError");
  el.textContent = msg;
  el.classList.add("show");
}

function togglePass() {
  const inp = document.getElementById("loginPass");
  const btn = document.querySelector(".show-btn");
  if (inp.type === "password") {
    inp.type = "text";
    btn.textContent = "HIDE";
  } else {
    inp.type = "password";
    btn.textContent = "SHOW";
  }
}

// ── Dashboard ─────────────────────────────────────────────
function showDashboard() {
  showPage("pageDashboard");

  // Set faculty badge
  if (currentUser) {
    document.getElementById("facultyBadge").style.display = "flex";
    document.getElementById("btnLogout").style.display = "block";
    document.getElementById("facultyName").textContent = currentUser.name;
    document.getElementById("facultyDept").textContent = currentUser.dept;
    const initials = currentUser.name.split(" ").map(w => w[0]).join("").slice(0, 2);
    document.getElementById("facultyAvatar").textContent = initials;
  }

  loadStats();
  loadAuditLog();
}

async function loadStats() {
  try {
    const res = await authFetch("/api/stats");
    const data = await res.json();
    document.getElementById("statTotal").textContent = data.total_analyzed;
    document.getElementById("statFlagged").textContent = data.flagged;
    document.getElementById("statApproved").textContent = data.approved;
    document.getElementById("statAvg").textContent =
      data.total_analyzed > 0 ? data.avg_risk_score + "%" : "—";
  } catch (e) {
    console.warn("Stats load failed:", e);
  }
}

async function loadAuditLog() {
  try {
    const res = await authFetch("/api/audit");
    const data = await res.json();
    const logs = data.logs || [];
    document.getElementById("auditCount").textContent = logs.length;
    renderAuditRows(logs);
  } catch (e) {
    console.warn("Audit load failed:", e);
  }
}

function renderAuditRows(logs) {
  const container = document.getElementById("auditRows");
  if (!logs.length) {
    container.innerHTML = `<div style="padding:24px 22px;font-size:12px;color:var(--muted)">No analyses yet.</div>`;
    return;
  }
  container.innerHTML = logs.map(log => {
    const pillClass = log.risk_level === "HIGH" ? "pill-high" :
                      log.risk_level === "LOW"  ? "pill-low" : "pill-medium";
    const dt = new Date(log.timestamp).toLocaleString();
    return `
      <div class="audit-row">
        <div>
          <div class="audit-student">${escHtml(log.student_name)}</div>
          <div class="audit-file">${escHtml(log.file_name || "—")}</div>
        </div>
        <div class="audit-time">${dt}</div>
        <div class="audit-faculty">${escHtml(log.analysed_by)}</div>
        <div><span class="risk-pill ${pillClass}">${log.risk_level}</span></div>
      </div>`;
  }).join("");
}

// ── File Handling ─────────────────────────────────────────
function handleDragOver(e) {
  e.preventDefault();
  document.getElementById("dropzone").classList.add("drag");
}

function handleDragLeave() {
  document.getElementById("dropzone").classList.remove("drag");
}

function handleDrop(e) {
  e.preventDefault();
  const dz = document.getElementById("dropzone");
  dz.classList.remove("drag");
  const file = e.dataTransfer.files[0];
  if (file) setFile(file);
}

function handleFileSelect(e) {
  const file = e.target.files[0];
  if (file) setFile(file);
}

function setFile(file) {
  const allowed = ["image/jpeg", "image/png", "image/webp", "application/pdf"];
  if (!allowed.includes(file.type)) {
    showError("Unsupported file type. Please upload JPG, PNG, WEBP, or PDF.");
    return;
  }
  selectedFile = file;
  const dz = document.getElementById("dropzone");
  dz.classList.add("has-file");
  document.getElementById("dropIcon").textContent = "✅";
  document.getElementById("dropTitle").textContent = file.name;
  document.getElementById("dropSub").textContent =
    (file.size / 1024).toFixed(1) + " KB — ready to analyze";
  document.getElementById("btnAnalyse").classList.add("show");
  hideError();
}

// ── Analysis ──────────────────────────────────────────────
async function startAnalysis() {
  if (!selectedFile) return;

  const studentName = document.getElementById("studentName").value.trim();
  const studentId = document.getElementById("studentId").value.trim();

  hideError();
  showProcessing();

  // Animate steps
  const steps = ["ps1","ps2","ps3","ps4","ps5"];
  const labels = [
    "Uploading document…",
    "Extracting text with OCR…",
    "Running Gemini AI analysis…",
    "Validating fraud rules…",
    "Generating risk report…",
  ];
  let stepIdx = 0;
  const stepTimer = setInterval(() => {
    if (stepIdx > 0) {
      document.getElementById(steps[stepIdx - 1]).classList.remove("active");
      document.getElementById(steps[stepIdx - 1]).classList.add("done");
      document.getElementById(`${steps[stepIdx - 1]} .step-dot`);
      const prevDot = document.querySelector(`#${steps[stepIdx-1]} .step-dot`);
      if (prevDot) prevDot.textContent = "✓";
    }
    if (stepIdx < steps.length) {
      document.getElementById(steps[stepIdx]).classList.add("active");
      document.getElementById("procStep").textContent = labels[stepIdx];
      stepIdx++;
    } else {
      clearInterval(stepTimer);
    }
  }, 1200);

  try {
    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("student_name", studentName);
    formData.append("student_id", studentId);

    const res = await authFetch("/api/analyze", {
      method: "POST",
      body: formData,
    });

    clearInterval(stepTimer);

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Analysis failed.");
    }

    const data = await res.json();
    lastResult = data;

    hideProcessing();
    renderResults(data);
    loadStats();
    loadAuditLog();
  } catch (err) {
    clearInterval(stepTimer);
    hideProcessing();
    showError("Analysis failed: " + err.message);
    resetDropzone();
  }
}

function retryAnalysis() {
  if (!selectedFile) return;
  document.getElementById("resultsWrap").classList.remove("show");
  startAnalysis();
}

// ── Results Rendering ─────────────────────────────────────
function renderResults(data) {
  const score = data.risk_score || 0;
  const level = (data.risk_level || "MEDIUM").toUpperCase();

  // Score circle
  const circumference = 264;
  const offset = circumference - (score / 100) * circumference;
  const fill = document.getElementById("scoreFill");
  const color = level === "HIGH" ? "#f43f5e" : level === "LOW" ? "#10b981" : "#f59e0b";
  fill.style.stroke = color;
  setTimeout(() => { fill.style.strokeDashoffset = offset; }, 100);

  document.getElementById("scoreNum").textContent = score + "%";
  document.getElementById("scoreNum").style.color = color;

  // Verdict badge
  const badge = document.getElementById("verdictBadge");
  badge.textContent = "● " + level + " RISK";
  badge.className = "verdict-badge badge-" + level.toLowerCase();

  // Hero
  document.getElementById("heroVerdict").textContent = data.verdict || "Analysis Complete";
  const s = [data.student_name, data.student_id].filter(Boolean).join(" · ");
  document.getElementById("heroStudent").textContent = s || "No student info provided";

  // Risk bar
  const bar = document.getElementById("riskBarFill");
  bar.style.background = color;
  setTimeout(() => { bar.style.width = score + "%"; }, 100);

  // Hero stats
  document.getElementById("heroStats").innerHTML =
    `<span>Analyzed by <strong>${escHtml(data.analysed_by)}</strong></span>
     <span>Time: <strong>${new Date(data.timestamp).toLocaleTimeString()}</strong></span>
     <span>Risk: <strong style="color:${color}">${score}%</strong></span>`;

  // Extracted fields
  const fields = data.extracted_fields || {};
  const fieldLabels = {
    patient_name: "Patient Name",
    doctor_name: "Doctor Name",
    doctor_registration: "Doctor Reg. No.",
    hospital_name: "Hospital/Clinic",
    issue_date: "Issue Date",
    valid_from: "Valid From",
    valid_until: "Valid Until",
    diagnosis: "Diagnosis",
    signature_present: "Signature",
    stamp_present: "Official Stamp",
  };
  document.getElementById("extractedFields").innerHTML = Object.entries(fieldLabels).map(([k, label]) => {
    let val = fields[k];
    if (val === null || val === undefined || val === "") val = null;
    if (typeof val === "boolean") val = val ? "✓ Present" : "✗ Not found";
    return `<div class="field-row">
      <span class="field-key">${label}</span>
      <span class="field-val ${val ? "" : "missing"}">${val ? escHtml(String(val)) : "—"}</span>
    </div>`;
  }).join("");

  // Observations
  const obs = data.observations || [];
  document.getElementById("aiObservations").innerHTML = obs.length
    ? obs.map(o => `<div class="obs-item"><span class="obs-dot">◆</span><span>${escHtml(o)}</span></div>`).join("")
    : '<div style="font-size:13px;color:var(--muted)">No observations.</div>';

  // Rule checks
  const rules = data.rule_checks || [];
  document.getElementById("rulesGrid").innerHTML = rules.map(r => `
    <div class="rule-item ${r.pass ? "pass" : "fail"}">
      <div class="rule-icon">${r.pass ? "✅" : "❌"}</div>
      <div>
        <div class="rule-name">${escHtml(r.name)}</div>
        <div class="rule-detail">${escHtml(r.detail || "")}</div>
      </div>
    </div>`).join("");

  // Raw OCR
  document.getElementById("rawText").textContent = data.raw_text || "No OCR text extracted.";

  // Debug
  document.getElementById("debugText").textContent =
    `Timestamp: ${data.timestamp}\nAnalysed by: ${data.analysed_by}\nDebug: ${data.debug_info || "N/A"}`;

  document.getElementById("resultsWrap").classList.add("show");
  document.getElementById("resultsWrap").scrollIntoView({ behavior: "smooth", block: "start" });
}

// ── Export ────────────────────────────────────────────────
function exportReport() {
  if (!lastResult) return;
  const d = lastResult;
  const lines = [
    "MEDVERIFY — ANALYSIS REPORT",
    "=".repeat(50),
    `Date: ${new Date(d.timestamp).toLocaleString()}`,
    `Analysed by: ${d.analysed_by}`,
    `Student: ${d.student_name || "—"} (${d.student_id || "—"})`,
    "",
    `RISK SCORE: ${d.risk_score}%`,
    `RISK LEVEL: ${d.risk_level}`,
    `VERDICT: ${d.verdict}`,
    "",
    "EXTRACTED FIELDS",
    "-".repeat(30),
    ...Object.entries(d.extracted_fields || {}).map(([k, v]) => `${k}: ${v ?? "—"}`),
    "",
    "AI OBSERVATIONS",
    "-".repeat(30),
    ...(d.observations || []).map(o => `• ${o}`),
    "",
    "RULE CHECKS",
    "-".repeat(30),
    ...(d.rule_checks || []).map(r => `[${r.pass ? "PASS" : "FAIL"}] ${r.name}: ${r.detail}`),
    "",
    "OCR EXTRACTED TEXT",
    "-".repeat(30),
    d.raw_text || "(none)",
  ];
  const blob = new Blob([lines.join("\n")], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `medverify_${d.student_id || "report"}_${Date.now()}.txt`;
  a.click();
  URL.revokeObjectURL(url);
}

// ── UI Helpers ────────────────────────────────────────────
function showPage(id) {
  document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
  document.getElementById(id).classList.add("active");
}

function showProcessing() {
  document.getElementById("uploadCard") && (document.querySelector(".upload-card").style.display = "none");
  document.querySelector(".upload-card").style.display = "none";
  document.getElementById("processingWrap").classList.add("show");
  document.getElementById("resultsWrap").classList.remove("show");
  // Reset step indicators
  ["ps1","ps2","ps3","ps4","ps5"].forEach(id => {
    const el = document.getElementById(id);
    el.classList.remove("done","active");
    const dot = el.querySelector(".step-dot");
    if (dot) dot.textContent = el.id.replace("ps","");
  });
}

function hideProcessing() {
  document.querySelector(".upload-card").style.display = "block";
  document.getElementById("processingWrap").classList.remove("show");
}

function resetToUpload() {
  document.getElementById("resultsWrap").classList.remove("show");
  resetDropzone();
  document.getElementById("studentName").value = "";
  document.getElementById("studentId").value = "";
  selectedFile = null;
  lastResult = null;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function resetDropzone() {
  const dz = document.getElementById("dropzone");
  dz.classList.remove("has-file","drag");
  document.getElementById("dropIcon").textContent = "📎";
  document.getElementById("dropTitle").textContent = "Drop certificate here";
  document.getElementById("dropSub").textContent = "or click to browse files";
  document.getElementById("btnAnalyse").classList.remove("show");
  document.getElementById("fileInput").value = "";
}

function showError(msg) {
  const el = document.getElementById("errorBox");
  el.textContent = msg;
  el.classList.add("show");
}

function hideError() {
  document.getElementById("errorBox").classList.remove("show");
}

function toggleRaw() {
  const body = document.getElementById("rawBody");
  const btn = document.querySelector(".raw-toggle");
  body.classList.toggle("open");
  btn.textContent = body.classList.contains("open") ? "[ hide ]" : "[ show ]";
}

function toggleDebug() {
  const body = document.getElementById("debugBody");
  const btn = document.querySelector(".debug-toggle");
  body.classList.toggle("open");
  btn.textContent = body.classList.contains("open") ? "[ hide ]" : "[ show ]";
}

function toggleAudit() {
  const body = document.getElementById("auditBody");
  const btn = document.getElementById("auditToggleBtn");
  body.classList.toggle("open");
  btn.textContent = body.classList.contains("open") ? "[ hide ]" : "[ show ]";
}

// ── API Helper ────────────────────────────────────────────
function authFetch(path, options = {}) {
  const headers = options.headers || {};
  if (token) headers["Authorization"] = `Bearer ${token}`;
  // Don't set Content-Type for FormData (browser sets it with boundary)
  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }
  return fetch(`${API_BASE}${path}`, { ...options, headers });
}

function escHtml(str) {
  if (typeof str !== "string") return str;
  return str.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}
