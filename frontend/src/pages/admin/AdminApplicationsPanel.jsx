import { useEffect, useState } from "react";
import { getAllApplications, assignReviewer, recordDecision, getApplicationDetail } from "../../services/applicationService";
import { getActiveReviewers, updateDecision } from "../../services/adminService";
import Loader from "../../components/Loader";
import ErrorMessage from "../../components/ErrorMessage";

export default function AdminApplicationsPanel() {
  const [applications, setApplications] = useState([]);
  const [reviewers, setReviewers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [reviewerId, setReviewerId] = useState("");
  const [decision, setDecision] = useState("AWARDED");
  const [selectedApp, setSelectedApp] = useState(null);

  useEffect(() => {
    fetchApps();
    fetchReviewers();
  }, []);

  const fetchApps = async () => {
    try {
      const { data } = await getAllApplications();
      setApplications(data);
    } catch (err) {
      setError("Failed to fetch applications");
    } finally {
      setLoading(false);
    }
  };

  const fetchReviewers = async () => {
    try {
      const { data } = await getActiveReviewers();
      setReviewers(data);
      if (data.length > 0) setReviewerId(data[0].id.toString());
    } catch (err) {
      console.error("Failed to fetch reviewers", err);
    }
  };

  const handleAssign = async (appId) => {
    if (!reviewerId) return alert("Select a Reviewer");
    try {
      await assignReviewer(appId, { reviewer_id: parseInt(reviewerId) });
      alert("Reviewer assigned!");
      fetchApps();
    } catch (err) {
      alert("Failed to assign reviewer");
    }
  };

  const handleDecision = async (appId) => {
    try {
      await recordDecision(appId, { application_id: appId, decision_status: decision });
      alert("Decision recorded!");
      fetchApps();
      viewDetails(appId);
    } catch (err) {
      alert("Failed to record decision. Make sure the review is complete.");
    }
  };

  const handleUpdateDecision = async (decisionId, appId) => {
    try {
      await updateDecision(decisionId, { decision_status: decision });
      alert("Decision updated!");
      fetchApps();
      viewDetails(appId);
    } catch (err) {
      alert("Failed to update decision.");
    }
  };

  const viewDetails = async (appId) => {
    try {
      const { data } = await getApplicationDetail(appId);
      setSelectedApp(data);
    } catch {
      alert("Failed to load details");
    }
  };

  if (loading) return <Loader />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold mb-6 border-b pb-4">All Applications</h2>
      
      {applications.length === 0 ? (
        <p className="text-slate-500">No applications found.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="bg-slate-100 text-slate-600">
              <tr>
                <th className="px-4 py-3 rounded-l-lg">Application ID</th>
                <th className="px-4 py-3">Student Name</th>
                <th className="px-4 py-3">Student ID</th>
                <th className="px-4 py-3">Scholarship ID</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Reviewer Name</th>
                <th className="px-4 py-3 rounded-r-lg text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {applications.map(app => (
                <tr key={app.id} className="border-b last:border-0 hover:bg-slate-50">
                  <td className="px-4 py-3 font-medium">#{app.id}</td>
                  <td className="px-4 py-3 font-semibold text-slate-800">{app.student_name || "Unknown"}</td>
                  <td className="px-4 py-3 text-slate-600">{app.student_id}</td>
                  <td className="px-4 py-3 text-slate-600">{app.scholarship_id}</td>
                  <td className="px-4 py-3">
                    <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-semibold">
                      {app.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-slate-600">{app.reviewer_name ? `${app.reviewer_name} (ID: ${app.reviewer_id})` : "Unassigned"}</td>
                  <td className="px-4 py-3 text-right space-x-2">
                    <button onClick={() => viewDetails(app.id)} className="text-blue-600 hover:underline">View</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {selectedApp && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold">Application #{selectedApp.application.id} Details</h3>
              <button onClick={() => setSelectedApp(null)} className="text-slate-400 hover:text-slate-800">✕</button>
            </div>
            
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-slate-50 p-3 rounded">
                <p className="text-xs text-slate-500">Student</p>
                <p className="font-semibold">{selectedApp.application.student_name || "Unknown"} (ID: {selectedApp.application.student_id})</p>
              </div>
              <div className="bg-slate-50 p-3 rounded">
                <p className="text-xs text-slate-500">Status</p>
                <p className="font-semibold">{selectedApp.application.status}</p>
              </div>
            </div>

            <div className="mb-6">
              <h4 className="font-semibold border-b pb-2 mb-2">Essay</h4>
              <p className="text-sm text-slate-700 whitespace-pre-wrap bg-slate-50 p-3 rounded">
                {selectedApp.essay?.essay || "No essay provided"}
              </p>
            </div>

            {selectedApp.reviewer_note && (
              <div className="mb-6 border border-blue-100 rounded-lg p-4 bg-blue-50">
                <h4 className="font-semibold text-blue-800 mb-2">Reviewer Feedback (Score: {selectedApp.reviewer_note.score}/100)</h4>
                <p className="text-sm text-blue-900 whitespace-pre-wrap">{selectedApp.reviewer_note.reviewer_notes}</p>
              </div>
            )}

            <div className="flex flex-col gap-4 border-t pt-4">
              <div className="flex items-end gap-2">
                <div className="flex-1">
                  <label className="block text-xs font-medium text-slate-500 mb-1">Assign Reviewer</label>
                  <select value={reviewerId} onChange={e => setReviewerId(e.target.value)} className="w-full border rounded px-3 py-2 text-sm">
                    {reviewers.length === 0 ? (
                      <option value="">No reviewers available</option>
                    ) : (
                      reviewers.map(r => (
                        <option key={r.id} value={r.id}>{r.name} ({r.email})</option>
                      ))
                    )}
                  </select>
                </div>
                <button onClick={() => handleAssign(selectedApp.application.id)} className="bg-slate-800 text-white px-4 py-2 rounded text-sm hover:bg-slate-700">Assign</button>
              </div>

              {selectedApp.application.review_completed && !selectedApp.decision_recorded && (
                <div className="flex items-end gap-2 mt-4">
                  <div className="flex-1">
                    <label className="block text-xs font-medium text-slate-500 mb-1">Make Final Decision</label>
                    <select value={decision} onChange={e => setDecision(e.target.value)} className="w-full border rounded px-3 py-2 text-sm">
                      <option value="AWARDED">Award Scholarship</option>
                      <option value="SHORTLISTED">Shortlist</option>
                      <option value="REJECTED">Reject</option>
                    </select>
                  </div>
                  <button onClick={() => handleDecision(selectedApp.application.id)} className="bg-green-600 text-white px-4 py-2 rounded text-sm hover:bg-green-700">Submit Decision</button>
                </div>
              )}

              {selectedApp.decision_recorded && selectedApp.decision?.decision_status === "SHORTLISTED" && (
                <div className="flex items-end gap-2 mt-4 bg-yellow-50 p-3 rounded border border-yellow-100">
                  <div className="flex-1">
                    <label className="block text-xs font-medium text-yellow-800 mb-1">Update Shortlisted Decision</label>
                    <select value={decision} onChange={e => setDecision(e.target.value)} className="w-full border-yellow-300 rounded px-3 py-2 text-sm">
                      <option value="SHORTLISTED">Remain Shortlisted</option>
                      <option value="AWARDED">Upgrade to Awarded</option>
                      <option value="REJECTED">Reject</option>
                    </select>
                  </div>
                  <button onClick={() => handleUpdateDecision(selectedApp.decision.id, selectedApp.application.id)} className="bg-yellow-600 text-white px-4 py-2 rounded text-sm hover:bg-yellow-700">Update Status</button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
