import { Link, useNavigate, useLocation } from "react-router-dom";

function getPayload() {
  const token = localStorage.getItem("token");
  if (!token) return null;
  try { return JSON.parse(atob(token.split(".")[1])); } catch { return null; }
}

export default function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  const payload = getPayload();
  const role = payload?.role;

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  let navItems = [];
  
  if (role === "ADMIN") {
    navItems = [
      { path: "/admin?tab=dashboard", match: "?tab=dashboard", exactMatch: "/admin", label: "Dashboard", icon: "📊" },
      { path: "/admin?tab=scholarships", match: "?tab=scholarships", label: "Scholarships", icon: "🎓" },
      { path: "/admin?tab=applications", match: "?tab=applications", label: "Applications", icon: "📄" },
      { path: "/admin?tab=users", match: "?tab=users", label: "All Users", icon: "👥" },
      { path: "/admin?tab=decisions", match: "?tab=decisions", label: "Decisions List", icon: "✅" },
      { path: "/admin?tab=reviewers", match: "?tab=reviewers", label: "Pending Reviewers", icon: "⏳" },
    ];
  } else if (role === "STUDENT") {
    navItems = [
      { path: "/scholarships", match: "/scholarships", label: "Discover Scholarships", icon: "🔍" },
      { path: "/my-applications", match: "/my-applications", label: "My Applications", icon: "📄" },
      { path: "/profile", match: "/profile", label: "My Profile", icon: "👤" },
    ];
  } else if (role === "REVIEWER") {
    navItems = [
      { path: "/reviewer?tab=assigned", match: "?tab=assigned", exactMatch: "/reviewer", label: "Assigned Applications", icon: "📄" },
      { path: "/reviewer?tab=scoring", match: "?tab=scoring", label: "Scoring Form", icon: "⭐" },
      { path: "/reviewer?tab=decisions", match: "?tab=decisions", label: "Decision Records", icon: "✅" },
    ];
  }

  const currentPath = location.pathname + location.search;
  
  const isActive = (item) => {
    if (role === "ADMIN") {
       return currentPath.includes(item.match) || (item.exactMatch && currentPath === item.exactMatch);
    }
    return location.pathname === item.match || location.pathname.startsWith(item.match + "/");
  };

  const portalName = role === "ADMIN" ? "Admin Portal" : role === "STUDENT" ? "Student Portal" : role === "REVIEWER" ? "Reviewer Portal" : "Portal";

  return (
    <div className="w-64 bg-slate-900 text-slate-300 flex flex-col h-full shadow-2xl z-20 transition-all shrink-0">
      {/* Brand */}
      <div className="p-6 border-b border-slate-800">
        <h2 className="text-xl font-bold text-white tracking-wide">ScholarTrack</h2>
        <p className="text-xs text-slate-500 mt-1">{portalName}</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-6 space-y-1 overflow-y-auto">
        <p className="px-3 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Menu</p>
        {navItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
              isActive(item)
                ? "bg-blue-600 text-white shadow-md shadow-blue-900/20"
                : "hover:bg-slate-800 hover:text-white"
            }`}
          >
            <span className="text-lg">{item.icon}</span>
            {item.label}
          </Link>
        ))}
      </nav>

      {/* Footer / Logout */}
      <div className="p-4 border-t border-slate-800">
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-red-400 hover:bg-red-500/10 hover:text-red-300 transition-colors"
        >
          <span className="text-lg">🚪</span>
          Logout
        </button>
      </div>
    </div>
  );
}
