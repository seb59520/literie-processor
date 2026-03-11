import { useEffect, useState } from "react";
import { listFiles, downloadFile, deleteFile } from "../api";
import ExcelPreview from "../components/ExcelPreview";
import Header from "../components/Header";
import Footer from "../components/Footer";

interface FileInfo {
  name: string;
  size: number;
  modified: number;
}

interface Props {
  onBack: () => void;
  onLogout: () => void;
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} o`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} Ko`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} Mo`;
}

function formatDate(ts: number): string {
  const d = new Date(ts * 1000);
  return d.toLocaleDateString("fr-FR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function isMatelas(name: string): boolean {
  return name.toLowerCase().startsWith("matelas");
}

function isSommier(name: string): boolean {
  return name.toLowerCase().startsWith("sommier");
}

function FileCard({
  file,
  onPreview,
  onDownload,
  onDelete,
}: {
  file: FileInfo;
  onPreview: () => void;
  onDownload: () => void;
  onDelete: () => void;
}) {
  return (
    <div className="bg-white border border-gray-100 rounded-xl p-3 hover:border-gray-200 hover:shadow-sm transition-all">
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 rounded-lg bg-green-50 flex items-center justify-center flex-shrink-0 mt-0.5">
          <svg className="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
          </svg>
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm text-gray-800 truncate font-medium" title={file.name}>
            {file.name}
          </p>
          <p className="text-xs text-gray-400 mt-0.5">
            {formatSize(file.size)} &middot; {formatDate(file.modified)}
          </p>
        </div>
      </div>
      <div className="flex gap-1.5 mt-3">
        <button
          onClick={onPreview}
          className="bg-brand-600 text-white px-3 py-1 rounded-lg text-xs font-medium hover:bg-brand-700"
        >
          Apercu
        </button>
        <button
          onClick={onDownload}
          className="bg-green-600 text-white px-3 py-1 rounded-lg text-xs font-medium hover:bg-green-700"
        >
          Telecharger
        </button>
        <button
          onClick={onDelete}
          className="text-gray-400 hover:text-red-600 hover:bg-red-50 px-3 py-1 rounded-lg text-xs font-medium"
        >
          Supprimer
        </button>
      </div>
    </div>
  );
}

export default function FilesPage({ onBack, onLogout }: Props) {
  const [files, setFiles] = useState<FileInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [previewFile, setPreviewFile] = useState<string | null>(null);
  const [search, setSearch] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const data = await listFiles();
        const sorted = (data.files as FileInfo[]).sort(
          (a, b) => b.modified - a.modified
        );
        setFiles(sorted);
      } catch (e: any) {
        setError(e.message || "Erreur de chargement");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const handleDelete = async (name: string) => {
    if (!confirm(`Supprimer ${name} ?`)) return;
    try {
      await deleteFile(name);
      setFiles((prev) => prev.filter((f) => f.name !== name));
    } catch (e: any) {
      setError(e.message || "Erreur lors de la suppression");
    }
  };

  const filtered = search
    ? files.filter((f) => f.name.toLowerCase().includes(search.toLowerCase()))
    : files;

  const matelasFiles = filtered.filter((f) => isMatelas(f.name));
  const sommierFiles = filtered.filter((f) => isSommier(f.name));
  const autresFiles = filtered.filter(
    (f) => !isMatelas(f.name) && !isSommier(f.name)
  );

  const navItems = [
    { label: "Traitement", id: "upload", onClick: onBack },
    { label: "Historique", id: "files", onClick: () => {} },
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header currentPage="files" navItems={navItems} onLogout={onLogout} />

      <main className="max-w-6xl mx-auto px-4 py-8 space-y-5 flex-1 w-full">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-800">
            Historique des fichiers Excel
          </h2>
          <span className="text-sm text-gray-400">
            {filtered.length} fichier{filtered.length !== 1 ? "s" : ""}
          </span>
        </div>

        <div className="relative">
          <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            placeholder="Rechercher un fichier..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full border border-gray-200 rounded-xl pl-10 pr-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-brand-600 focus:border-transparent"
          />
        </div>

        {loading && (
          <div className="text-center text-gray-400 py-12">Chargement...</div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm">
            {error}
          </div>
        )}

        {!loading && !error && filtered.length === 0 && (
          <div className="text-center text-gray-400 py-16">
            <svg className="w-12 h-12 text-gray-200 mx-auto mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
            </svg>
            <p>{search ? "Aucun fichier correspondant" : "Aucun fichier disponible"}</p>
          </div>
        )}

        {!loading && !error && filtered.length > 0 && (
          <>
            {/* Two-column layout */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Matelas column */}
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold text-gray-700">Matelas</h3>
                  <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full font-medium">
                    {matelasFiles.length}
                  </span>
                </div>
                {matelasFiles.length === 0 ? (
                  <p className="text-sm text-gray-400 py-6 text-center bg-white rounded-xl border border-dashed border-gray-200">
                    Aucun fichier matelas
                  </p>
                ) : (
                  <div className="space-y-2">
                    {matelasFiles.map((f) => (
                      <FileCard
                        key={f.name}
                        file={f}
                        onPreview={() => setPreviewFile(f.name)}
                        onDownload={() => downloadFile(f.name)}
                        onDelete={() => handleDelete(f.name)}
                      />
                    ))}
                  </div>
                )}
              </div>

              {/* Sommiers column */}
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold text-gray-700">Sommiers</h3>
                  <span className="text-xs bg-brand-100 text-brand-700 px-2 py-0.5 rounded-full font-medium">
                    {sommierFiles.length}
                  </span>
                </div>
                {sommierFiles.length === 0 ? (
                  <p className="text-sm text-gray-400 py-6 text-center bg-white rounded-xl border border-dashed border-gray-200">
                    Aucun fichier sommier
                  </p>
                ) : (
                  <div className="space-y-2">
                    {sommierFiles.map((f) => (
                      <FileCard
                        key={f.name}
                        file={f}
                        onPreview={() => setPreviewFile(f.name)}
                        onDownload={() => downloadFile(f.name)}
                        onDelete={() => handleDelete(f.name)}
                      />
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Other files */}
            {autresFiles.length > 0 && (
              <div className="space-y-3 mt-4">
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold text-gray-700">Autres</h3>
                  <span className="text-xs bg-gray-200 text-gray-600 px-2 py-0.5 rounded-full font-medium">
                    {autresFiles.length}
                  </span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {autresFiles.map((f) => (
                    <FileCard
                      key={f.name}
                      file={f}
                      onPreview={() => setPreviewFile(f.name)}
                      onDownload={() => downloadFile(f.name)}
                      onDelete={() => handleDelete(f.name)}
                    />
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </main>

      <Footer />

      {previewFile && (
        <ExcelPreview
          filename={previewFile}
          onClose={() => setPreviewFile(null)}
        />
      )}
    </div>
  );
}
