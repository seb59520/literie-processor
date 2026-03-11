import { useEffect, useState } from "react";
import * as XLSX from "xlsx";
import { fetchFileBuffer, downloadFile } from "../api";

interface Props {
  filename: string;
  onClose: () => void;
}

type SheetData = (string | number | boolean | null)[][];

export default function ExcelPreview({ filename, onClose }: Props) {
  const [sheets, setSheets] = useState<Record<string, SheetData>>({});
  const [sheetNames, setSheetNames] = useState<string[]>([]);
  const [activeSheet, setActiveSheet] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const buffer = await fetchFileBuffer(filename);
        if (cancelled) return;
        const wb = XLSX.read(buffer, { type: "array" });
        const parsed: Record<string, SheetData> = {};
        for (const name of wb.SheetNames) {
          parsed[name] = XLSX.utils.sheet_to_json<(string | number | boolean | null)[]>(
            wb.Sheets[name],
            { header: 1, defval: null }
          );
        }
        setSheets(parsed);
        setSheetNames(wb.SheetNames);
        setActiveSheet(wb.SheetNames[0] || "");
      } catch (e: any) {
        if (!cancelled) setError(e.message || "Erreur de chargement");
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [filename]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  const rows = sheets[activeSheet] || [];

  return (
    <div className="fixed inset-0 z-50 flex flex-col bg-black/50" onClick={onClose}>
      <div
        className="m-4 flex flex-col flex-1 bg-white rounded-lg shadow-xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b bg-gray-50">
          <h2 className="text-sm font-semibold text-gray-800 truncate">
            {filename}
          </h2>
          <div className="flex gap-2 shrink-0">
            <button
              onClick={() => downloadFile(filename)}
              className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700"
            >
              Telecharger
            </button>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-800 text-xl leading-none px-2"
            >
              &times;
            </button>
          </div>
        </div>

        {/* Sheet tabs */}
        {sheetNames.length > 1 && (
          <div className="flex border-b bg-gray-50 px-2 gap-1 overflow-x-auto">
            {sheetNames.map((name) => (
              <button
                key={name}
                onClick={() => setActiveSheet(name)}
                className={`px-3 py-1.5 text-xs font-medium border-b-2 whitespace-nowrap ${
                  name === activeSheet
                    ? "border-blue-600 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700"
                }`}
              >
                {name}
              </button>
            ))}
          </div>
        )}

        {/* Content */}
        <div className="flex-1 overflow-auto p-2">
          {loading && (
            <div className="flex items-center justify-center h-full text-gray-500">
              Chargement...
            </div>
          )}
          {error && (
            <div className="flex items-center justify-center h-full text-red-500">
              {error}
            </div>
          )}
          {!loading && !error && rows.length === 0 && (
            <div className="flex items-center justify-center h-full text-gray-400">
              Feuille vide
            </div>
          )}
          {!loading && !error && rows.length > 0 && (
            <table className="text-xs border-collapse w-full">
              <tbody>
                {rows.map((row, ri) => (
                  <tr key={ri}>
                    <td className="px-1 py-0.5 border border-gray-200 bg-gray-50 text-gray-400 text-right select-none w-8">
                      {ri + 1}
                    </td>
                    {row.map((cell, ci) => {
                      const filled = cell !== null && cell !== undefined && cell !== "";
                      return (
                        <td
                          key={ci}
                          className={`px-1.5 py-0.5 border border-gray-200 whitespace-nowrap ${
                            filled ? "bg-blue-50" : ""
                          }`}
                        >
                          {cell != null ? String(cell) : ""}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}
