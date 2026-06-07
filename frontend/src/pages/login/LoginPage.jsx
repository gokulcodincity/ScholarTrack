import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login } from "../../services/authService";
import ErrorMessage from "../../components/ErrorMessage";

const features = [
  "Browse & Apply for Scholarships",
  "AI-Powered Application Scoring",
  "Expert Reviewer Network",
  "Real-time Decision Tracking",
];

export default function LoginPage() {
  const navigate = useNavigate();

  const [email, setEmail]       = useState("");
  const [password, setPassword] = useState("");
  const [showPw, setShowPw]     = useState(false);
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const { data } = await login({ email, password });
      const token = data.access_token;
      localStorage.setItem("token", token);
      
      const payload = JSON.parse(atob(token.split(".")[1]));
      if (payload.role === "ADMIN") {
        navigate("/admin");
      } else if (payload.role === "REVIEWER") {
        navigate("/reviewer");
      } else {
        navigate("/scholarships");
      }
    } catch (err) {
      setError(err?.response?.data?.detail || "Invalid credentials. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">

      {/* Left dark panel */}
      <div className="hidden lg:flex w-5/12 bg-[#0d1b2a] flex-col justify-between p-12 text-white">
        <div className="flex items-center gap-2">
          <div className="bg-blue-600 w-9 h-9 rounded-xl flex items-center justify-center text-lg font-bold">S</div>
          <span className="text-xl font-bold">ScholarTrack</span>
        </div>

        <div>
          <h1 className="text-4xl font-bold leading-tight mb-4">
            Your Scholar's<br />Command Center
          </h1>
          <p className="text-slate-400 text-sm leading-relaxed mb-8">
            Connect with opportunities that match your potential. Whether you're a student searching
            for funding or a reviewer shaping futures, ScholarTrack powers every step.
          </p>
          <ul className="space-y-4">
            {features.map((f) => (
              <li key={f} className="flex items-center gap-3 text-sm text-slate-300">
                <span className="w-5 h-5 rounded-full bg-blue-600 flex items-center justify-center text-white text-xs">✓</span>
                {f}
              </li>
            ))}
          </ul>
        </div>

        <p className="text-xs text-slate-600">© 2026 ScholarTrack. All rights reserved.</p>
      </div>

      {/* Right white panel */}
      <div className="flex-1 flex flex-col items-center justify-center px-6 py-12 bg-white">
        <div className="w-full max-w-md">

          {/* Title */}
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold text-blue-600">ScholarTrack</h2>
            <p className="text-sm text-blue-500 mt-1">Scholarship Management Platform</p>
          </div>

          {/* Login / Register tabs */}
          <div className="flex border border-slate-200 rounded-lg p-1 mb-6 bg-slate-50">
            <span className="flex-1 text-center py-2 rounded-md bg-blue-600 text-white text-sm font-semibold">
              🔐 Login
            </span>
            <Link to="/register" className="flex-1 text-center py-2 rounded-md text-slate-500 text-sm font-medium hover:text-slate-700 transition">
              👤 Register
            </Link>
          </div>

          {/* Form */}
          <form onSubmit={handleLogin} className="space-y-4">
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">✉</span>
              <input
                type="email"
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full border border-slate-200 rounded-lg pl-9 pr-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">🔒</span>
              <input
                type={showPw ? "text" : "password"}
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full border border-slate-200 rounded-lg pl-9 pr-10 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                type="button"
                onClick={() => setShowPw(!showPw)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs hover:text-slate-600"
              >
                {showPw ? "Hide" : "Show"}
              </button>
            </div>

            {error && <ErrorMessage message={error} />}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white font-semibold py-3 rounded-lg text-sm transition"
            >
              {loading ? "Signing in…" : "Login to Dashboard"}
            </button>
          </form>

          <p className="text-center text-xs text-slate-500 mt-6">
            Don't have an account?{" "}
            <Link to="/register" className="text-blue-600 font-medium hover:underline">Register here</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
