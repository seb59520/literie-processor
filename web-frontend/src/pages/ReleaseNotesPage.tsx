import { useEffect, useState } from "react";
import { getReleaseNotes } from "../api";
import Header from "../components/Header";
import Footer from "../components/Footer";

interface Props {
  onBack: () => void;
  onLogout: () => void;
}

function markdownToHtml(md: string): string {
  return md
    .replace(/^## (.+)$/gm, '<h2 class="text-base font-semibold text-gray-800 mt-6 mb-2 pb-1 border-b border-gray-100">$1</h2>')
    .replace(/^# (.+)$/gm, '<h1 class="text-lg font-bold text-gray-900 mb-4">$1</h1>')
    .replace(/^---$/gm, '<hr class="my-4 border-gray-100" />')
    .replace(/^- (.+)$/gm, '<li class="text-sm text-gray-600 ml-4 list-disc">$1</li>')
    .replace(/\n/g, "\n");
}

export default function ReleaseNotesPage({ onBack, onLogout }: Props) {
  const [content, setContent] = useState("");
  const [version, setVersion] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const data = await getReleaseNotes();
        setContent(data.content);
        setVersion(data.version);
      } catch (e: any) {
        setError(e.message || "Impossible de charger les notes de version");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const navItems = [
    { label: "Traitement", id: "upload", onClick: onBack },
    { label: "Notes de version", id: "release-notes", onClick: () => {} },
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header currentPage="release-notes" navItems={navItems} onLogout={onLogout} />

      <main className="max-w-4xl mx-auto px-4 py-8 flex-1 w-full">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-gray-800">Notes de version</h2>
          {version && (
            <span className="text-xs bg-brand-50 text-brand-700 px-3 py-1 rounded-full font-medium">
              v{version}
            </span>
          )}
        </div>

        {loading && (
          <div className="text-center text-gray-400 py-12">Chargement...</div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm">
            {error}
          </div>
        )}

        {!loading && !error && content && (
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <div
              className="prose prose-sm max-w-none"
              dangerouslySetInnerHTML={{ __html: markdownToHtml(content) }}
            />
          </div>
        )}

        {!loading && !error && !content && (
          <div className="text-center text-gray-400 py-12">
            Aucune note de version disponible.
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}
