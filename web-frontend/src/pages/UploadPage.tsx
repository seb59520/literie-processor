import { useState, useRef, useEffect } from "react";
import { uploadPDFs } from "../api";
import Header from "../components/Header";
import Footer from "../components/Footer";

interface Props {
  onResults: (data: any) => void;
  onLogout: () => void;
  onFiles: () => void;
  onSettings: () => void;
  onReleaseNotes?: () => void;
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return bytes + " o";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " Ko";
  return (bytes / (1024 * 1024)).toFixed(1) + " Mo";
}

export default function UploadPage({ onResults, onLogout, onFiles, onSettings, onReleaseNotes }: Props) {
  const [files, setFiles] = useState<File[]>([]);
  const [semaine, setSemaine] = useState(() => {
    const saved = localStorage.getItem("matelas_semaine");
    if (saved) return Number(saved);
    const now = new Date();
    const start = new Date(now.getFullYear(), 0, 1);
    const diff = now.getTime() - start.getTime();
    return Math.ceil(diff / (7 * 24 * 60 * 60 * 1000));
  });
  const [annee, setAnnee] = useState(() => {
    const saved = localStorage.getItem("matelas_annee");
    if (saved) return Number(saved);
    return new Date().getFullYear();
  });
  const [commandes, setCommandes] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [dragOver, setDragOver] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const [progressStage, setProgressStage] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    localStorage.setItem("matelas_semaine", String(semaine));
  }, [semaine]);

  useEffect(() => {
    localStorage.setItem("matelas_annee", String(annee));
  }, [annee]);

  useEffect(() => {
    if (loading) {
      setElapsed(0);
      setProgressStage("Envoi des fichiers...");
      timerRef.current = setInterval(() => {
        setElapsed((prev) => {
          const next = prev + 1;
          if (next >= 5 && next < 15) setProgressStage("Analyse en cours...");
          else if (next >= 15) setProgressStage("Traitement des donnees...");
          return next;
        });
      }, 1000);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
      timerRef.current = null;
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [loading]);

  const totalSize = files.reduce((sum, f) => sum + f.size, 0);

  const addFiles = (newFiles: File[]) => {
    const pdfs = newFiles.filter((f) => f.name.toLowerCase().endsWith(".pdf"));
    if (pdfs.length === 0) return;
    const extracted = pdfs.map((f) => {
      const m = f.name.match(/\d+/);
      return m ? m[0] : "";
    });
    setFiles((prev) => [...prev, ...pdfs]);
    setCommandes((prev) => [...prev, ...extracted]);
  };

  const removeFile = (idx: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== idx));
    setCommandes((prev) => prev.filter((_, i) => i !== idx));
  };

  const removeAllFiles = () => {
    setFiles([]);
    setCommandes([]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (files.length === 0) return;
    setLoading(true);
    setError("");
    try {
      const data = await uploadPDFs({
        files,
        semaine_prod: semaine,
        annee_prod: annee,
        commande_client: commandes,
      });
      onResults(data);
    } catch (err: any) {
      if (err.message === "AUTH") {
        setError("Session expiree, reconnectez-vous");
      } else {
        setError(err.message || "Erreur lors du traitement");
      }
    } finally {
      setLoading(false);
    }
  };

  const navItems = [
    { label: "Traitement", id: "upload", onClick: () => {} },
    { label: "Historique", id: "files", onClick: onFiles },
    { label: "Parametres", id: "settings", onClick: onSettings },
    ...(onReleaseNotes ? [{ label: "Nouveautes", id: "release-notes", onClick: onReleaseNotes }] : []),
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header currentPage="upload" navItems={navItems} onLogout={onLogout} />

      <main className="max-w-4xl mx-auto px-4 py-8 flex-1 w-full">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Drop zone */}
          <div
            className={`border-2 border-dashed rounded-2xl p-8 sm:p-12 text-center cursor-pointer transition-all ${
              dragOver
                ? "border-brand-500 bg-brand-50 scale-[1.01]"
                : "border-gray-200 bg-white hover:border-brand-300 hover:bg-brand-50/30"
            }`}
            onDragOver={(e) => {
              e.preventDefault();
              setDragOver(true);
            }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(e) => {
              e.preventDefault();
              setDragOver(false);
              addFiles(Array.from(e.dataTransfer.files));
            }}
            onClick={() => inputRef.current?.click()}
          >
            <input
              ref={inputRef}
              type="file"
              multiple
              accept=".pdf"
              className="hidden"
              onChange={(e) => addFiles(Array.from(e.target.files || []))}
            />
            {/* Upload icon */}
            <div className="mx-auto w-12 h-12 rounded-full bg-brand-50 flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-brand-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
              </svg>
            </div>
            <p className="text-gray-600 font-medium">
              Glissez vos fichiers PDF ici
            </p>
            <p className="text-sm text-gray-400 mt-1">
              ou cliquez pour parcourir
            </p>
          </div>

          {/* File list */}
          {files.length > 0 && (
            <div className="bg-white rounded-xl border border-gray-200 p-4 space-y-3">
              <div className="flex items-center justify-between">
                <h2 className="font-semibold text-gray-700">
                  Fichiers ({files.length})
                  <span className="ml-2 text-sm font-normal text-gray-400">
                    {formatSize(totalSize)}
                  </span>
                </h2>
                <button
                  type="button"
                  onClick={removeAllFiles}
                  className="text-sm text-red-500 hover:text-red-700"
                >
                  Tout retirer
                </button>
              </div>
              {files.map((f, i) => (
                <div
                  key={i}
                  className="flex items-center gap-3 border-b border-gray-50 pb-2 last:border-0"
                >
                  {/* PDF icon */}
                  <div className="w-8 h-8 rounded-lg bg-red-50 flex items-center justify-center flex-shrink-0">
                    <svg className="w-4 h-4 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0">
                    <span className="text-sm text-gray-700 truncate block">
                      {f.name}
                    </span>
                    <span className="text-xs text-gray-400">
                      {formatSize(f.size)}
                    </span>
                  </div>
                  <input
                    type="text"
                    placeholder="N° commande"
                    value={commandes[i] || ""}
                    onChange={(e) => {
                      const next = [...commandes];
                      next[i] = e.target.value;
                      setCommandes(next);
                    }}
                    className="border border-gray-200 rounded-lg px-3 py-1.5 text-sm w-28 sm:w-40 focus:outline-none focus:ring-2 focus:ring-brand-600 focus:border-transparent"
                  />
                  <button
                    type="button"
                    onClick={() => removeFile(i)}
                    className="text-gray-300 hover:text-red-500 p-1"
                    title="Supprimer"
                  >
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              ))}
            </div>
          )}

          {/* Production week */}
          <div className="bg-white rounded-xl border border-gray-200 p-4 grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-600 mb-1">
                Semaine de production
              </label>
              <input
                type="number"
                min={1}
                max={53}
                value={semaine}
                onChange={(e) => setSemaine(Number(e.target.value))}
                className="w-full border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand-600 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-600 mb-1">
                Annee
              </label>
              <input
                type="number"
                min={2020}
                max={2040}
                value={annee}
                onChange={(e) => setAnnee(Number(e.target.value))}
                className="w-full border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand-600 focus:border-transparent"
              />
            </div>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm">
              {error}
            </div>
          )}

          {/* Recap before submit */}
          {files.length > 0 && !loading && (
            <div className="bg-brand-50 border border-brand-200 rounded-xl px-4 py-3 text-sm text-brand-800">
              {files.length} fichier{files.length > 1 ? "s" : ""} ({formatSize(totalSize)})
              {" - "}Semaine {semaine}/{annee}
              {commandes.filter(Boolean).length > 0 && (
                <> - Commandes : {commandes.filter(Boolean).join(", ")}</>
              )}
            </div>
          )}

          {/* Progress bar during processing */}
          {loading && (
            <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-3">
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-brand-600 animate-pulse" />
                  <span className="text-gray-700 font-medium">{progressStage}</span>
                </div>
                <span className="text-gray-400 tabular-nums">{elapsed}s</span>
              </div>
              <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                <div className="bg-brand-600 h-2 rounded-full progress-bar" />
              </div>
              <style>{`
                .progress-bar {
                  animation: indeterminate 1.5s ease-in-out infinite;
                }
                @keyframes indeterminate {
                  0% { transform: translateX(-100%); width: 40%; }
                  50% { transform: translateX(60%); width: 40%; }
                  100% { transform: translateX(200%); width: 40%; }
                }
              `}</style>
            </div>
          )}

          <button
            type="submit"
            disabled={loading || files.length === 0}
            className="w-full bg-brand-600 text-white py-3 rounded-xl text-lg font-semibold hover:bg-brand-700 disabled:opacity-40 disabled:cursor-not-allowed shadow-sm"
          >
            {loading ? "Traitement en cours..." : "Traiter les fichiers"}
          </button>
        </form>
      </main>

      <Footer />
    </div>
  );
}
