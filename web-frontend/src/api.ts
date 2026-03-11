const getAuthHeader = (): Record<string, string> => {
  const password = localStorage.getItem("auth_password") || "";
  if (!password) return {};
  return {
    Authorization: "Basic " + btoa("user:" + password),
  };
};

export async function healthCheck() {
  const res = await fetch("/api/health", { headers: getAuthHeader() });
  if (!res.ok) throw new Error(`Health check failed: ${res.status}`);
  return res.json();
}

export async function authCheck() {
  const res = await fetch("/api/auth/check", { headers: getAuthHeader() });
  if (!res.ok) throw new Error(`Auth failed: ${res.status}`);
  return res.json();
}

export interface UploadParams {
  files: File[];
  semaine_prod: number;
  annee_prod: number;
  commande_client: string[];
}

export async function uploadPDFs(params: UploadParams) {
  const form = new FormData();
  for (const f of params.files) {
    form.append("file", f);
  }
  form.append("semaine_prod", String(params.semaine_prod));
  form.append("annee_prod", String(params.annee_prod));
  for (const cc of params.commande_client) {
    form.append("commande_client", cc);
  }

  const res = await fetch("/api/upload", {
    method: "POST",
    headers: getAuthHeader(),
    body: form,
  });
  if (res.status === 401) throw new Error("AUTH");
  if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
  return res.json();
}

export async function getSettings() {
  const res = await fetch("/api/settings", { headers: getAuthHeader() });
  if (!res.ok) throw new Error(`Settings failed: ${res.status}`);
  return res.json();
}

export async function updateSettings(settings: Record<string, string>) {
  const res = await fetch("/api/settings", {
    method: "PUT",
    headers: { ...getAuthHeader(), "Content-Type": "application/json" },
    body: JSON.stringify(settings),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || `Update failed: ${res.status}`);
  }
  return res.json();
}

export async function getReleaseNotes() {
  const res = await fetch("/api/release-notes");
  if (!res.ok) throw new Error(`Release notes failed: ${res.status}`);
  return res.json() as Promise<{ version: string; content: string }>;
}

export async function deleteFile(filename: string) {
  const res = await fetch(`/api/files/${encodeURIComponent(filename)}`, {
    method: "DELETE",
    headers: getAuthHeader(),
  });
  if (!res.ok) throw new Error(`Delete failed: ${res.status}`);
  return res.json();
}

export async function listFiles() {
  const res = await fetch("/api/files", { headers: getAuthHeader() });
  if (res.status === 401) throw new Error("AUTH");
  if (!res.ok) throw new Error(`List files failed: ${res.status}`);
  return res.json();
}

export function downloadUrl(filename: string): string {
  return `/api/download/${encodeURIComponent(filename)}`;
}

export async function fetchFileBuffer(filename: string): Promise<ArrayBuffer> {
  const res = await fetch(`/api/download/${encodeURIComponent(filename)}`, {
    headers: getAuthHeader(),
  });
  if (!res.ok) throw new Error(`Download failed: ${res.status}`);
  return res.arrayBuffer();
}

export async function downloadFile(filename: string) {
  const res = await fetch(`/api/download/${encodeURIComponent(filename)}`, {
    headers: getAuthHeader(),
  });
  if (!res.ok) throw new Error(`Download failed: ${res.status}`);
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
