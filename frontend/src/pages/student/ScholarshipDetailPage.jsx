import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import DashboardLayout from "../../components/DashboardLayout";
import Loader from "../../components/Loader";
import ErrorMessage from "../../components/ErrorMessage";
import { getScholarshipById } from "../../services/scholarshipService";

function ScholarshipDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [scholarship, setScholarship] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchScholarship();
  }, [id]);

  const fetchScholarship = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await getScholarshipById(id);
      setScholarship(response.data);
    } catch (error) {
      console.error("Failed to fetch scholarship", error);
      setError("Failed to load scholarship details.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Loader />;
  }

  if (error || !scholarship) {
    return (
      <DashboardLayout title="Scholarship Details">
        <div className="min-h-screen flex items-center justify-center bg-slate-50">
          <div className="w-full max-w-md"><ErrorMessage message={error || "Scholarship not found."} /></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title={scholarship.title}>
      <div className="py-10 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <h1 className="text-4xl font-bold text-slate-800 mb-6">
              {scholarship.title}
            </h1>

            <div className="grid md:grid-cols-2 gap-6 mb-8">
              <div className="bg-slate-100 p-5 rounded-xl">
                <h3 className="font-semibold text-slate-700">Amount</h3>
                <p className="text-2xl font-bold text-green-600 mt-2">
                  ₹{scholarship.amount?.toLocaleString()}
                </p>
              </div>

              <div className="bg-slate-100 p-5 rounded-xl">
                <h3 className="font-semibold text-slate-700">Deadline</h3>
                <p className="mt-2 text-slate-800">{scholarship.deadline}</p>
              </div>
            </div>

            <div className="mb-8">
              <h2 className="text-2xl font-semibold mb-3">Eligibility</h2>
              <p className="text-slate-600 leading-relaxed">
                {scholarship.eligibility}
              </p>
            </div>

            {scholarship.description && (
              <div className="mb-8">
                <h2 className="text-2xl font-semibold mb-3">Description</h2>
                <p className="text-slate-600 leading-relaxed">
                  {scholarship.description}
                </p>
              </div>
            )}

            <div className="flex flex-col sm:flex-row gap-4">
              <button
                onClick={() => navigate(`/apply/${scholarship.id}`)}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl transition font-medium"
              >
                Apply Now
              </button>

              <button
                onClick={() => navigate("/scholarships")}
                className="border border-slate-300 px-6 py-3 rounded-xl hover:bg-slate-100 font-medium text-slate-700"
              >
                Back
              </button>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default ScholarshipDetailPage;
