// Get USER_ID from URL or localStorage
let USER_ID = new URLSearchParams(window.location.search).get("user_id")
             || localStorage.getItem("user_id")
             || 1;

localStorage.setItem("user_id", USER_ID);
console.log("✓ Dashboard loaded with USER_ID:", USER_ID);

const TRAINING_MODULES = [
  "Phishing Awareness",
  "Password Security",
  "Ransomware Prevention",
  "Data Protection Basics",
];

let progressChartInstance = null;
let modulesChartInstance = null;

// ============ MAIN LOAD FUNCTION ============
async function loadDashboard() {
  try {
    const res = await fetch(`/api/dashboard/metrics/${USER_ID}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    
    const data = await res.json();
    console.log("✓ Dashboard data loaded");

    // Update header
    const orgEl = document.getElementById("org-name");
    const roleEl = document.getElementById("user-role");
    if (orgEl) orgEl.textContent = data.user?.organization || "Loading...";
    if (roleEl) roleEl.textContent = data.user?.role || "Loading...";

    // Update KPI cards
    if (document.getElementById("completion-percentage")) {
      document.getElementById("completion-percentage").textContent = 
        Math.round(data.kpis?.training_completion?.percentage || 0) + "%";
    }
    if (document.getElementById("avg-score")) {
      document.getElementById("avg-score").textContent = 
        Math.round(data.kpis?.average_quiz_score || 0) + "%";
    }
    if (document.getElementById("modules-completed")) {
      const c = data.kpis?.training_completion?.completed || 0;
      const t = data.kpis?.training_completion?.total || 0;
      document.getElementById("modules-completed").textContent = `${c}/${t}`;
    }
    if (document.getElementById("risk-score")) {
      document.getElementById("risk-score").textContent = 
        data.kpis?.risk_score || "--";
    }

    // Draw charts
    if (data.completion_timeline && Array.isArray(data.completion_timeline)) {
      drawProgressChart(data.completion_timeline);
    }
    if (data.modules && Array.isArray(data.modules)) {
      drawModulesChart(data.modules);
      displayModules(data.modules);
    }

    // Populate module selector
    populateModuleSelector();

    // Load alerts
    await loadAlerts();

  } catch (error) {
    console.error("❌ Error loading dashboard:", error);
  }
}

// ============ ALERTS ============
async function loadAlerts() {
  try {
    const res = await fetch("/api/dashboard/alerts");
    if (!res.ok) return;
    
    const data = await res.json();
    const container = document.getElementById("alerts-section");
    if (container && data.alerts) {
      container.innerHTML = data.alerts
        .map(a => `<div class="alert-item alert-${a.type}">${a.message}</div>`)
        .join("");
    }
  } catch (error) {
    console.error("Error loading alerts:", error);
  }
}

// ============ CHARTS ============
function drawProgressChart(timeline) {
  const canvas = document.getElementById("progressChart");
  if (!canvas) return;
  
  if (progressChartInstance) progressChartInstance.destroy();
  
  const ctx = canvas.getContext("2d");
  const labels = (timeline || []).map(p => p.date);
  const values = (timeline || []).map(p => p.completed);

  progressChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Modules Completed",
        data: values,
        borderColor: "#667eea",
        backgroundColor: "rgba(102, 126, 234, 0.1)",
        tension: 0.3,
        fill: true,
        pointRadius: 5,
        pointBackgroundColor: "#667eea"
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } }
    }
  });
}

function drawModulesChart(modules) {
  const canvas = document.getElementById("modulesChart");
  if (!canvas) return;
  
  if (modulesChartInstance) modulesChartInstance.destroy();
  
  const completed = (modules || []).filter(m => m.status === "completed").length;
  const inProgress = (modules || []).filter(m => m.status === "in_progress").length;
  const notStarted = (modules || []).filter(m => m.status === "not_started").length;

  const ctx = canvas.getContext("2d");
  modulesChartInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Completed", "In Progress", "Not Started"],
      datasets: [{
        data: [completed, inProgress, notStarted],
        backgroundColor: ["#28a745", "#ffc107", "#e9ecef"]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "bottom" }
      }
    }
  });
}

function displayModules(modules) {
  const container = document.getElementById("modules-list");
  if (!container) return;
  
  container.innerHTML = (modules || [])
    .map(m => `
      <div class="training-item">
        <span><strong>${m.name}</strong></span>
        <span>${m.status}</span>
        ${m.score !== null && m.score !== undefined ? `<span>${m.score}%</span>` : ""}
      </div>
    `).join("");
}

// ============ MODULE SELECTOR ============
function populateModuleSelector() {
  const selector = document.getElementById("module-selector");
  if (!selector) {
    console.warn("⚠️  module-selector container not found");
    return;
  }

  selector.innerHTML = TRAINING_MODULES
    .map(module => `
      <button type="button" class="btn btn-outline-primary w-100 mb-2" 
              onclick="startModule('${module}')">
        ${module}
      </button>
    `).join("");
  
  console.log("✓ Module selector populated");
}

function startModule(moduleName) {
  console.log(`→ Starting module: ${moduleName}`);
  
  // Close modal
  const modalEl = document.getElementById("moduleModal");
  if (modalEl) {
    const modal = bootstrap.Modal.getInstance(modalEl);
    if (modal) modal.hide();
  }
  
  // Redirect
  const url = `/training?module=${encodeURIComponent(moduleName)}&user_id=${USER_ID}`;
  console.log(`→ Redirecting to: ${url}`);
  window.location.href = url;
}

// ============ PAGE INITIALIZATION ============
document.addEventListener("DOMContentLoaded", function() {
  console.log("✓ DOM ready, loading dashboard...");
  loadDashboard();
});

// Auto-refresh every 5 seconds
setInterval(loadDashboard, 5000);
