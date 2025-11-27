// NEW - Get from URL parameter or localStorage
let USER_ID = new URLSearchParams(window.location.search).get("user_id") 
           || localStorage.getItem("user_id") 
           || 1;

console.log("Loaded user:", USER_ID);

async function loadDashboard() {
  try {
    // Fetch metrics from backend
    const res = await fetch(`/api/dashboard/metrics/${USER_ID}`);
    const data = await res.json();

    // Update header with user info
    document.getElementById("org-name").textContent = data.user.organization;
    document.getElementById("user-role").textContent = data.user.role;

    // Update KPI cards
    document.getElementById("completion-percentage").textContent =
      Math.round(data.kpis.training_completion.percentage) + "%";
    
    document.getElementById("avg-score").textContent =
      Math.round(data.kpis.average_quiz_score) + "%";
    
    document.getElementById("modules-completed").textContent =
      `${data.kpis.training_completion.completed}/${data.kpis.training_completion.total}`;
    
    document.getElementById("risk-score").textContent =
      data.kpis.risk_score || "--";

    // Draw charts
    drawProgressChart(data.completion_timeline);
    drawModulesChart(data.modules);

    // Display modules list
    displayModules(data.modules);

    // Load alerts
    await loadAlerts();

  } catch (error) {
    console.error("Error loading dashboard:", error);
    document.body.innerHTML = `<div class="alert alert-danger">Error loading dashboard: ${error.message}</div>`;
  }
}

async function loadAlerts() {
  try {
    const res = await fetch("/api/dashboard/alerts");
    const data = await res.json();

    const container = document.getElementById("alerts-section");
    container.innerHTML = data.alerts
      .map(a => `<div class="alert-item alert-${a.type}">${a.message}</div>`)
      .join("");
  } catch (error) {
    console.error("Error loading alerts:", error);
  }
}

function drawProgressChart(timeline) {
  const ctx = document.getElementById("progressChart").getContext("2d");
  const labels = timeline.map(p => p.date);
  const values = timeline.map(p => p.completed);

  new Chart(ctx, {
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
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function drawModulesChart(modules) {
  const completed = modules.filter(m => m.status === "completed").length;
  const inProgress = modules.filter(m => m.status === "in_progress").length;
  const notStarted = modules.filter(m => m.status === "not_started").length;

  const ctx = document.getElementById("modulesChart").getContext("2d");
  new Chart(ctx, {
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
        legend: {
          position: "bottom"
        }
      }
    }
  });
}

function displayModules(modules) {
  const container = document.getElementById("modules-list");
  container.innerHTML = modules.map(m => `
    <div class="training-item">
      <span><strong>${m.name}</strong></span>
      <span>${m.status}</span>
      ${m.score !== null ? `<span>${m.score}%</span>` : ""}
    </div>
  `).join("");
}

function startNewTraining() {
  alert("Select a module and start training!");
  // Will implement training page on Day 5
}

// Load dashboard when page loads
window.addEventListener("load", loadDashboard);
