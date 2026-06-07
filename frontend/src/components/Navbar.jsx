import { Link, useNavigate } from "react-router-dom";

// Decode the JWT payload (no library needed)
function getTokenPayload() {
  const token = localStorage.getItem("token");
  if (!token) return null;
  try {
    return JSON.parse(atob(token.split(".")[1]));
  } catch {
    return null;
  }
}

export default function Navbar() {
  const navigate = useNavigate();
  const payload = getTokenPayload();
  const role = payload?.role;

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <nav className="bg-white shadow sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        <Link to="/scholarships" className="text-xl font-bold text-blue-600">ScholarTrack</Link>

        <div className="flex items-center gap-4 text-sm font-medium">
          {!role && (
            <>
              <Link to="/" className="text-slate-600 hover:text-blue-600">Login</Link>
              <Link to="/register" className="text-slate-600 hover:text-blue-600">Register</Link>
            </>
          )}

          {role === "STUDENT" && (
            <>
              <Link to="/scholarships" className="text-slate-600 hover:text-blue-600">Scholarships</Link>
              <Link to="/my-applications" className="text-slate-600 hover:text-blue-600">My Applications</Link>
              <Link to="/profile" className="text-slate-600 hover:text-blue-600">My Profile</Link>
            </>
          )}

          {role === "REVIEWER" && (
            <Link to="/reviewer" className="text-slate-600 hover:text-blue-600">Reviewer Panel</Link>
          )}

          {role === "ADMIN" && (
            <Link to="/admin" className="text-slate-600 hover:text-blue-600">Admin</Link>
          )}

          {role && (
            <button
              onClick={handleLogout}
              className="bg-red-50 text-red-600 hover:bg-red-100 px-3 py-1.5 rounded-lg transition"
            >
              Logout
            </button>
          )}
        </div>
      </div>
    </nav>
  );
}
