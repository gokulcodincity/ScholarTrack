import { useState, useEffect } from "react";
import DashboardLayout from "../../components/DashboardLayout";
import Loader from "../../components/Loader";
import ErrorMessage from "../../components/ErrorMessage";
import { getStudentApplications, getApplicationDetail } from "../../services/applicationService";

function getPayload() {
  const token = localStorage.getItem("token");
  if (!token) return null;
  try { return JSON.parse(atob(token.split(".")[1])); } catch { return null; }
}

const STATUS_STYLE = {
  PENDING:      "bg-yellow-100 text-yellow-700",
  UNDER_REVIEW: "bg-blue-100 text-blue-700",
  REVIEW_DONE:  "bg-purple-100 text-purple-700",
  SHORTLISTED:  "bg-cyan-100 text-cyan-700",
  AWARDED:      "bg-green-100 text-green-700",
  REJECTED:     "bg-red-100 text-red-700",
};

export default function StudentDashboard() {
  const [applications, setApplications] = useState([]);
  const [selected, setSelected] = useState(null); // full detail of clicked app
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [error, setError] = useState("");

  const payload = getPayload();
  const studentId = payload?.id;

  useEffect(() => {
    if (!studentId) { setError("Not logged in."); setLoading(false); return; }
    getStudentApplications(studentId)
      .then(({ data }) => setApplications(data))
      .catch(() => setError("Failed to load applications."))
      .finally(() => setLoading(false));
  }, [studentId]);

  const viewDetail = async (appId) => {
    setDetailLoading(true);
    try {
      const { data } = await getApplicationDetail(appId);
      setSelected(data);
    } catch {
      setError("Could not load application details.");
    } finally {
      setDetailLoading(false);
    }
  };

  return (
    <DashboardLayout title="Student System">
      <div className="py-8 px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-2xl font-bold text-slate-800 mb-1">My Applications</h1>
          <p className="text-slate-500 mb-6">Track the status of your scholarship applications.</p>

          {loading && <Loader />}
          {error && <ErrorMessage message={error} />}

          {!loading && !error && applications.length === 0 && (
            <p className="text-center text-slate-500 py-16">You haven't applied for any scholarship yet.</p>
          )}

          {/* Application List */}
          {!loading && !error && applications.length > 0 && (
            <div className="space-y-4">
              {applications.map((app) => (
                <div key={app.id} className="bg-white rounded-xl shadow p-5">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="text-sm text-slate-500">Application #{app.id}</p>
                      <p className="text-slate-700 text-sm mt-1">Scholarship ID: <span className="font-semibold">{app.scholarship_id}</span></p>
                      <p className="text-slate-600 text-sm">Applied: {new Date(app.created_at).toLocaleDateString()}</p>
                    </div>
                    <div className="text-right">
                      <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${STATUS_STYLE[app.status] ?? "bg-slate-100 text-slate-600"}`}>
                        {app.status.replace("_", " ")}
                      </span>
                      <div className="mt-3">
                        <button
                          onClick={() => viewDetail(app.id)}
                          className="text-xs text-blue-600 hover:underline"
                        >
                          View Details →
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Detail Panel */}
          {detailLoading && <Loader />}
          {selected && !detailLoading && (
            <div className="mt-8 bg-white rounded-xl shadow p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-bold text-slate-800">Application #{selected.application?.id} — Details</h2>
                <button onClick={() => setSelected(null)} className="text-slate-400 hover:text-slate-600 text-sm">✕ Close</button>
              </div>

              {/* Status */}
              <p className="mb-4">
                <span className="text-sm font-medium text-slate-600">Status: </span>
                <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${STATUS_STYLE[selected.application?.status] ?? ""}`}>
                  {selected.application?.status?.replace("_", " ")}
                </span>
              </p>

              {/* Essay */}
              {selected.essay && (
                <div className="mb-4">
                  <p className="text-sm font-semibold text-slate-700 mb-1">Your Essay</p>
                  <p className="text-sm text-slate-600 bg-slate-50 rounded-lg p-3 leading-relaxed">{selected.essay.essay}</p>
                  {selected.essay.supporting_content && (
                    <p className="text-xs text-slate-500 mt-2">Supporting: {selected.essay.supporting_content}</p>
                  )}
                </div>
              )}

              {/* Reviewer Note */}
              {selected.reviewer_note ? (
                <div className="bg-blue-50 rounded-lg p-4">
                  <p className="text-sm font-semibold text-blue-700 mb-2">Reviewer Feedback</p>
                  <p className="text-sm text-slate-700">{selected.reviewer_note.reviewer_notes}</p>
                  <p className="text-sm text-slate-600 mt-1">Score: <span className="font-bold">{selected.reviewer_note.score}/100</span></p>
                  {selected.reviewer_note.scoring_rationale && (
                    <p className="text-xs text-slate-500 mt-1">Rationale: {selected.reviewer_note.scoring_rationale}</p>
                  )}
                </div>
              ) : (
                <p className="text-sm text-slate-400 italic">Review not yet completed.</p>
              )}

              {/* Decision */}
              {selected.decision_recorded && (
                <p className="mt-4 text-sm font-semibold text-green-600">✓ Decision has been recorded by admin.</p>
              )}
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}
