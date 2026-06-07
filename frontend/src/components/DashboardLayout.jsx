import { useState, useEffect } from "react";
import Sidebar from "./Sidebar";
import Navbar from "./Navbar";
import { getUserById } from "../services/userService";

function getPayload() {
  const token = localStorage.getItem("token");
  if (!token) return null;
  try { return JSON.parse(atob(token.split(".")[1])); } catch { return null; }
}

export default function DashboardLayout({ children, title }) {
  const payload = getPayload();
  const userId = payload?.id;
  const role = payload?.role;

  const [userName, setUserName] = useState("User");

  useEffect(() => {
    if (userId) {
      getUserById(userId)
        .then(({ data }) => {
          if (data && data.name) setUserName(data.name);
        })
        .catch(console.error);
    }
  }, [userId]);

  // If no user is logged in, just show normal Navbar and content
  if (!role) {
    return (
      <div className="min-h-screen bg-slate-50 font-sans flex flex-col">
        <Navbar />
        <main className="flex-1">
          {children}
        </main>
      </div>
    );
  }

  // Common Layout for Logged In Users
  return (
    <div className="flex h-screen bg-slate-50 font-sans overflow-hidden">
      <Sidebar />
      
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Top Header */}
        <header className="bg-white border-b border-slate-200 px-8 py-4 flex justify-between items-center z-10 shrink-0 shadow-sm">
          <h1 className="text-xl font-bold text-slate-800 tracking-tight">
            {title || "Scholarship Management System"}
          </h1>
          <div className="flex items-center gap-3">
            <span className="text-sm font-medium text-slate-500">Welcome, <span className="text-blue-600 font-bold">{userName}</span></span>
            <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-bold">
              {userName.charAt(0).toUpperCase()}
            </div>
          </div>
        </header>

        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto relative">
          {children}
        </main>
      </div>
    </div>
  );
}
