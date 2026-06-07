import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

import { register } from "../../services/authService";
import Navbar from "../../components/Navbar";
import ErrorMessage from "../../components/ErrorMessage";

function RegisterPage() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    role: "student",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      setError("");
      setLoading(true);

      const payload = { ...formData };
      if (payload.cgpa === "") payload.cgpa = null;
      if (payload.department === "") payload.department = null;
      if (payload.academic_year === "") payload.academic_year = null;

      const response = await register(payload);

      if (formData.role === "reviewer") {
        // Redirect to reviewer request form with user_id
        navigate("/reviewer-request", {
          state: { user_id: response.data.user_id },
        });
      } else {
        alert("Registration successful! Please login.");
        navigate("/");
      }
    } catch (err) {
      console.error(err);
      setError(err?.response?.data?.detail || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />

      <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
        <div className="w-full max-w-md bg-white shadow-xl rounded-2xl p-8">
          <h1 className="text-3xl font-bold text-center text-blue-600 mb-2">
            ScholarTrack
          </h1>

          <p className="text-center text-slate-500 mb-6">Create your account</p>

          {error && <ErrorMessage message={error} />}

          <form onSubmit={handleRegister} className="space-y-4">
            <div>
              <label className="block mb-1 text-sm font-medium">
                Full Name
              </label>

              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                className="w-full border border-slate-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter your name"
              />
            </div>

            <div>
              <label className="block mb-1 text-sm font-medium">Email</label>

              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="w-full border border-slate-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter your email"
              />
            </div>

            <div>
              <label className="block mb-1 text-sm font-medium">Password</label>

              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                className="w-full border border-slate-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter password"
              />
            </div>

            <div>
              <label className="block mb-1 text-sm font-medium">Role</label>

              <select
                name="role"
                value={formData.role}
                onChange={handleChange}
                className="w-full border border-slate-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="student">Student</option>

                <option value="reviewer">Reviewer</option>
              </select>
            </div>

            {formData.role === "student" && (
              <>
                <div>
                  <label className="block mb-1 text-sm font-medium">Department</label>
                  <input
                    type="text"
                    name="department"
                    value={formData.department || ""}
                    onChange={handleChange}
                    className="w-full border border-slate-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g. Computer Science"
                  />
                </div>
                <div>
                  <label className="block mb-1 text-sm font-medium">CGPA</label>
                  <input
                    type="number"
                    step="0.01"
                    name="cgpa"
                    value={formData.cgpa || ""}
                    onChange={handleChange}
                    className="w-full border border-slate-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g. 8.5"
                  />
                </div>
                <div>
                  <label className="block mb-1 text-sm font-medium">Academic Year</label>
                  <input
                    type="text"
                    name="academic_year"
                    value={formData.academic_year || ""}
                    onChange={handleChange}
                    className="w-full border border-slate-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g. 2024-2025"
                  />
                </div>
              </>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
            >
              {loading ? "Creating Account..." : "Register"}
            </button>
          </form>

          <p className="text-center mt-6 text-sm text-slate-600">
            Already have an account?{" "}
            <Link to="/" className="text-blue-600 font-semibold">
              Login
            </Link>
          </p>
        </div>
      </div>
    </>
  );
}

export default RegisterPage;
