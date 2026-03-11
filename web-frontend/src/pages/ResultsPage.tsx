import { useState } from "react";
import { downloadFile } from "../api";
import ExcelPreview from "../components/ExcelPreview";
import Header from "../components/Header";
import Footer from "../components/Footer";

interface Props {
  data: any;
  onBack: () => void;
  onLogout: () => void;
}

export default function ResultsPage({ data, onBack, onLogout }: Props) {
  const [previewFile, setPreviewFile] = useState<string | null>(null);
  const [showDetails, setShowDetails] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const results = data.results || [];
  const excelFiles = data.fichiers_excel || [];
  const errors = data.errors || [];

  const downloadAll = async () => {
    setDownloading(true);
    for (const filepath of excelFiles) {
      const filename =
        filepath.split("/").pop() || filepath.split("\\").pop() || filepath;
      await downloadFile(filename);
    }
    setDownloading(false);
  };

  const navItems = [
    { label: "Nouveau traitement", id: "upload", onClick: onBack },
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header currentPage="results" navItems={navItems} onLogout={onLogout} />

      <main className="max-w-4xl mx-auto px-4 py-8 space-y-6 flex-1 w-full">
        {/* Summary */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            Resultats du traitement
          </h2>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div className="bg-green-50 rounded-xl p-4">
              <div className="text-2xl font-bold text-green-600">
                {data.successful_files || 0}
              </div>
              <div className="text-sm text-gray-500">Fichiers traites</div>
            </div>
            <div className="bg-blue-50 rounded-xl p-4">
              <div className="text-2xl font-bold text-blue-600">
                {data.total_pre_imports || 0}
              </div>
              <div className="text-sm text-gray-500">Articles detectes</div>
            </div>
            <div className="bg-brand-50 rounded-xl p-4">
              <div className="text-2xl font-bold text-brand-600">
                {excelFiles.length}
              </div>
              <div className="text-sm text-gray-500">Fichiers Excel</div>
            </div>
          </div>
          {data.total_processing_time && (
            <p className="text-xs text-gray-400 mt-3 text-right">
              Traite en {data.total_processing_time.toFixed(1)}s
            </p>
          )}
        </div>

        {/* Excel download - priority position */}
        {excelFiles.length > 0 && (
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-800">
                Fichiers Excel generes
              </h2>
              {excelFiles.length > 1 && (
                <button
                  onClick={downloadAll}
                  disabled={downloading}
                  className="bg-green-600 text-white px-4 py-1.5 rounded-lg text-sm font-medium hover:bg-green-700 disabled:opacity-50"
                >
                  {downloading ? "Telechargement..." : "Tout telecharger"}
                </button>
              )}
            </div>
            <div className="space-y-2">
              {excelFiles.map((filepath: string, i: number) => {
                const filename =
                  filepath.split("/").pop() || filepath.split("\\").pop() || filepath;
                return (
                  <div
                    key={i}
                    className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                  >
                    <div className="flex items-center gap-3 min-w-0">
                      <div className="w-8 h-8 rounded-lg bg-green-100 flex items-center justify-center flex-shrink-0">
                        <svg className="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <span className="text-sm text-gray-700 truncate">{filename}</span>
                    </div>
                    <div className="flex gap-2 flex-shrink-0">
                      <button
                        onClick={() => setPreviewFile(filename)}
                        className="bg-brand-600 text-white px-4 py-1.5 rounded-lg text-sm hover:bg-brand-700"
                      >
                        Apercu
                      </button>
                      <button
                        onClick={() => downloadFile(filename)}
                        className="bg-green-600 text-white px-4 py-1.5 rounded-lg text-sm hover:bg-green-700"
                      >
                        Telecharger
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Errors */}
        {errors.length > 0 && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-4">
            <h3 className="font-semibold text-red-700 mb-2">Erreurs</h3>
            {errors.map((err: string, i: number) => (
              <p key={i} className="text-sm text-red-600">
                {err}
              </p>
            ))}
          </div>
        )}

        {/* Toggle details */}
        {results.length > 0 && (
          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowDetails(!showDetails)}
              className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-800"
            >
              <span
                className={`inline-block w-9 h-5 rounded-full relative transition-colors ${
                  showDetails ? "bg-brand-600" : "bg-gray-300"
                }`}
              >
                <span
                  className={`absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow transition-transform ${
                    showDetails ? "translate-x-4" : ""
                  }`}
                />
              </span>
              Afficher le detail des fichiers traites
            </button>
          </div>
        )}

        {/* Per-file details */}
        {showDetails &&
          results.map((r: any, i: number) => (
            <div key={i} className="bg-white rounded-xl border border-gray-200 p-4">
              <h3 className="font-semibold text-gray-700 mb-3">
                {r.filename || r.file}
                {r.status === "success" ? (
                  <span className="ml-2 text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full">
                    OK
                  </span>
                ) : (
                  <span className="ml-2 text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded-full">
                    Erreur
                  </span>
                )}
              </h3>
              {r.error && (
                <p className="text-sm text-red-500 mb-2">{r.error}</p>
              )}
              {r.extraction_stats && (
                <p className="text-xs text-gray-500">
                  {r.extraction_stats.nb_caracteres} caracteres,{" "}
                  {r.extraction_stats.nb_mots} mots
                </p>
              )}

              {/* Mattress configs */}
              {r.configurations_matelas?.length > 0 && (
                <div className="mt-3">
                  <h4 className="text-sm font-medium text-gray-600 mb-2">
                    Matelas ({r.configurations_matelas.length})
                  </h4>
                  <div className="overflow-x-auto">
                    <table className="text-xs w-full border-collapse">
                      <thead>
                        <tr className="bg-gray-50 text-left">
                          <th className="px-2 py-1.5 border border-gray-200">#</th>
                          <th className="px-2 py-1.5 border border-gray-200">Noyau</th>
                          <th className="px-2 py-1.5 border border-gray-200">Dimensions</th>
                          <th className="px-2 py-1.5 border border-gray-200">Fermete</th>
                          <th className="px-2 py-1.5 border border-gray-200">Housse</th>
                          <th className="px-2 py-1.5 border border-gray-200">Matiere</th>
                        </tr>
                      </thead>
                      <tbody>
                        {r.configurations_matelas.map(
                          (cfg: any, j: number) => (
                            <tr key={j} className="hover:bg-gray-50">
                              <td className="px-2 py-1.5 border border-gray-200">{cfg.matelas_index}</td>
                              <td className="px-2 py-1.5 border border-gray-200">{cfg.noyau}</td>
                              <td className="px-2 py-1.5 border border-gray-200">{cfg.dimension_literie || "-"}</td>
                              <td className="px-2 py-1.5 border border-gray-200">{cfg.fermete}</td>
                              <td className="px-2 py-1.5 border border-gray-200">{cfg.housse}</td>
                              <td className="px-2 py-1.5 border border-gray-200">{cfg.matiere_housse}</td>
                            </tr>
                          )
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Sommier configs */}
              {r.configurations_sommiers?.length > 0 && (
                <div className="mt-3">
                  <h4 className="text-sm font-medium text-gray-600 mb-2">
                    Sommiers ({r.configurations_sommiers.length})
                  </h4>
                  <div className="overflow-x-auto">
                    <table className="text-xs w-full border-collapse">
                      <thead>
                        <tr className="bg-gray-50 text-left">
                          <th className="px-2 py-1.5 border border-gray-200">#</th>
                          <th className="px-2 py-1.5 border border-gray-200">Type</th>
                          <th className="px-2 py-1.5 border border-gray-200">Dimensions</th>
                          <th className="px-2 py-1.5 border border-gray-200">Materiau</th>
                        </tr>
                      </thead>
                      <tbody>
                        {r.configurations_sommiers.map(
                          (cfg: any, j: number) => (
                            <tr key={j} className="hover:bg-gray-50">
                              <td className="px-2 py-1.5 border border-gray-200">{cfg.sommier_index}</td>
                              <td className="px-2 py-1.5 border border-gray-200">{cfg.type_sommier}</td>
                              <td className="px-2 py-1.5 border border-gray-200">{cfg.dimension_sommier || "-"}</td>
                              <td className="px-2 py-1.5 border border-gray-200">{cfg.materiau}</td>
                            </tr>
                          )
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Client info */}
              {r.donnees_client?.nom && (
                <div className="mt-3 text-xs text-gray-600">
                  <span className="font-medium">Client:</span>{" "}
                  {r.donnees_client.nom}
                  {r.donnees_client.adresse &&
                    ` - ${r.donnees_client.adresse}`}
                </div>
              )}
            </div>
          ))}
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
