import { useState } from "react";
import { authCheck } from "../api";

interface Props {
  onLogin: () => void;
}

export default function LoginPage({ onLogin }: Props) {
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    localStorage.setItem("auth_password", password);
    try {
      await authCheck();
      onLogin();
    } catch {
      setError("Mot de passe incorrect ou serveur inaccessible");
      localStorage.removeItem("auth_password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-200">
      <div className="w-full max-w-sm">
        <form
          onSubmit={handleSubmit}
          className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100"
        >
          {/* Logo */}
          <div className="flex justify-center mb-6">
            <img
              src="/logo_westelynck.svg"
              alt="Westelynck"
              className="h-14 w-auto"
            />
          </div>

          <h1 className="text-xl font-bold mb-1 text-center text-gray-800">
            Literie Processor
          </h1>
          <p className="text-sm text-gray-400 mb-6 text-center">
            Traitement de devis literie
          </p>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-600 mb-1">
                Mot de passe
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Entrez votre mot de passe"
                className="w-full border border-gray-200 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-brand-600 focus:border-transparent"
                autoFocus
              />
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-600 text-sm px-3 py-2 rounded-lg">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !password}
              className="w-full bg-brand-600 text-white py-2.5 rounded-lg font-medium hover:bg-brand-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Connexion..." : "Se connecter"}
            </button>
          </div>
        </form>

        <p className="text-xs text-gray-400 text-center mt-4">
          Westelynck &middot; Literie Processor
        </p>
      </div>
    </div>
  );
}
