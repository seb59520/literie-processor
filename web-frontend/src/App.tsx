import { useState } from "react";
import LoginPage from "./pages/LoginPage";
import UploadPage from "./pages/UploadPage";
import ResultsPage from "./pages/ResultsPage";
import FilesPage from "./pages/FilesPage";
import SettingsPage from "./pages/SettingsPage";
import ReleaseNotesPage from "./pages/ReleaseNotesPage";

type View = "upload" | "results" | "files" | "settings" | "release-notes";

function App() {
  const [authenticated, setAuthenticated] = useState(
    () => !!localStorage.getItem("auth_password")
  );
  const [view, setView] = useState<View>("upload");
  const [results, setResults] = useState<any>(null);

  const logout = () => {
    localStorage.removeItem("auth_password");
    setAuthenticated(false);
  };

  if (!authenticated) {
    return <LoginPage onLogin={() => setAuthenticated(true)} />;
  }

  if (view === "results" && results) {
    return (
      <ResultsPage
        data={results}
        onBack={() => { setResults(null); setView("upload"); }}
        onLogout={logout}
      />
    );
  }

  if (view === "files") {
    return (
      <FilesPage
        onBack={() => setView("upload")}
        onLogout={logout}
      />
    );
  }

  if (view === "settings") {
    return (
      <SettingsPage
        onBack={() => setView("upload")}
        onLogout={logout}
      />
    );
  }

  if (view === "release-notes") {
    return (
      <ReleaseNotesPage
        onBack={() => setView("upload")}
        onLogout={logout}
      />
    );
  }

  return (
    <UploadPage
      onResults={(data: any) => { setResults(data); setView("results"); }}
      onLogout={logout}
      onFiles={() => setView("files")}
      onSettings={() => setView("settings")}
      onReleaseNotes={() => setView("release-notes")}
    />
  );
}

export default App;
