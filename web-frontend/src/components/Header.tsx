interface NavItem {
  label: string;
  id: string;
  onClick: () => void;
}

interface Props {
  currentPage: string;
  navItems: NavItem[];
  onLogout: () => void;
}

export default function Header({ currentPage, navItems, onLogout }: Props) {
  return (
    <header className="bg-white border-b border-gray-200">
      <div className="max-w-6xl mx-auto px-4 py-3 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <img
            src="/logo_westelynck.svg"
            alt="Westelynck"
            className="h-8 w-auto"
          />
          <div className="h-6 w-px bg-gray-200 hidden sm:block" />
          <span className="text-sm font-semibold text-gray-700 hidden sm:block">
            Literie Processor
          </span>
        </div>

        {/* Navigation */}
        <nav className="flex items-center gap-1 flex-wrap">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={item.onClick}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                currentPage === item.id
                  ? "bg-brand-50 text-brand-700"
                  : "text-gray-500 hover:text-gray-800 hover:bg-gray-100"
              }`}
            >
              {item.label}
            </button>
          ))}
          <div className="h-5 w-px bg-gray-200 mx-1" />
          <button
            onClick={onLogout}
            className="px-3 py-1.5 rounded-lg text-sm text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors"
          >
            Deconnexion
          </button>
        </nav>
      </div>
    </header>
  );
}
