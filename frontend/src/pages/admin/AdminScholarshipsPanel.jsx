import { useEffect, useState } from "react";
import { getScholarships, createScholarship, updateScholarship, deleteScholarship, getScholarshipStats } from "../../services/scholarshipService";
import Loader from "../../components/Loader";
import ErrorMessage from "../../components/ErrorMessage";

export default function AdminScholarshipsPanel() {
  const [scholarships, setScholarships] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [stats, setStats] = useState(null);

  const [form, setForm] = useState({ id: null, title: "", description: "", amount: "", deadline: "", eligibility: "", field: "" });
  const [isEditing, setIsEditing] = useState(false);
  const [showForm, setShowForm] = useState(false);

  // Filter state
  const [filterField, setFilterField] = useState("");
  const [filterMinAmount, setFilterMinAmount] = useState("");
  const [filterDeadline, setFilterDeadline] = useState("");

  useEffect(() => {
    fetchScholarships();
  }, []);

  const fetchScholarships = async () => {
    try {
      setLoading(true);
      const params = {};
      if (filterField) params.field = filterField;
      if (filterMinAmount) params.min_amount = filterMinAmount;
      if (filterDeadline) params.deadline_before = filterDeadline;
      
      const { data } = await getScholarships(params);
      setScholarships(data);
    } catch (err) {
      setError("Failed to fetch scholarships");
    } finally {
      setLoading(false);
    }
  };

  const handleFilter = (e) => {
    e.preventDefault();
    fetchScholarships();
  };

  const handleReset = () => {
    setFilterField(""); setFilterMinAmount(""); setFilterDeadline("");
    setTimeout(() => {
      // Need to fetch without filters
      getScholarships().then(({ data }) => setScholarships(data)).catch(() => {});
    }, 0);
  };

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      if (isEditing) {
        await updateScholarship(form.id, form);
        alert("Scholarship updated");
      } else {
        await createScholarship(form);
        alert("Scholarship created");
      }
      setShowForm(false);
      fetchScholarships();
    } catch (err) {
      alert("Failed to save scholarship");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this scholarship?")) return;
    try {
      await deleteScholarship(id);
      alert("Scholarship deleted");
      fetchScholarships();
    } catch (err) {
      alert("Failed to delete scholarship");
    }
  };

  const viewStats = async (id) => {
    try {
      const { data } = await getScholarshipStats(id);
      setStats(data);
    } catch (err) {
      alert("Failed to load stats");
    }
  };

  const openForm = (sch = null) => {
    if (sch) {
      setForm(sch);
      setIsEditing(true);
    } else {
      setForm({ id: null, title: "", description: "", amount: "", deadline: "", eligibility: "", field: "" });
      setIsEditing(false);
    }
    setShowForm(true);
  };

  if (loading) return <Loader />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center mb-6 border-b pb-4">
        <h2 className="text-2xl font-semibold">Scholarships Management</h2>
        <button onClick={() => openForm()} className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700">
          + New Scholarship
        </button>
      </div>

      {/* Filter Bar */}
      <form onSubmit={handleFilter} className="bg-slate-50 border border-slate-200 rounded-xl p-4 mb-6 flex flex-wrap gap-3 items-end">
        <div className="flex-1 min-w-[140px]">
          <label className="block text-xs font-medium text-slate-500 mb-1">Field</label>
          <input
            value={filterField}
            onChange={(e) => setFilterField(e.target.value)}
            placeholder="e.g. Engineering"
            className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="flex-1 min-w-[140px]">
          <label className="block text-xs font-medium text-slate-500 mb-1">Min Amount (₹)</label>
          <input
            type="number"
            value={filterMinAmount}
            onChange={(e) => setFilterMinAmount(e.target.value)}
            placeholder="e.g. 10000"
            className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="flex-1 min-w-[140px]">
          <label className="block text-xs font-medium text-slate-500 mb-1">Deadline Before</label>
          <input
            type="date"
            value={filterDeadline}
            onChange={(e) => setFilterDeadline(e.target.value)}
            className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="flex gap-2">
          <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition">
            Filter
          </button>
          <button type="button" onClick={handleReset} className="border border-slate-200 bg-white text-slate-600 hover:bg-slate-50 px-4 py-2 rounded-lg text-sm font-medium transition">
            Reset
          </button>
        </div>
      </form>

      <div className="grid grid-cols-1 gap-4">
        {scholarships.map((s) => (
          <div key={s.id} className="border border-slate-200 rounded-xl p-4 hover:shadow-md transition bg-white flex justify-between items-center">
            <div>
              <h3 className="text-lg font-bold text-slate-800">{s.title}</h3>
              <p className="text-slate-500 text-sm">₹{s.amount} • Deadline: {s.deadline}</p>
            </div>
            <div className="flex gap-2">
              <button onClick={() => viewStats(s.id)} className="text-indigo-600 border border-indigo-200 bg-indigo-50 px-3 py-1.5 rounded text-sm hover:bg-indigo-100">Stats</button>
              <button onClick={() => openForm(s)} className="text-blue-600 border border-blue-200 bg-blue-50 px-3 py-1.5 rounded text-sm hover:bg-blue-100">Edit</button>
              <button onClick={() => handleDelete(s.id)} className="text-red-600 border border-red-200 bg-red-50 px-3 py-1.5 rounded text-sm hover:bg-red-100">Delete</button>
            </div>
          </div>
        ))}
      </div>

      {/* Stats Modal */}
      {stats && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-xl p-6 w-full max-w-sm">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold">Scholarship Stats</h3>
              <button onClick={() => setStats(null)} className="text-slate-400 hover:text-slate-800">✕</button>
            </div>
            <div className="space-y-3 bg-indigo-50 p-4 rounded-lg text-sm text-indigo-900 border border-indigo-100">
              <p className="flex justify-between border-b border-indigo-200 pb-1"><span>Total Applications:</span> <span className="font-bold">{stats.total_applications}</span></p>
              <p className="flex justify-between border-b border-indigo-200 pb-1"><span>Pending:</span> <span className="font-bold">{stats.pending}</span></p>
              <p className="flex justify-between border-b border-indigo-200 pb-1"><span>Under Review:</span> <span className="font-bold">{stats.under_review}</span></p>
              <p className="flex justify-between border-b border-indigo-200 pb-1"><span>Shortlisted:</span> <span className="font-bold">{stats.shortlisted}</span></p>
              <p className="flex justify-between border-b border-indigo-200 pb-1"><span>Awarded:</span> <span className="font-bold">{stats.awarded}</span></p>
              <p className="flex justify-between border-b border-indigo-200 pb-1"><span>Rejected:</span> <span className="font-bold">{stats.rejected}</span></p>
              <p className="flex justify-between font-semibold mt-2 pt-2 border-t border-indigo-300"><span>Average Score:</span> <span>{stats.average_score?.toFixed(1) || "N/A"}</span></p>
            </div>
          </div>
        </div>
      )}

      {/* Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50 overflow-y-auto">
          <div className="bg-white rounded-xl shadow-xl p-6 w-full max-w-lg my-8">
            <h3 className="text-xl font-bold mb-4">{isEditing ? "Edit Scholarship" : "New Scholarship"}</h3>
            <form onSubmit={handleSave} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Title</label>
                <input required value={form.title} onChange={e => setForm({...form, title: e.target.value})} className="w-full border rounded px-3 py-2 text-sm" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Amount</label>
                  <input type="number" required value={form.amount} onChange={e => setForm({...form, amount: e.target.value})} className="w-full border rounded px-3 py-2 text-sm" />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Deadline</label>
                  <input type="date" required value={form.deadline} onChange={e => setForm({...form, deadline: e.target.value})} className="w-full border rounded px-3 py-2 text-sm" />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Field</label>
                <input required value={form.field} onChange={e => setForm({...form, field: e.target.value})} className="w-full border rounded px-3 py-2 text-sm" />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Eligibility</label>
                <textarea required rows={2} value={form.eligibility} onChange={e => setForm({...form, eligibility: e.target.value})} className="w-full border rounded px-3 py-2 text-sm"></textarea>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Description (optional)</label>
                <textarea rows={3} value={form.description} onChange={e => setForm({...form, description: e.target.value})} className="w-full border rounded px-3 py-2 text-sm"></textarea>
              </div>
              <div className="flex gap-3 justify-end pt-4 border-t">
                <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 text-slate-600 bg-slate-100 hover:bg-slate-200 rounded">Cancel</button>
                <button type="submit" className="px-4 py-2 bg-blue-600 text-white hover:bg-blue-700 rounded">Save</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
