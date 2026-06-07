import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import DashboardLayout from "../../components/DashboardLayout";
import Loader from "../../components/Loader";
import ErrorMessage from "../../components/ErrorMessage";
import { getScholarshipById } from "../../services/scholarshipService";
import { createApplication, submitEssay } from "../../services/applicationService";

// Decode JWT to get user_id
function getPayload() {
  const token = localStorage.getItem("token");
  if (!token) return null;
  try { return JSON.parse(atob(token.split(".")[1])); } catch { return null; }
}

export default function ApplicationPage() {
  const { scholarshipId } = useParams();
  const navigate = useNavigate();

  const [scholarship, setScholarship] = useState(null);
  const [essay, setEssay] = useState("");
  const [supporting, setSupporting] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const payload = getPayload();
  const studentId = payload?.id;

  useEffect(() => {
    getScholarshipById(scholarshipId)
      .then(({ data }) => setScholarship(data))
      .catch(() => setError("Could not load scholarship details."))
      .finally(() => setLoading(false));
  }, [scholarshipId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!studentId) { setError("Please login again."); return; }
    setSubmitting(true);
    setError("");
    try {
      // Step 1 — create application
      const { data: app } = await createApplication({
        student_id: studentId,
        scholarship_id: Number(scholarshipId),
      });
      // Step 2 — attach essay
      await submitEssay({
        application_id: app.id,
        essay,
        supporting_content: supporting || null,
      });
      alert("Application submitted successfully!");
      navigate("/my-applications");
    } catch (err) {
      setError(err?.response?.data?.detail || "Submission failed. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <Loader />;

  return (
    <DashboardLayout title="Apply for Scholarship">
      <div className="flex items-center justify-center px-4 py-10">
        <div className="w-full max-w-xl bg-white rounded-xl shadow p-8">
          <h1 className="text-2xl font-bold text-slate-800 mb-1">Apply for Scholarship</h1>

          {scholarship && (
            <div className="bg-blue-50 rounded-lg p-4 mb-6 text-sm">
              <p className="font-semibold text-blue-700">{scholarship.title}</p>
              <p className="text-slate-600">Amount: ₹{scholarship.amount?.toLocaleString()} | Deadline: {scholarship.deadline}</p>
            </div>
          )}

          {error && <ErrorMessage message={error} />}

          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Student ID — read-only from token */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Student ID</label>
              <input
                value={studentId ?? ""}
                disabled
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm bg-slate-100 text-slate-500"
              />
            </div>

            {/* Essay */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Essay <span className="text-red-500">*</span></label>
              <textarea
                rows={5}
                required
                value={essay}
                onChange={(e) => setEssay(e.target.value)}
                placeholder="Write about yourself, your achievements, and why you deserve this scholarship..."
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              />
            </div>

            {/* Supporting Content */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Supporting Content <span className="text-slate-400 text-xs">(optional)</span></label>
              <textarea
                rows={3}
                value={supporting}
                onChange={(e) => setSupporting(e.target.value)}
                placeholder="Any additional information, links, or references..."
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              />
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white font-semibold py-3 rounded-lg text-sm transition"
            >
              {submitting ? "Submitting…" : "Submit Application"}
            </button>
          </form>
        </div>
      </div>
    </DashboardLayout>
  );
}
