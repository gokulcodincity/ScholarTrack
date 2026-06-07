import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import Navbar from "../../components/Navbar";
import { submitReviewerRequest } from "../../services/authService";
import ErrorMessage from "../../components/ErrorMessage";

function ReviewerRequestPage() {
  const location = useLocation();
  const navigate = useNavigate();

  const userId = location.state?.user_id;

  const [formData, setFormData] = useState({
    university: "",
    department: "",
    years_of_experience: "",
    institution_email: "",
  });

  const [resumeFile, setResumeFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && !file.name.toLowerCase().endsWith(".pdf")) {
      alert("Only PDF files are accepted");
      e.target.value = "";
      return;
    }
    setResumeFile(file);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!userId) {
      alert("Session expired. Please register again.");
      navigate("/register");
      return;
    }

    if (!resumeFile) {
      alert("Please upload your resume (PDF)");
      return;
    }

    try {
      setError("");
      setLoading(true);

      // Use FormData for multipart/form-data submission
      const payload = new FormData();
      payload.append("user_id", userId);
      payload.append("university", formData.university);
      payload.append("department", formData.department);
      payload.append("years_of_experience", formData.years_of_experience);
      payload.append("institution_email", formData.institution_email);
      payload.append("resume", resumeFile);

      await submitReviewerRequest(payload);

      alert(
        "Application submitted successfully! Please wait for admin approval before logging in."
      );

      navigate("/");
    } catch (err) {
      console.error(err);
      setError(err?.response?.data?.detail || "Failed to submit request");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4 py-10">
        <div className="w-full max-w-lg bg-white shadow-xl rounded-2xl p-8">
          <h1 className="text-3xl font-bold text-blue-600 mb-1">
            Reviewer Application
          </h1>
          <p className="text-slate-500 mb-6 text-sm">
            Fill in your details. Admin will review your application before
            granting access.
          </p>

          {error && <ErrorMessage message={error} />}

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* University */}
            <div>
              <label className="block mb-1 text-sm font-medium">
                University / Institution
              </label>
              <input
                type="text"
                name="university"
                value={formData.university}
                onChange={handleChange}
                required
                className="w-full border border-slate-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g. MIT"
              />
            </div>

            {/* Department */}
            <div>
              <label className="block mb-1 text-sm font-medium">
                Department
              </label>
              <input
                type="text"
                name="department"
                value={formData.department}
                onChange={handleChange}
                required
                className="w-full border border-slate-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g. Computer Science"
              />
            </div>

            {/* Institution Email */}
            <div>
              <label className="block mb-1 text-sm font-medium">
                Institution Email
              </label>
              <input
                type="email"
                name="institution_email"
                value={formData.institution_email}
                onChange={handleChange}
                required
                className="w-full border border-slate-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g. you@university.edu"
              />
            </div>

            {/* Years of Experience */}
            <div>
              <label className="block mb-1 text-sm font-medium">
                Years of Experience
              </label>
              <input
                type="number"
                name="years_of_experience"
                value={formData.years_of_experience}
                onChange={handleChange}
                required
                min={0}
                className="w-full border border-slate-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g. 3"
              />
            </div>

            {/* Resume Upload */}
            <div>
              <label className="block mb-1 text-sm font-medium">
                Resume <span className="text-slate-400 text-xs">(PDF only)</span>
              </label>
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                required
                className="w-full border border-slate-300 rounded-lg p-2.5 text-sm text-slate-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
            >
              {loading ? "Submitting..." : "Submit Application"}
            </button>
          </form>
        </div>
      </div>
    </>
  );
}

export default ReviewerRequestPage;
