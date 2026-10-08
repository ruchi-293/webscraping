let allData = [];
let runsChart, wicketsChart;

async function getJSON(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error("Request failed");
  return response.json();
}

function number(n) {
  return Number(n || 0).toLocaleString("en-IN", {maximumFractionDigits: 2});
}

function renderTable(data) {
  const body = document.getElementById("tableBody");
  body.innerHTML = data.map(p => `
    <tr>
      <td><b>${escapeHTML(p["Player Name"])}</b></td>
      <td>${number(p.Matches)}</td>
      <td>${number(p.Runs)}</td>
      <td>${number(p["Batting Avg"])}</td>
      <td>${number(p.Wickets)}</td>
      <td>${number(p["Bowling Avg"])}</td>
    </tr>
  `).join("");
  document.getElementById("rowCount").textContent = `${data.length} players`;
}

function escapeHTML(value) {
  return String(value).replace(/[&<>"']/g, c => ({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"
  }[c]));
}

function makeChart(canvasId, labels, values, label) {
  return new Chart(document.getElementById(canvasId), {
    type: "bar",
    data: { labels, datasets: [{ label, data: values, borderRadius: 7 }] },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: "#8da8bb" }, grid: { display: false } },
        y: { ticks: { color: "#8da8bb" }, grid: { color: "#193044" } }
      }
    }
  });
}

function renderInsights(data) {
  const bestAverage = [...data].sort((a,b) => b["Batting Avg"] - a["Batting Avg"])[0];
  const mostMatches = [...data].sort((a,b) => b.Matches - a.Matches)[0];
  const bestBowling = [...data]
    .filter(p => p.Wickets > 0 && p["Bowling Avg"] > 0)
    .sort((a,b) => a["Bowling Avg"] - b["Bowling Avg"])[0];

  const insights = [
    ["Highest batting average", bestAverage ? `${bestAverage["Player Name"]} — ${number(bestAverage["Batting Avg"])}` : "—"],
    ["Most experienced", mostMatches ? `${mostMatches["Player Name"]} — ${number(mostMatches.Matches)} matches` : "—"],
    ["Best bowling average", bestBowling ? `${bestBowling["Player Name"]} — ${number(bestBowling["Bowling Avg"])}` : "—"]
  ];

  document.getElementById("insightList").innerHTML = insights.map(x =>
    `<div class="insight"><b>${x[0]}</b>${escapeHTML(x[1])}</div>`
  ).join("");
}

async function init() {
  try {
    const [data, summary] = await Promise.all([
      getJSON("/api/data"),
      getJSON("/api/summary")
    ]);
    allData = data;
    document.getElementById("players").textContent = summary.players;
    document.getElementById("runs").textContent = number(summary.total_runs);
    document.getElementById("topRuns").textContent = summary.top_run_scorer;
    document.getElementById("topBowler").textContent = summary.top_bowler;

    renderTable(allData);
    renderInsights(allData);

    const runs = [...allData].sort((a,b) => b.Runs-a.Runs).slice(0,10);
    const wickets = [...allData].sort((a,b) => b.Wickets-a.Wickets).slice(0,10);

    runsChart = makeChart("runsChart", runs.map(p=>p["Player Name"]), runs.map(p=>p.Runs), "Runs");
    wicketsChart = makeChart("wicketsChart", wickets.map(p=>p["Player Name"]), wickets.map(p=>p.Wickets), "Wickets");
  } catch (error) {
    console.error(error);
    document.getElementById("tableBody").innerHTML =
      `<tr><td colspan="6">Could not load data. Run the scraper first.</td></tr>`;
  }
}

document.getElementById("search").addEventListener("input", e => {
  const q = e.target.value.toLowerCase().trim();
  renderTable(allData.filter(p => p["Player Name"].toLowerCase().includes(q)));
});

init();
