import { useEffect, useState } from "react";
import { getSettings, updateSettings } from "../api";
import Header from "../components/Header";
import Footer from "../components/Footer";

interface Props {
  onBack: () => void;
  onLogout: () => void;
}

export default function SettingsPage({ onBack, onLogout }: Props) {
  const [outputDir, setOutputDir] = useState("");
  const [savedDir, setSavedDir] = useState("");
  const [noyauOrder, setNoyauOrder] = useState<string[]>([]);
  const [savedNoyauOrder, setSavedNoyauOrder] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const data = await getSettings();
        setOutputDir(data.excel_output_directory);
        setSavedDir(data.excel_output_directory);
        setNoyauOrder(data.noyau_order || []);
        setSavedNoyauOrder(data.noyau_order || []);
      } catch (e: any) {
        setError(e.message || "Erreur de chargement");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const handleSave = async () => {
    setSaving(true);
    setError("");
    setSuccess("");
    try {
      const payload: Record<string, any> = {};
      if (outputDir !== savedDir) payload.excel_output_directory = outputDir;
      if (JSON.stringify(noyauOrder) !== JSON.stringify(savedNoyauOrder))
        payload.noyau_order = noyauOrder;

      const data = await updateSettings(payload);
      setSavedDir(data.excel_output_directory);
      setOutputDir(data.excel_output_directory);
      setSavedNoyauOrder(data.noyau_order || []);
      setNoyauOrder(data.noyau_order || []);
      setSuccess("Parametres enregistres");
      setTimeout(() => setSuccess(""), 3000);
    } catch (e: any) {
      setError(e.message || "Erreur lors de la sauvegarde");
    } finally {
      setSaving(false);
    }
  };

  const moveNoyau = (idx: number, dir: -1 | 1) => {
    const next = [...noyauOrder];
    const target = idx + dir;
    if (target < 0 || target >= next.length) return;
    [next[idx], next[target]] = [next[target], next[idx]];
    setNoyauOrder(next);
  };

  const removeNoyau = (idx: number) => {
    setNoyauOrder((prev) => prev.filter((_, i) => i !== idx));
  };

  const addNoyau = (name: string) => {
    if (!name.trim()) return;
    setNoyauOrder((prev) => [...prev, name.trim().toUpperCase()]);
  };

  const hasChanges =
    outputDir !== savedDir ||
    JSON.stringify(noyauOrder) !== JSON.stringify(savedNoyauOrder);

  const navItems = [
    { label: "Traitement", id: "upload", onClick: onBack },
    { label: "Parametres", id: "settings", onClick: () => {} },
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header currentPage="settings" navItems={navItems} onLogout={onLogout} />

      <main className="max-w-4xl mx-auto px-4 py-8 space-y-6 flex-1 w-full">
        <h2 className="text-lg font-semibold text-gray-800">Parametres</h2>

        {loading && (
          <div className="text-center text-gray-400 py-12">Chargement...</div>
        )}

        {!loading && (
          <>
            {/* Repertoire Excel */}
            <div className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Repertoire de sortie des fichiers Excel
                </label>
                <input
                  type="text"
                  value={outputDir}
                  onChange={(e) => setOutputDir(e.target.value)}
                  placeholder="/chemin/vers/le/repertoire"
                  className="w-full border border-gray-200 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-600 focus:border-transparent"
                />
                <p className="text-xs text-gray-400 mt-1">
                  Chemin absolu sur le serveur ou les fichiers Excel seront enregistres
                </p>
              </div>
            </div>

            {/* Ordre des noyaux */}
            <div className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Ordre d'inscription des noyaux dans le fichier Excel
                </label>
                <p className="text-xs text-gray-400 mb-3">
                  Les matelas seront inscrits dans cet ordre dans le fichier Excel.
                  Utilisez les fleches pour reorganiser.
                </p>

                {noyauOrder.length === 0 && (
                  <p className="text-sm text-orange-500 mb-3">
                    Aucun ordre defini — les matelas seront inscrits dans l'ordre de detection.
                  </p>
                )}

                <div className="space-y-1">
                  {noyauOrder.map((noyau, idx) => (
                    <div
                      key={idx}
                      className="flex items-center gap-2 bg-gray-50 rounded-lg px-3 py-2"
                    >
                      <span className="text-xs text-gray-400 w-5 text-right">
                        {idx + 1}.
                      </span>
                      <span className="flex-1 text-sm text-gray-800">{noyau}</span>
                      <button
                        onClick={() => moveNoyau(idx, -1)}
                        disabled={idx === 0}
                        className="text-gray-400 hover:text-brand-600 disabled:opacity-30 text-sm px-1"
                        title="Monter"
                      >
                        &uarr;
                      </button>
                      <button
                        onClick={() => moveNoyau(idx, 1)}
                        disabled={idx === noyauOrder.length - 1}
                        className="text-gray-400 hover:text-brand-600 disabled:opacity-30 text-sm px-1"
                        title="Descendre"
                      >
                        &darr;
                      </button>
                      <button
                        onClick={() => removeNoyau(idx)}
                        className="text-gray-400 hover:text-red-500 text-sm px-1"
                        title="Supprimer"
                      >
                        &times;
                      </button>
                    </div>
                  ))}
                </div>

                <AddNoyauInput onAdd={addNoyau} existing={noyauOrder} />
              </div>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded-xl text-sm">
                {error}
              </div>
            )}

            {success && (
              <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-2 rounded-xl text-sm">
                {success}
              </div>
            )}

            <button
              onClick={handleSave}
              disabled={saving || !hasChanges}
              className="bg-brand-600 text-white px-6 py-2.5 rounded-xl text-sm font-medium hover:bg-brand-700 disabled:opacity-40 disabled:cursor-not-allowed shadow-sm"
            >
              {saving ? "Enregistrement..." : "Enregistrer"}
            </button>
          </>
        )}
      </main>

      <Footer />
    </div>
  );
}

const KNOWN_NOYAUX = [
  "LATEX NATUREL",
  "MOUSSE VISCO",
  "LATEX MIXTE 7 ZONES",
  "MOUSSE RAINUREE 7 ZONES",
  "LATEX RENFORCE",
  "SELECT 43",
];

function AddNoyauInput({
  onAdd,
  existing,
}: {
  onAdd: (name: string) => void;
  existing: string[];
}) {
  const [value, setValue] = useState("");
  const available = KNOWN_NOYAUX.filter((n) => !existing.includes(n));

  return (
    <div className="flex gap-2 mt-3">
      {available.length > 0 ? (
        <select
          value={value}
          onChange={(e) => setValue(e.target.value)}
          className="flex-1 border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-brand-600 focus:border-transparent"
        >
          <option value="">Ajouter un noyau...</option>
          {available.map((n) => (
            <option key={n} value={n}>
              {n}
            </option>
          ))}
        </select>
      ) : (
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Nom du noyau"
          className="flex-1 border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-brand-600 focus:border-transparent"
        />
      )}
      <button
        onClick={() => {
          onAdd(value);
          setValue("");
        }}
        disabled={!value.trim()}
        className="bg-gray-100 text-gray-700 px-4 py-1.5 rounded-lg text-sm font-medium hover:bg-gray-200 disabled:opacity-40"
      >
        Ajouter
      </button>
    </div>
  );
}
