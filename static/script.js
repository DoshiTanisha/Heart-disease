/* ===============================
   ACCURACY BAR CHART (BEST MODEL HIGHLIGHT)
================================ */

const acc = document.getElementById("accuracyChart");

if (acc) {
  new Chart(acc, {
    type: "bar",
    data: {
      labels: ["Logistic Regression", "Decision Tree", "Random Forest", "XGBoost (Best)"],
      datasets: [
        {
          label: "Accuracy (%)",
          data: [68, 71, 73, 74],
          backgroundColor: [
            "#38bdf8", // Logistic
            "#d218e6ff", // Decision Tree
            "#facc15", // Random Forest
            "#16a34a", // XGBoost (BEST)
          ],
          borderRadius: 10,
        },
      ],
    },
    options: {
      responsive: true,
      animation: {
        duration: 1500,
        easing: "easeOutBounce",
      },
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              if (context.dataIndex === 3) {
                return "XGBoost (Best Model): 74%";
              }
              return context.raw + "%";
            },
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          title: {
            display: true,
            text: "Accuracy Percentage",
          },
        },
        x: {
          title: {
            display: true,
            text: "Machine Learning Algorithms",
          },
        },
      },
    },
  });
}

/* ===============================
   HEATMAP / CORRELATION (RADAR)
================================ */

const heat = document.getElementById("heatmapChart");

if (heat) {
  new Chart(heat, {
    type: "radar",
    data: {
      labels: [
        "Age",
        "Blood Pressure",
        "BMI",
        "Cholesterol",
        "Glucose",
        "Physical Activity",
      ],
      datasets: [
        {
          label: "Feature Importance / Correlation",
          data: [0.75, 0.82, 0.65, 0.55, 0.48, 0.4],
          backgroundColor: "rgba(56,189,248,0.35)",
          borderColor: "#38bdf8",
          borderWidth: 2,
          pointBackgroundColor: "#22c55e",
        },
      ],
    },
    options: {
      responsive: true,
      animation: {
        duration: 1400,
        easing: "easeOutQuart",
      },
      scales: {
        r: {
          beginAtZero: true,
          max: 1,
          ticks: {
            stepSize: 0.2,
          },
        },
      },
      plugins: {
        legend: {
          position: "top",
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              return context.label + ": Correlation " + context.raw;
            },
          },
        },
      },
    },
  });
}


/* ===============================
   DARK MODE
================================ */
document.addEventListener("DOMContentLoaded", () => {

  const toggleBtn = document.getElementById("themeToggle");

  // APPLY SAVED THEME ON PAGE LOAD
  const savedTheme = localStorage.getItem("theme");

  if (savedTheme === "light") {
    document.body.classList.add("light-mode");
  }

  if (!toggleBtn) return;

  // SET INITIAL ICON
  toggleBtn.textContent = document.body.classList.contains("light-mode")
    ? "🌙"   // Light mode ON → show Moon
    : "☀️";  // Dark mode ON → show Sun

  // TOGGLE THEME
  toggleBtn.addEventListener("click", () => {

    document.body.classList.toggle("light-mode");

    const isLight = document.body.classList.contains("light-mode");

    // Change icon
    toggleBtn.textContent = isLight ? "🌙" : "☀️";

    // Save theme properly
    localStorage.setItem("theme", isLight ? "light" : "dark");
  });

});


