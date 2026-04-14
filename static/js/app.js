async function send(type) {
  await fetch("/api/events", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({event_type: type})
  });
  load();
}

async function load() {
  const res = await fetch("/api/events");
  const data = await res.json();

  const ul = document.getElementById("events");
  ul.innerHTML = "";

  data.forEach(e => {
    const li = document.createElement("li");
    li.textContent = e.label + " " + e.created_at;
    ul.appendChild(li);
  });
}