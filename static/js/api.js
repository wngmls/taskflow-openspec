const API_BASE = "/api";

function getToken() { return localStorage.getItem("token"); }
function setToken(t) { localStorage.setItem("token", t); }
function removeToken() { localStorage.removeItem("token"); }
function getUser() { try { return JSON.parse(localStorage.getItem("user")); } catch { return null; } }
function setUser(u) { localStorage.setItem("user", JSON.stringify(u)); }
function removeUser() { localStorage.removeItem("user"); }

function redirectLogin() { removeToken(); removeUser(); location.href = "/login.html"; }

// team_id가 없으면 팀 선택으로 강제 이동
function requireTeam() {
  const user = getUser();
  if (!user || !user.team_id) { location.href = "/team.html"; return false; }
  return true;
}

async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (token) headers["Authorization"] = "Bearer " + token;
  const res = await fetch(API_BASE + path, { ...options, headers });
  if (res.status === 401) { redirectLogin(); return null; }
  return res;
}

async function apiJSON(path, options = {}) {
  const res = await apiFetch(path, options);
  if (!res) return null;
  const data = await res.json();
  if (!res.ok) throw { status: res.status, ...(data.error || data) };
  return data;
}
