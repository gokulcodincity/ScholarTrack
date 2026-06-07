import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import DashboardLayout from "../../components/DashboardLayout";
import Loader from "../../components/Loader";
import ErrorMessage from "../../components/ErrorMessage";
import { getReviewerApplications, getApplicationDetail, submitReview, completeReview, getEssay } from "../../services/applicationService";
import { getReviewerNote } from "../../services/reviewerNoteService";

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

export default function ReviewerDashboard() {
  const [searchParams, setSearchParams] = useSearchParams();
  const activeTab = searchParams.get("tab") || "assigned";

  const [applications, setApplications] = useState([]);
  const [selected, setSelected] = useState(null);
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [error, setError] = useState("");

  // Review form state
  const [notes, setNotes] = useState("");
  const [score, setScore] = useState("");
  const [rationale, setRationale] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [reviewError, setReviewError] = useState("");
  const [reviewSuccess, setReviewSuccess] = useState("");

  const payload = getPayload();
  const reviewerId = payload?.id;

  useEffect(() => {
    if (!reviewerId) { setError("Not logged in."); setLoading(false); return; }
    getReviewerApplications(reviewerId)
      .then(({ data }) => setApplications(data))
      .catch(() => setError("Failed to load assigned applications."))
      .finally(() => setLoading(false));
  }, [reviewerId]);

  const pendingApps = applications.filter(a => !a.review_completed);
  const completedApps = applications.filter(a => a.review_completed);

  const openDetail = async (app) => {
    setSelected(app);
    setDetail(null);
    setNotes(""); setScore(""); setRationale("");
    setReviewError(""); setReviewSuccess("");
    setDetailLoading(true);
    
    // Switch tab to scoring form automatically
    setSearchParams({ tab: "scoring" });

    try {
      const { data } = await getApplicationDetail(app.id);
      
      try {
        const essayRes = await getEssay(app.id);
        data.essay = essayRes.data;
      } catch (e) {
        console.warn("No essay found or failed to fetch essay separately");
      }
      
      try {
        const noteRes = await getReviewerNote(app.id);
        data.reviewer_note = noteRes.data;
      } catch (e) {
        console.warn("No reviewer note found or failed to fetch separately");
      }

      setDetail(data);
    } catch {
      setReviewError("Could not load application details.");
    } finally {
      setDetailLoading(false);
    }
  };

  const handleSubmitReview = async (e) => {
    e.preventDefault();
    setReviewError(""); setReviewSuccess("");
    if (!score || Number(score) < 0 || Number(score) > 100) {
      setReviewError("Score must be between 0 and 100.");
      return;
    }
    setSubmitting(true);
    try {
      await submitReview(selected.id, {
        reviewer_notes: notes,
        score: Number(score),
        scoring_rationale: rationale || null,
      });
      setReviewSuccess("Review submitted successfully!");
      // Refresh list
      const { data } = await getReviewerApplications(reviewerId);
      setApplications(data);
    } catch (err) {
      setReviewError(err?.response?.data?.detail || "Failed to submit review.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleCompleteReviewPatch = async () => {
    try {
      setSubmitting(true);
      await completeReview(selected.id);
      setReviewSuccess("Review marked as completed!");
      const { data } = await getReviewerApplications(reviewerId);
      setApplications(data);
      openDetail(selected);
    } catch (err) {
      setReviewError("Failed to mark review as complete.");
    } finally {
      setSubmitting(false);
    }
  };

  const renderAppCard = (app) => (
    <button
      key={app.id}
      onClick={() => openDetail(app)}
      className={`w-full text-left bg-white rounded-xl shadow-sm hover:shadow-md transition border-2 p-5 ${selected?.id === app.id ? "border-blue-500" : "border-slate-100"}`}
    >
      <div className="flex justify-between items-center">
        <div>
          <p className="font-bold text-slate-800">Application #{app.id}</p>
          <p className="text-slate-600 text-sm mt-1">Student: <span className="font-medium">{app.student_name || "Unknown"}</span></p>
          <p className="text-slate-500 text-xs mt-1">Scholarship #{app.scholarship_id}</p>
        </div>
        <div className="text-right">
          <span className={`text-xs font-bold px-3 py-1 rounded-full ${STATUS_STYLE[app.status] ?? "bg-slate-100 text-slate-600"}`}>
            {app.status.replace("_", " ")}
          </span>
          {app.review_completed && (
            <p className="text-xs text-green-600 mt-2 font-bold flex items-center justify-end gap-1">
              <span>✓</span> Reviewed
            </p>
          )}
        </div>
      </div>
    </button>
  );

  return (
    <DashboardLayout title="Reviewer Portal">
      <div className="p-8">
        {loading && <Loader />}
        {error && <ErrorMessage message={error} />}

        {!loading && !error && (
          <div className="max-w-4xl mx-auto">
            
            {/* ASSIGNED APPLICATIONS TAB */}
            {activeTab === "assigned" && (
              <div className="animate-fade-in">
                <h2 className="text-2xl font-bold text-slate-800 mb-2">Assigned Applications</h2>
                <p className="text-slate-500 mb-6">Applications currently pending your review.</p>
                
                {pendingApps.length === 0 ? (
                  <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-12 text-center">
                    <div className="text-4xl mb-4">🎉</div>
                    <p className="text-lg font-bold text-slate-800">All caught up!</p>
                    <p className="text-slate-500">You have no pending applications to review.</p>
                  </div>
                ) : (
                  <div className="grid gap-4">
                    {pendingApps.map(renderAppCard)}
                  </div>
                )}
              </div>
            )}

            {/* DECISION RECORDS TAB */}
            {activeTab === "decisions" && (
              <div className="animate-fade-in">
                <h2 className="text-2xl font-bold text-slate-800 mb-2">Decision Records</h2>
                <p className="text-slate-500 mb-6">History of your completed reviews.</p>
                
                {completedApps.length === 0 ? (
                  <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-12 text-center">
                    <p className="text-slate-500">You haven't completed any reviews yet.</p>
                  </div>
                ) : (
                  <div className="grid gap-4">
                    {completedApps.map(renderAppCard)}
                  </div>
                )}
              </div>
            )}

            {/* SCORING FORM TAB */}
            {activeTab === "scoring" && (
              <div className="animate-fade-in">
                <h2 className="text-2xl font-bold text-slate-800 mb-2">Scoring Form</h2>
                <p className="text-slate-500 mb-6">Review application details and submit your score.</p>
                
                {!selected ? (
                  <div className="bg-blue-50 border border-blue-100 rounded-2xl p-8 text-center">
                    <p className="text-blue-800 font-semibold mb-2">No application selected</p>
                    <p className="text-blue-600 text-sm">Please select an application from the Assigned Applications or Decision Records tab to view or score it.</p>
                  </div>
                ) : (
                  <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8">
                    <div className="flex justify-between items-center mb-6 pb-4 border-b border-slate-100">
                      <div>
                        <h2 className="text-xl font-bold text-slate-800">Application #{selected.id}</h2>
                        <p className="text-slate-500 text-sm">Student: {selected.student_name}</p>
                      </div>
                      <span className={`text-xs font-bold px-3 py-1 rounded-full ${STATUS_STYLE[selected.status] ?? "bg-slate-100 text-slate-600"}`}>
                        {selected.status.replace("_", " ")}
                      </span>
                    </div>

                    {detailLoading && <Loader />}

                    {detail && !detailLoading && (
                      <div className="grid md:grid-cols-2 gap-8">
                        {/* Left Side: App Details */}
                        <div>
                          <h3 className="font-bold text-slate-800 mb-4">Application Materials</h3>
                          {detail.essay ? (
                            <div className="space-y-4">
                              <div>
                                <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Student Essay</p>
                                <div className="bg-slate-50 rounded-xl p-4 text-sm text-slate-700 leading-relaxed border border-slate-100 max-h-64 overflow-y-auto">
                                  {detail.essay.essay}
                                </div>
                              </div>
                              {detail.essay.supporting_content && (
                                <div>
                                  <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Supporting Content</p>
                                  <div className="bg-slate-50 rounded-xl p-4 text-sm text-slate-700 leading-relaxed border border-slate-100">
                                    {detail.essay.supporting_content}
                                  </div>
                                </div>
                              )}
                            </div>
                          ) : (
                            <p className="text-slate-500 italic text-sm">No essay submitted.</p>
                          )}
                        </div>

                        {/* Right Side: Scoring Form */}
                        <div>
                          <h3 className="font-bold text-slate-800 mb-4">Evaluation</h3>
                          
                          {detail.reviewer_note ? (
                            <div className="bg-green-50 border border-green-100 rounded-xl p-6">
                              <div className="flex items-center gap-2 text-green-700 font-bold mb-4">
                                <span className="text-xl">✓</span> Review Completed
                              </div>
                              <div className="space-y-4">
                                <div>
                                  <p className="text-xs font-bold text-green-600/70 uppercase tracking-wider mb-1">Score</p>
                                  <p className="text-2xl font-black text-green-800">{detail.reviewer_note.score}<span className="text-lg text-green-600/50">/100</span></p>
                                </div>
                                <div>
                                  <p className="text-xs font-bold text-green-600/70 uppercase tracking-wider mb-1">Notes</p>
                                  <p className="text-sm text-green-900 bg-white/50 p-3 rounded-lg">{detail.reviewer_note.reviewer_notes}</p>
                                </div>
                                {detail.reviewer_note.scoring_rationale && (
                                  <div>
                                    <p className="text-xs font-bold text-green-600/70 uppercase tracking-wider mb-1">Rationale</p>
                                    <p className="text-sm text-green-900 bg-white/50 p-3 rounded-lg">{detail.reviewer_note.scoring_rationale}</p>
                                  </div>
                                )}
                              </div>
                            </div>
                          ) : (
                            <form onSubmit={handleSubmitReview} className="space-y-5 bg-slate-50 rounded-xl p-6 border border-slate-100">
                              <div>
                                <label className="block text-sm font-bold text-slate-700 mb-1">Score (0–100) <span className="text-red-500">*</span></label>
                                <input
                                  type="number"
                                  min={0}
                                  max={100}
                                  required
                                  value={score}
                                  onChange={(e) => setScore(e.target.value)}
                                  className="w-full border border-slate-200 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 font-bold text-slate-800"
                                />
                              </div>

                              <div>
                                <label className="block text-sm font-bold text-slate-700 mb-1">Review Notes <span className="text-red-500">*</span></label>
                                <textarea
                                  rows={4}
                                  required
                                  value={notes}
                                  onChange={(e) => setNotes(e.target.value)}
                                  placeholder="Provide feedback on the essay..."
                                  className="w-full border border-slate-200 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                                />
                              </div>

                              <div>
                                <label className="block text-sm font-bold text-slate-700 mb-1">Scoring Rationale <span className="text-slate-400 font-normal text-xs">(optional)</span></label>
                                <textarea
                                  rows={2}
                                  value={rationale}
                                  onChange={(e) => setRationale(e.target.value)}
                                  placeholder="Justify your score..."
                                  className="w-full border border-slate-200 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                                />
                              </div>

                              {reviewError && <ErrorMessage message={reviewError} />}
                              {reviewSuccess && <div className="bg-green-100 text-green-700 p-3 rounded-lg text-sm font-medium">{reviewSuccess}</div>}

                              <div className="flex flex-col gap-3 pt-2">
                                <button
                                  type="submit"
                                  disabled={submitting}
                                  className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white font-bold py-3 rounded-xl transition"
                                >
                                  {submitting ? "Submitting…" : "Submit Final Score"}
                                </button>
                                
                                <button
                                  type="button"
                                  onClick={handleCompleteReviewPatch}
                                  disabled={submitting}
                                  className="w-full border-2 border-blue-200 text-blue-600 hover:bg-blue-50 hover:border-blue-300 disabled:opacity-60 font-bold py-2.5 rounded-xl transition"
                                >
                                  Mark Completed (No Score)
                                </button>
                              </div>
                            </form>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
