import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import LoginPage from "./pages/login/LoginPage";
import RegisterPage from "./pages/register/RegisterPage";
import ScholarshipsPage from "./pages/student/ScholarshipsPage";
import ScholarshipDetailPage from "./pages/student/ScholarshipDetailPage";
import ApplicationPage from "./pages/student/ApplicationPage";
import StudentDashboard from "./pages/student/StudentDashboard";
import ReviewerDashboard from "./pages/reviewer/ReviewerDashboard";
import AdminDashboard from "./pages/admin/AdminDashboard";
import ReviewerRequestPage from "./pages/reviewer/ReviewerRequestPage";
import StudentProfilePage from "./pages/student/StudentProfilePage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/"                   element={<LoginPage />} />
        <Route path="/register"           element={<RegisterPage />} />
        <Route path="/scholarships"       element={<ScholarshipsPage />} />
        <Route path="/scholarships/:id"   element={<ScholarshipDetailPage />} />
        <Route path="/apply/:scholarshipId" element={<ApplicationPage />} />
        <Route path="/my-applications"    element={<StudentDashboard />} />
        <Route path="/reviewer"           element={<ReviewerDashboard />} />
        <Route path="/admin"              element={<AdminDashboard />} />
        <Route path="/reviewer-request"   element={<ReviewerRequestPage />} />
        <Route path="/profile"            element={<StudentProfilePage />} />
        <Route path="*"                   element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
