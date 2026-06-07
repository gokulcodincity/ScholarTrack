import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import DashboardLayout from "../../components/DashboardLayout";
import Loader from "../../components/Loader";
import ErrorMessage from "../../components/ErrorMessage";
import { getScholarships } from "../../services/scholarshipService";

export default function ScholarshipsPage() {
  const [scholarships, setScholarships] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Filter state
  const [field, setField] = useState("");
  const [minAmount, setMinAmount] = useState("");
  const [deadline, setDeadline] = useState("");

  const fetchScholarships = async () => {
    setLoading(true);
    setError("");
    try {
      const params = {};
      if (field) params.field = field;
      if (minAmount) params.min_amount = minAmount;
      if (deadline) params.deadline_before = deadline;
      const { data } = await getScholarships(params);
      setScholarships(data);
    } catch {
      setError("Failed to load scholarships. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchScholarships(); }, []);

  const handleFilter = (e) => {
    e.preventDefault();
    fetchScholarships();
  };

  const handleReset = () => {
    setField(""); setMinAmount(""); setDeadline("");
    setTimeout(fetchScholarships, 0);
  };

  const statusColor = (deadline) => {
    const days = Math.ceil((new Date(deadline) - new Date()) / 86400000);
    if (days < 0) return "text-red-500";
    if (days <= 7) return "text-orange-500";
    return "text-green-600";
  };

  return (
    <DashboardLayout title="Discover Scholarships">
      <div className="py-8 px-4">
        <div className="max-w-6xl mx-auto">

          <h1 className="text-3xl font-bold text-slate-800 mb-1">Scholarships</h1>
          <p className="text-slate-500 mb-6">Browse and filter scholarships by field, amount, or deadline.</p>

          {/* Filter Bar */}
          <form onSubmit={handleFilter} className="bg-white rounded-xl shadow p-4 mb-8 flex flex-wrap gap-3 items-end">
            <div className="flex-1 min-w-[140px]">
              <label className="block text-xs font-medium text-slate-500 mb-1">Field</label>
              <input
                value={field}
                onChange={(e) => setField(e.target.value)}
                placeholder="e.g. Engineering"
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div className="flex-1 min-w-[140px]">
              <label className="block text-xs font-medium text-slate-500 mb-1">Min Amount (₹)</label>
              <input
                type="number"
                value={minAmount}
                onChange={(e) => setMinAmount(e.target.value)}
                placeholder="e.g. 10000"
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div className="flex-1 min-w-[140px]">
              <label className="block text-xs font-medium text-slate-500 mb-1">Deadline Before</label>
              <input
                type="date"
                value={deadline}
                onChange={(e) => setDeadline(e.target.value)}
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div className="flex gap-2">
              <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition">
                Filter
              </button>
              <button type="button" onClick={handleReset} className="border border-slate-200 text-slate-600 hover:bg-slate-50 px-4 py-2 rounded-lg text-sm font-medium transition">
                Reset
              </button>
            </div>
          </form>

          {/* States */}
          {loading && <Loader />}
          {error && <ErrorMessage message={error} />}

          {/* Grid */}
          {!loading && !error && (
            scholarships.length === 0 ? (
              <p className="text-center text-slate-500 py-16">No scholarships found. Try changing the filters.</p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {scholarships.map((s) => (
                  <div key={s.id} className="bg-white rounded-xl shadow hover:shadow-md transition p-6 flex flex-col justify-between">
                    <div>
                      <span className="text-xs font-semibold bg-blue-50 text-blue-600 px-2 py-1 rounded-full">{s.field}</span>
                      <h2 className="text-lg font-bold text-slate-800 mt-3 mb-2">{s.title}</h2>
                      <p className="text-slate-500 text-sm mb-4 line-clamp-2">{s.eligibility}</p>
                      <div className="text-sm space-y-1">
                        <p className="text-slate-700 font-medium">₹{s.amount.toLocaleString()}</p>
                        <p className={`font-medium ${statusColor(s.deadline)}`}>
                          Deadline: {s.deadline}
                        </p>
                      </div>
                    </div>
                    <Link
                      to={`/scholarships/${s.id}`}
                      className="mt-5 block text-center bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm font-medium transition"
                    >
                      View & Apply
                    </Link>
                  </div>
                ))}
              </div>
            )
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}
