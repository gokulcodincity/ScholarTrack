import { useEffect, useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import api from "../services/api";
import Navbar from "../components/Navbar";

export default function VerifyEmailPage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  
  const [status, setStatus] = useState("verifying"); // verifying, success, error
  const [message, setMessage] = useState("Verifying your email address...");

  useEffect(() => {
    if (!token) {
      setStatus("error");
      setMessage("No verification token found.");
      return;
    }

    const verifyEmail = async () => {
      try {
        const response = await api.get(`/auth/verify-email?token=${token}`);
        setStatus("success");
        setMessage(response.data.message || "Your email has been successfully verified!");
      } catch (err) {
        setStatus("error");
        setMessage(err.response?.data?.detail || "Verification failed. The link may be expired or invalid.");
      }
    };

    verifyEmail();
  }, [token]);

  return (
    <>
      <Navbar />
      <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
        <div className="w-full max-w-md bg-white shadow-xl rounded-2xl p-8 text-center">
          <h1 className="text-3xl font-bold text-blue-600 mb-6">ScholarTrack</h1>
          
          {status === "verifying" && (
            <div className="text-slate-600">
              <p className="text-4xl mb-4">⏳</p>
              <h2 className="text-xl font-semibold mb-2">Please wait</h2>
              <p>{message}</p>
            </div>
          )}

          {status === "success" && (
            <div className="text-green-600">
              <p className="text-4xl mb-4">✅</p>
              <h2 className="text-xl font-semibold mb-2">Verification Complete!</h2>
              <p className="text-slate-600 mb-6">{message}</p>
              <Link to="/" className="inline-block bg-blue-600 text-white font-semibold py-2 px-6 rounded-lg hover:bg-blue-700 transition">
                Proceed to Login
              </Link>
            </div>
          )}

          {status === "error" && (
            <div className="text-red-600">
              <p className="text-4xl mb-4">❌</p>
              <h2 className="text-xl font-semibold mb-2">Verification Failed</h2>
              <p className="text-slate-600 mb-6">{message}</p>
              <Link to="/register" className="inline-block bg-slate-800 text-white font-semibold py-2 px-6 rounded-lg hover:bg-slate-900 transition">
                Back to Registration
              </Link>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
