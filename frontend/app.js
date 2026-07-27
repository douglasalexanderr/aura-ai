const $ = (id) => document.getElementById(id);

function toast(message) {
  const el = $("toast");
  el.textContent = message;
  el.classList.add("show");
  setTimeout(() => el.classList.remove("show"), 2400);
}

document.querySelectorAll(".nav").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".nav").forEach(x => x.classList.remove("active"));
    document.querySelectorAll(".view").forEach(x => x.classList.remove("active"));
    btn.classList.add("active");
    $(btn.dataset.view).classList.add("active");
    $("pageTitle").textContent = btn.textContent;
    if (btn.dataset.view === "dashboard") loadDashboard();
    if (btn.dataset.view === "crm") loadLeads();
    if (btn.dataset.view === "history") loadHistory();
  });
});

async function api(url, options = {}) {
  const response = await fetch(url, {
    headers: {"Content-Type": "application/json", ...(options.headers || {})},
    ...options
  });
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || "Ocurrió un error");
  }
  return response.json();
}

async function loadDashboard() {
  const data = await api("/api/dashboard");
  $("statCampaigns").textContent = data.campaigns;
  $("statLeads").textContent = data.leads;
  $("statWon").textContent = data.won;
  $("statConversion").textContent = data.conversion + "%";
  $("recentCampaigns").innerHTML = data.recent_campaigns.length
    ? data.recent_campaigns.map(x => `<div class="card"><strong>${x.name}</strong><p>${x.city}</p></div>`).join("")
    : '<div class="empty">Aún no hay campañas.</div>';
}

$("generateBtn").addEventListener("click", async () => {
  const idea = $("idea").value.trim();
  if (idea.length < 5) return toast("Escribe una idea más completa.");

  const btn = $("generateBtn");
  btn.disabled = true;
  btn.textContent = "AURA está trabajando...";

  try {
    const data = await api("/api/campaigns", {
      method: "POST",
      body: JSON.stringify({
        idea,
        city: $("city").value,
        company: $("company").value,
        objective: $("objective").value,
        tone: $("tone").value
      })
    });

    const p = data.package;
    $("campaignName").textContent = data.name;
    $("campaignObjective").textContent = p.objective;
    $("targetAudience").innerHTML = p.target_audience.map(x => `<li>${x}</li>`).join("");
    $("valueProposition").textContent = p.value_proposition;
    $("videoScript").innerHTML = p.video_script.map(x => `<li>${x}</li>`).join("");
    $("flyerPreview").src = data.flyer_url + "?t=" + Date.now();
    $("exportLink").href = `/api/campaigns/${data.id}/export.txt`;
    $("socialPosts").innerHTML = p.social_posts.map(x => `
      <div class="card">
        <h4>${x.network}</h4>
        <p>${x.text}</p>
        <small>${x.hashtags.join(" ")}</small>
      </div>`).join("");
    $("calendar").innerHTML = p.calendar.map(x =>
      `<div><strong>Día ${x.day}</strong><p>${x.content}</p><small>${x.network}</small></div>`
    ).join("");

    $("campaignResult").classList.remove("hidden");
    $("campaignResult").scrollIntoView({behavior:"smooth"});
    toast("Campaña generada y guardada.");
    loadDashboard();
  } catch (error) {
    toast(error.message);
  } finally {
    btn.disabled = false;
    btn.textContent = "Crear campaña";
  }
});

$("saveLeadBtn").addEventListener("click", async () => {
  try {
    await api("/api/leads", {
      method:"POST",
      body: JSON.stringify({
        name: $("leadName").value,
        phone: $("leadPhone").value,
        email: $("leadEmail").value,
        service: $("leadService").value,
        source: "Manual",
        notes: $("leadNotes").value
      })
    });
    ["leadName","leadPhone","leadEmail","leadService","leadNotes"].forEach(id => $(id).value = "");
    toast("Prospecto guardado.");
    loadLeads();
    loadDashboard();
  } catch (error) {
    toast(error.message);
  }
});

async function loadLeads() {
  const leads = await api("/api/leads");
  $("leadsTable").innerHTML = leads.map(x => `
    <tr>
      <td>${x.name}<br><small>${x.email || ""}</small></td>
      <td>${x.service}</td>
      <td>${x.phone}</td>
      <td>
        <select class="status-select" onchange="changeStatus(${x.id}, this.value)">
          ${["Nuevo","Contactado","Cotizado","Ganado","Perdido"].map(s =>
            `<option ${s === x.status ? "selected" : ""}>${s}</option>`
          ).join("")}
        </select>
      </td>
    </tr>`).join("");
}

async function changeStatus(id, status) {
  await api(`/api/leads/${id}/status`, {
    method:"PATCH",
    body: JSON.stringify({status})
  });
  toast("Estado actualizado.");
  loadDashboard();
}

async function loadHistory() {
  const items = await api("/api/campaigns");
  $("campaignHistory").innerHTML = items.length
    ? items.map(x => `
      <div class="card">
        <h4>${x.name}</h4>
        <p>${x.idea}</p>
        <small>${x.created_at}</small><br><br>
        <a class="secondary" href="/api/campaigns/${x.id}/export.txt" target="_blank">Exportar</a>
      </div>`).join("")
    : '<div class="empty">Aún no hay campañas.</div>';
}

loadDashboard();
