export default function Footer() {
  return (
    <footer className="border-t border-gray-100 mt-auto">
      <div className="max-w-6xl mx-auto px-4 py-4 flex flex-col sm:flex-row justify-between items-center gap-2 text-xs text-gray-400">
        <span>Westelynck &middot; Literie Processor v3.12</span>
        <span>&copy; {new Date().getFullYear()} Tous droits reserves</span>
      </div>
    </footer>
  );
}
