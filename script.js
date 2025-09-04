const availableYears = [2024];

document.addEventListener("DOMContentLoaded", () => {
  const yearSelect = document.getElementById("year-select");
  const statsContainer = document.getElementById("stats-container");
  const title = document.getElementById("season-title");

  // Fill dropdown
  availableYears.forEach(year => {
    const option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    yearSelect.appendChild(option);
  });

  // Load latest by default
  loadStats(availableYears[availableYears.length - 1]);

  yearSelect.addEventListener("change", e => loadStats(e.target.value));

  async function loadStats(year) {
    try {
      const res = await fetch(`data/${year}.json`);
      const data = await res.json();
      renderStats(data);
    } catch (err) {
      statsContainer.innerHTML = `<p>Error loading stats for ${year}</p>`;
    }
  }

  function renderStats(data) {
    title.textContent = `${data.year} Season Stats`;
    statsContainer.innerHTML = "";

    // Running totals for participants
    const participantTotals = {};

    // Render each round separately
    data.rounds.forEach(round => {
      const roundDiv = document.createElement("div");
      roundDiv.classList.add("round");

      const heading = document.createElement("h2");
      heading.textContent = round.name;
      roundDiv.appendChild(heading);

      // Collect players drafted in this round
      const players = [];
      round.draftees.forEach(d => {
        const participant = data.participants.find(p => p.id === d.participantID);
        if (!(participant.id in participantTotals)) {
          participantTotals[participant.id] = 0;
        }
        d.draftees.forEach(player => {
          players.push({
            participantID: participant.id,
            participant: participant.name,
            ...player
          });
        });
      });

      // Create table
      const table = document.createElement("table");
      const thead = document.createElement("thead");
      const tbody = document.createElement("tbody");

      // Row 1: participants (colspan = #players + 1 for "Total")
      const rowParticipants = document.createElement("tr");
      rowParticipants.innerHTML = `<th rowspan="2">Date</th>`;
      const grouped = groupBy(players, "participantID");
      Object.entries(grouped).forEach(([pid, pl]) => {
        const th = document.createElement("th");
        th.colSpan = pl.length + 1; // +1 for total col
        const participant = data.participants.find(p => p.id == pid);
        th.textContent = participant.name;
        rowParticipants.appendChild(th);
      });
      thead.appendChild(rowParticipants);

      // Row 2: players + total col
      const rowPlayers = document.createElement("tr");
      Object.entries(grouped).forEach(([pid, pl]) => {
        pl.forEach(player => {
          const th = document.createElement("th");
          th.textContent = `${player.playerLast} (${player.teamCode}-${player.positionCode})`;
          rowPlayers.appendChild(th);
        });
        const thTotal = document.createElement("th");
        thTotal.textContent = "Total";
        rowPlayers.appendChild(thTotal);
      });
      thead.appendChild(rowPlayers);

      // Rows: scores by date for this round
      round.scores.forEach(day => {
        const row = document.createElement("tr");

        // Format date manually: "Month Day"
        function formatDate(isoDate) {
          const [year, month, day] = isoDate.split("-");
          const monthNames = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
          ];
          return `${monthNames[parseInt(month, 10) - 1]} ${parseInt(day, 10)}`;
        }

        const formattedDate = formatDate(day.date);
        const dateCell = document.createElement("td");
        dateCell.textContent = formattedDate;
        row.appendChild(dateCell);

        Object.entries(grouped).forEach(([pid, pl]) => {
          let participantDayTotal = 0;
          pl.forEach(player => {
            // Find this player’s score on this day
            const scoreObj = day.scores.find(s => s.playerID === player.playerID);
            const points = scoreObj ? scoreObj.points : 0;
            participantDayTotal += points;

            const td = document.createElement("td");
            td.textContent = points; // only points for the day
            row.appendChild(td);
          });

          // Update participant total (running)
          participantTotals[pid] += participantDayTotal;
          const tdTotal = document.createElement("td");
          tdTotal.textContent = participantTotals[pid];
          row.appendChild(tdTotal);
        });

        tbody.appendChild(row);
      });

      table.appendChild(thead);
      table.appendChild(tbody);
      roundDiv.appendChild(table);
      statsContainer.appendChild(roundDiv);
    });
  }

  function groupBy(arr, key) {
    return arr.reduce((acc, obj) => {
      const val = obj[key];
      acc[val] = acc[val] || [];
      acc[val].push(obj);
      return acc;
    }, {});
  }
});
