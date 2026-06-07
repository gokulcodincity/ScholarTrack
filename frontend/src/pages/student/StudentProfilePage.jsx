import { useState, useEffect } from "react";
import DashboardLayout from "../../components/DashboardLayout";
import Loader from "../../components/Loader";
import ErrorMessage from "../../components/ErrorMessage";
import { getStudent, createStudent } from "../../services/studentService";
import { getUserById } from "../../services/userService";

function getPayload() {
  const token = localStorage.getItem("token");
  if (!token) return null;
  try { return JSON.parse(atob(token.split(".")[1])); } catch { return null; }
}

export default function StudentProfilePage() {
  const [profile, setProfile] = useState(null);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [department, setDepartment] = useState("");
  const [cgpa, setCgpa] = useState("");
  const [academicYear, setAcademicYear] = useState("");
  
  const [submitting, setSubmitting] = useState(false);
  const [successMsg, setSuccessMsg] = useState("");

  const payload = getPayload();
  const userId = payload?.id;

  useEffect(() => {
    if (!userId) {
      setError("You must be logged in to view this page.");
      setLoading(false);
      return;
    }
    fetchProfile();
  }, [userId]);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      setError("");
      
      try {
        const userRes = await getUserById(userId);
        setUser(userRes.data);
      } catch (err) {
        console.warn("Could not fetch user details");
      }

      const { data } = await getStudent(userId);
      setProfile(data);
    } catch (err) {
      if (err?.response?.status === 404) {
        // Profile not created yet
        setProfile(null);
      } else {
        setError("Failed to load profile details.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userId) return;
    setSubmitting(true);
    setSuccessMsg("");
    setError("");

    try {
      await createStudent({
        user_id: userId,
        department,
        cgpa: parseFloat(cgpa),
        academic_year: academicYear
      });
      setSuccessMsg("Profile created successfully!");
      fetchProfile();
    } catch (err) {
      setError("Failed to create profile. Ensure you have not already created one.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <Loader />;

  return (
    <DashboardLayout title="Student System">
      <div className="flex justify-center py-12 px-4">
        <div className="w-full max-w-lg">
          <h1 className="text-3xl font-bold text-slate-800 mb-2">My Profile</h1>
          <p className="text-slate-500 mb-8">Manage your academic details for scholarship applications.</p>

          {error && <ErrorMessage message={error} />}
          {successMsg && <div className="bg-green-50 text-green-700 p-4 rounded-xl mb-6">{successMsg}</div>}

          {profile ? (
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <div className="flex items-center gap-4 mb-6 pb-6 border-b border-slate-100">
                <div className="bg-blue-100 text-blue-600 w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold">
                  {user?.name?.[0] || "S"}
                </div>
                <div>
                  <h2 className="text-xl font-bold text-slate-800">{user?.name || "Student"}</h2>
                  <p className="text-slate-500">{user?.email}</p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex justify-between items-center p-4 bg-slate-50 rounded-xl">
                  <span className="text-slate-500 font-medium">Department</span>
                  <span className="font-semibold text-slate-800">{profile.department}</span>
                </div>
                <div className="flex justify-between items-center p-4 bg-slate-50 rounded-xl">
                  <span className="text-slate-500 font-medium">CGPA</span>
                  <span className="font-semibold text-slate-800">{profile.cgpa.toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center p-4 bg-slate-50 rounded-xl">
                  <span className="text-slate-500 font-medium">Academic Year</span>
                  <span className="font-semibold text-slate-800">{profile.academic_year}</span>
                </div>
                <div className="flex justify-between items-center p-4 bg-blue-50 rounded-xl border border-blue-100">
                  <span className="text-blue-700 font-medium">Total Applications</span>
                  <span className="font-bold text-blue-800">{profile.application_count}</span>
                </div>
              </div>
              <p className="text-xs text-center text-slate-400 mt-6">Contact administration if you need to update these locked fields.</p>
            </div>
          ) : (
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <div className="bg-yellow-50 text-yellow-800 p-4 rounded-xl mb-6 text-sm">
                You haven't set up your academic profile yet. Please complete it below before applying to scholarships.
              </div>
              <form onSubmit={handleSubmit} className="space-y-5">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Department</label>
                  <input
                    required
                    value={department}
                    onChange={(e) => setDepartment(e.target.value)}
                    placeholder="e.g. Computer Science"
                    className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none transition"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">CGPA</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    max="10"
                    required
                    value={cgpa}
                    onChange={(e) => setCgpa(e.target.value)}
                    placeholder="e.g. 8.5"
                    className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none transition"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Academic Year</label>
                  <select
                    required
                    value={academicYear}
                    onChange={(e) => setAcademicYear(e.target.value)}
                    className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none transition"
                  >
                    <option value="" disabled>Select Year</option>
                    <option value="1st Year">1st Year</option>
                    <option value="2nd Year">2nd Year</option>
                    <option value="3rd Year">3rd Year</option>
                    <option value="4th Year">4th Year</option>
                    <option value="Graduated">Graduated</option>
                  </select>
                </div>
                <button
                  type="submit"
                  disabled={submitting}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg text-sm transition disabled:opacity-60"
                >
                  {submitting ? "Saving..." : "Save Profile"}
                </button>
              </form>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}
