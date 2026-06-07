import { useEffect, useState } from "react";
import { getAllDecisions, getDecisionById, deleteDecision } from "../../services/adminService";
import { getAllApplications } from "../../services/applicationService";
import Loader from "../../components/Loader";
import ErrorMessage from "../../components/ErrorMessage";

export default function AdminDecisionsPanel() {
  const [decisions, setDecisions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedDecision, setSelectedDecision] = useState(null);
  const [appMap, setAppMap] = useState({});

  useEffect(() => {
    fetchDecisions();
  }, []);

  const fetchDecisions = async () => {
    try {
      setLoading(true);
      const [decRes, appsRes] = await Promise.all([
        getAllDecisions(),
        getAllApplications()
      ]);
      setDecisions(decRes.data);
      
      const map = {};
      appsRes.data.forEach(app => {
        map[app.id] = {
          student_name: app.student_name,
          reviewer_name: app.reviewer_name
        };
      });
      setAppMap(map);
    } catch (err) {
      setError("Failed to fetch decisions");
    } finally {
      setLoading(false);
    }
  };

  const viewDecisionDetails = async (id) => {
    try {
      const { data } = await getDecisionById(id);
      setSelectedDecision(data);
    } catch (err) {
      alert("Failed to load decision details");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this decision? This might reset application states if not handled by backend cascades.")) return;
    try {
      await deleteDecision(id);
      alert("Decision deleted");
      fetchDecisions();
    } catch (err) {
      alert("Failed to delete decision");
    }
  };

  if (loading) return <Loader />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold mb-6 border-b pb-4">All Decisions Management</h2>

      {decisions.length === 0 ? (
        <p className="text-slate-500">No decisions found.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="bg-slate-100 text-slate-600">
              <tr>
                <th className="px-4 py-3 rounded-l-lg">ID</th>
                <th className="px-4 py-3">App ID</th>
                <th className="px-4 py-3">Student Name</th>
                <th className="px-4 py-3">Reviewer Name</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Admin ID</th>
                <th className="px-4 py-3">Date</th>
                <th className="px-4 py-3 rounded-r-lg text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {decisions.map(d => (
                <tr key={d.id} className="border-b last:border-0 hover:bg-slate-50">
                  <td className="px-4 py-3 font-medium">#{d.id}</td>
                  <td className="px-4 py-3 text-slate-600">#{d.application_id}</td>
                  <td className="px-4 py-3 text-slate-800">{appMap[d.application_id]?.student_name || "Unknown"}</td>
                  <td className="px-4 py-3 text-slate-600">{appMap[d.application_id]?.reviewer_name || "Unassigned"}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded text-xs font-semibold ${
                      d.decision_status === "AWARDED" ? "bg-green-100 text-green-800" :
                      d.decision_status === "SHORTLISTED" ? "bg-cyan-100 text-cyan-800" :
                      "bg-red-100 text-red-800"
                    }`}>
                      {d.decision_status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-slate-600">{d.decided_by}</td>
                  <td className="px-4 py-3 text-slate-600">{new Date(d.decision_date).toLocaleDateString()}</td>
                  <td className="px-4 py-3 text-right space-x-2">
                    <button onClick={() => viewDecisionDetails(d.id)} className="text-blue-600 hover:underline">View</button>
                    <button onClick={() => handleDelete(d.id)} className="text-red-600 hover:underline">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {selectedDecision && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-xl p-6 w-full max-w-sm">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold">Decision Details</h3>
              <button onClick={() => setSelectedDecision(null)} className="text-slate-400 hover:text-slate-800">✕</button>
            </div>
            <div className="space-y-3 bg-slate-50 p-4 rounded-lg text-sm">
              <p><span className="font-semibold text-slate-600">Decision ID:</span> {selectedDecision.id}</p>
              <p><span className="font-semibold text-slate-600">Application ID:</span> {selectedDecision.application_id}</p>
              <p><span className="font-semibold text-slate-600">Status:</span> {selectedDecision.decision_status}</p>
              <p><span className="font-semibold text-slate-600">Decided By (Admin ID):</span> {selectedDecision.decided_by}</p>
              <p><span className="font-semibold text-slate-600">Date:</span> {new Date(selectedDecision.decision_date).toLocaleString()}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
