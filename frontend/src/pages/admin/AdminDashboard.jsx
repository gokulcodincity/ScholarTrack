import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import api from "../../services/api";
import {
  getPendingReviewers,
  approveReviewer,
  rejectReviewer,
  getReviewerResumeUrl,
} from "../../services/adminService";
import Loader from "../../components/Loader";
import AdminApplicationsPanel from "./AdminApplicationsPanel";
import AdminUsersPanel from "./AdminUsersPanel";
import AdminScholarshipsPanel from "./AdminScholarshipsPanel";
import AdminDecisionsPanel from "./AdminDecisionsPanel";
import AdminHomeDashboard from "./AdminHomeDashboard";
import DashboardLayout from "../../components/DashboardLayout";

function AdminDashboard() {
  const [searchParams, setSearchParams] = useSearchParams();
  const activeTab = searchParams.get("tab") || "dashboard";

  const setActiveTab = (tab) => {
    setSearchParams({ tab });
  };

  const [pendingReviewers, setPendingReviewers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchPendingReviewers();
  }, []);

  const fetchPendingReviewers = async () => {
    try {
      setError("");
      const response = await getPendingReviewers();
      setPendingReviewers(response.data);
    } catch (err) {
      console.error("Failed to fetch pending reviewers", err);
      setError("Failed to load pending reviewers.");
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (userId) => {
    try {
      await approveReviewer(userId);
      alert("Reviewer approved! They can now login.");
      fetchPendingReviewers();
    } catch (error) {
      console.error(error);
      alert("Failed to approve reviewer");
    }
  };

  const handleReject = async (userId) => {
    try {
      await rejectReviewer(userId);
      alert("Reviewer rejected. Account downgraded to Student.");
      fetchPendingReviewers();
    } catch (error) {
      console.error(error);
      alert("Failed to reject reviewer");
    }
  };

  const handleDownloadResume = async (userId) => {
    try {
      const response = await api.get(getReviewerResumeUrl(userId), {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(
        new Blob([response.data], { type: "application/pdf" }),
      );
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `resume_user_${userId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Failed to download resume", error);
      alert("Resume not available");
    }
  };

  return (
    <DashboardLayout title="Admin System">
      <div className="p-8">
        {activeTab === "dashboard" && (
          <AdminHomeDashboard setActiveTab={setActiveTab} />
        )}

        <div className={activeTab === "dashboard" ? "hidden" : "block"}>
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8">
            {activeTab === "applications" && <AdminApplicationsPanel />}
            {activeTab === "scholarships" && <AdminScholarshipsPanel />}
            {activeTab === "users" && <AdminUsersPanel />}
            {activeTab === "decisions" && <AdminDecisionsPanel />}

            {activeTab === "reviewers" && (
              <>
                <h2 className="text-2xl font-semibold mb-6 border-b pb-4">
                  Pending Reviewer Applications
                </h2>

                {loading ? (
                  <Loader />
                ) : error ? (
                  <ErrorMessage message={error} />
                ) : pendingReviewers.length === 0 ? (
                  <p className="text-slate-500">
                    No pending reviewer applications.
                  </p>
                ) : (
                  <div className="space-y-6">
                    {pendingReviewers.map((user) => (
                      <div
                        key={user.id}
                        className="border border-slate-200 rounded-xl p-6 hover:shadow-md transition bg-slate-50/50"
                      >
                        {/* Header */}
                        <div className="flex justify-between items-start mb-4">
                          <div>
                            <h3 className="text-lg font-bold text-slate-800">
                              {user.name}
                            </h3>
                            <p className="text-slate-500 text-sm">
                              {user.email}
                            </p>
                            <span className="mt-1 inline-block bg-yellow-100 text-yellow-700 text-xs font-medium px-2.5 py-0.5 rounded">
                              {user.role}
                            </span>
                          </div>

                          {/* Action Buttons */}
                          <div className="flex gap-2 flex-wrap justify-end">
                            <button
                              onClick={() => handleApprove(user.id)}
                              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition"
                            >
                              ✓ Approve
                            </button>
                            <button
                              onClick={() => handleReject(user.id)}
                              className="border border-red-300 text-red-600 hover:bg-red-50 px-4 py-2 rounded-lg text-sm font-medium transition"
                            >
                              ✗ Reject
                            </button>
                          </div>
                        </div>

                        {/* Application Details */}
                        {user.request &&
                        user.request.status !== "NOT_SUBMITTED" ? (
                          <div className="bg-white rounded-xl p-4 text-sm space-y-3 border border-slate-200 shadow-sm">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                              <div>
                                <span className="font-semibold text-slate-600">
                                  University:{" "}
                                </span>
                                <span>{user.request.university ?? "—"}</span>
                              </div>
                              <div>
                                <span className="font-semibold text-slate-600">
                                  Department:{" "}
                                </span>
                                <span>{user.request.department ?? "—"}</span>
                              </div>
                              <div>
                                <span className="font-semibold text-slate-600">
                                  Institution Email:{" "}
                                </span>
                                <span>
                                  {user.request.institution_email ?? "—"}
                                </span>
                              </div>
                              <div>
                                <span className="font-semibold text-slate-600">
                                  Years of Experience:{" "}
                                </span>
                                <span>
                                  {user.request.years_of_experience ?? "—"}
                                </span>
                              </div>
                            </div>

                            {/* Resume Download */}
                            <div className="flex items-center gap-3 pt-1 border-t border-slate-100 mt-2">
                              <span className="font-semibold text-slate-600">
                                Resume:{" "}
                              </span>
                              {user.request.resume_filename ? (
                                <button
                                  onClick={() => handleDownloadResume(user.id)}
                                  className="inline-flex items-center gap-1.5 text-blue-600 hover:text-blue-800 text-sm font-medium transition"
                                >
                                  📄 Download / View PDF
                                </button>
                              ) : (
                                <span className="text-slate-400 italic text-sm">
                                  Not uploaded
                                </span>
                              )}
                            </div>
                          </div>
                        ) : (
                          <p className="text-sm text-amber-600 bg-amber-50 rounded-lg px-4 py-2 border border-amber-100">
                            ⚠ This user has not submitted a reviewer application
                            form yet.
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default AdminDashboard;
