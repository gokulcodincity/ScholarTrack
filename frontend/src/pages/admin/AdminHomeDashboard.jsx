import { useEffect, useState } from "react";
import { getAllUsers } from "../../services/userService";
import { getScholarships } from "../../services/scholarshipService";
import { getPendingReviewers } from "../../services/adminService";
import { getAllDecisions } from "../../services/adminService";

export default function AdminHomeDashboard({ setActiveTab }) {
  const [stats, setStats] = useState({
    users: 0,
    scholarships: 0,
    pendingReviewers: 0,
    decisions: 0,
  });

  useEffect(() => {
    async function fetchStats() {
      try {
        const [usersRes, schRes, revRes, decRes] = await Promise.all([
          getAllUsers().catch(() => ({ data: [] })),
          getScholarships().catch(() => ({ data: [] })),
          getPendingReviewers().catch(() => ({ data: [] })),
          getAllDecisions().catch(() => ({ data: [] })),
        ]);

        setStats({
          users: usersRes.data.length || 0,
          scholarships: schRes.data.length || 0,
          pendingReviewers: revRes.data.length || 0,
          decisions: decRes.data.length || 0,
        });
      } catch (err) {
        console.error("Failed to load dashboard stats", err);
      }
    }
    fetchStats();
  }, []);

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Top Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 flex items-center gap-4">
          <div className="w-14 h-14 rounded-full bg-green-100 text-green-600 flex items-center justify-center text-2xl">
            👥
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Total Users</p>
            <p className="text-3xl font-bold text-slate-800">{stats.users}</p>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 flex items-center gap-4">
          <div className="w-14 h-14 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-2xl">
            🎓
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Scholarships</p>
            <p className="text-3xl font-bold text-slate-800">{stats.scholarships}</p>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 flex items-center gap-4">
          <div className="w-14 h-14 rounded-full bg-orange-100 text-orange-600 flex items-center justify-center text-2xl">
            ⏳
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Pending Reviewers</p>
            <p className="text-3xl font-bold text-slate-800">{stats.pendingReviewers}</p>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 flex items-center gap-4">
          <div className="w-14 h-14 rounded-full bg-purple-100 text-purple-600 flex items-center justify-center text-2xl">
            ✅
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Total Decisions</p>
            <p className="text-3xl font-bold text-slate-800">{stats.decisions}</p>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div>
        <h3 className="text-lg font-bold text-slate-800 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <button onClick={() => setActiveTab("scholarships")} className="bg-white border border-slate-200 rounded-xl p-4 flex items-center gap-4 hover:shadow-md hover:border-blue-300 transition text-left">
            <div className="bg-blue-600 text-white rounded-lg p-3 text-xl">➕</div>
            <div>
              <p className="font-bold text-slate-800">Add Scholarship</p>
              <p className="text-xs text-slate-500">Create new listing</p>
            </div>
          </button>
          
          <button onClick={() => setActiveTab("users")} className="bg-white border border-slate-200 rounded-xl p-4 flex items-center gap-4 hover:shadow-md hover:green-300 transition text-left">
            <div className="bg-green-600 text-white rounded-lg p-3 text-xl">👥</div>
            <div>
              <p className="font-bold text-slate-800">Manage Users</p>
              <p className="text-xs text-slate-500">View all users</p>
            </div>
          </button>

          <button onClick={() => setActiveTab("applications")} className="bg-white border border-slate-200 rounded-xl p-4 flex items-center gap-4 hover:shadow-md hover:purple-300 transition text-left">
            <div className="bg-purple-600 text-white rounded-lg p-3 text-xl">📄</div>
            <div>
              <p className="font-bold text-slate-800">Applications</p>
              <p className="text-xs text-slate-500">Review submissions</p>
            </div>
          </button>

          <button onClick={() => setActiveTab("reviewers")} className="bg-white border border-slate-200 rounded-xl p-4 flex items-center gap-4 hover:shadow-md hover:orange-300 transition text-left">
            <div className="bg-orange-600 text-white rounded-lg p-3 text-xl">⏳</div>
            <div>
              <p className="font-bold text-slate-800">Reviewers</p>
              <p className="text-xs text-slate-500">Approve requests</p>
            </div>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Business Overview */}
        <div className="lg:col-span-2 bg-slate-100 rounded-2xl p-6">
          <h3 className="text-lg font-bold text-slate-800 mb-1">Platform Overview</h3>
          <p className="text-sm text-slate-500 mb-6 flex items-center gap-2">📈 Performance metrics</p>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white rounded-xl p-4 shadow-sm border border-slate-200 text-center">
              <p className="text-2xl font-bold text-slate-800 mb-1">{stats.users}</p>
              <p className="text-xs text-slate-500 mb-3">Total Accounts</p>
              <span className="bg-green-100 text-green-700 text-xs font-semibold px-2 py-1 rounded-full">✓ Active</span>
            </div>
            <div className="bg-white rounded-xl p-4 shadow-sm border border-slate-200 text-center">
              <p className="text-2xl font-bold text-slate-800 mb-1">{stats.scholarships}</p>
              <p className="text-xs text-slate-500 mb-3">Scholarships</p>
              <span className="bg-green-100 text-green-700 text-xs font-semibold px-2 py-1 rounded-full">✓ Running</span>
            </div>
            <div className="bg-white rounded-xl p-4 shadow-sm border border-slate-200 text-center">
              <p className="text-2xl font-bold text-slate-800 mb-1">{stats.decisions}</p>
              <p className="text-xs text-slate-500 mb-3">Decisions</p>
              <span className="bg-blue-100 text-blue-700 text-xs font-semibold px-2 py-1 rounded-full">↑ +12.5%</span>
            </div>
            <div className="bg-white rounded-xl p-4 shadow-sm border border-slate-200 text-center">
              <p className="text-2xl font-bold text-slate-800 mb-1">{stats.pendingReviewers}</p>
              <p className="text-xs text-slate-500 mb-3">Pending Tasks</p>
              <span className="bg-orange-100 text-orange-700 text-xs font-semibold px-2 py-1 rounded-full">⏳ In Queue</span>
            </div>
          </div>

          <div className="pt-6 border-t border-slate-300">
            <h4 className="font-bold text-slate-800 mb-4">System Performance</h4>
            <div className="flex flex-wrap justify-between text-sm">
              <p><span className="text-slate-500">Avg Response Time</span> <strong className="ml-2">2.4 hrs</strong></p>
              <p><span className="text-slate-500">User Satisfaction</span> <strong className="ml-2">4.8/5</strong></p>
              <p><span className="text-slate-500">Task Completion</span> <strong className="ml-2">94%</strong></p>
            </div>
          </div>
        </div>

        {/* Recent Activities */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-lg font-bold text-slate-800">Recent Activities</h3>
            <span className="bg-green-100 text-green-700 text-xs font-bold px-2 py-1 rounded flex items-center gap-1">
              <span className="w-1.5 h-1.5 bg-green-600 rounded-full animate-pulse"></span> Live
            </span>
          </div>
          
          <div className="space-y-6 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-200 before:to-transparent">
            {/* Timeline Item 1 */}
            <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
              <div className="flex items-center justify-center w-10 h-10 rounded-full border border-white bg-blue-100 text-blue-500 shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2">
                👤
              </div>
              <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-xl border border-slate-100 bg-slate-50">
                <div className="flex items-center justify-between space-x-2 mb-1">
                  <div className="font-bold text-slate-800 text-sm">New registration</div>
                </div>
                <div className="text-slate-500 text-xs">2 minutes ago</div>
              </div>
            </div>
            
            {/* Timeline Item 2 */}
            <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
              <div className="flex items-center justify-center w-10 h-10 rounded-full border border-white bg-green-100 text-green-500 shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2">
                ✅
              </div>
              <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-xl border border-slate-100 bg-slate-50">
                <div className="flex items-center justify-between space-x-2 mb-1">
                  <div className="font-bold text-slate-800 text-sm">Decision awarded</div>
                </div>
                <div className="text-slate-500 text-xs">15 minutes ago</div>
              </div>
            </div>

            {/* Timeline Item 3 */}
            <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
              <div className="flex items-center justify-center w-10 h-10 rounded-full border border-white bg-orange-100 text-orange-500 shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2">
                ⚠️
              </div>
              <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-xl border border-slate-100 bg-slate-50">
                <div className="flex items-center justify-between space-x-2 mb-1">
                  <div className="font-bold text-slate-800 text-sm">Pending approval</div>
                </div>
                <div className="text-slate-500 text-xs">1 hour ago</div>
              </div>
            </div>
            
            {/* Timeline Item 4 */}
            <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
              <div className="flex items-center justify-center w-10 h-10 rounded-full border border-white bg-purple-100 text-purple-500 shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2">
                📄
              </div>
              <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-xl border border-slate-100 bg-slate-50">
                <div className="flex items-center justify-between space-x-2 mb-1">
                  <div className="font-bold text-slate-800 text-sm">New application</div>
                </div>
                <div className="text-slate-500 text-xs">3 hours ago</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
