import { useEffect, useState } from "react";
import { getAllUsers, getUserById } from "../../services/userService";
import Loader from "../../components/Loader";
import ErrorMessage from "../../components/ErrorMessage";

export default function AdminUsersPanel() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedUser, setSelectedUser] = useState(null);
  const [roleFilter, setRoleFilter] = useState("ALL");

  const filteredUsers = roleFilter === "ALL" 
    ? users 
    : users.filter(u => u.role === roleFilter);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const { data } = await getAllUsers();
      setUsers(data);
    } catch (err) {
      setError("Failed to fetch users");
    } finally {
      setLoading(false);
    }
  };

  const viewUser = async (id) => {
    try {
      const { data } = await getUserById(id);
      setSelectedUser(data);
    } catch (err) {
      alert("Failed to fetch user details");
    }
  };

  if (loading) return <Loader />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 border-b pb-4 gap-4">
        <h2 className="text-2xl font-semibold">All System Users</h2>
        <select
          value={roleFilter}
          onChange={(e) => setRoleFilter(e.target.value)}
          className="border border-slate-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white shadow-sm"
        >
          <option value="ALL">All Roles</option>
          <option value="STUDENT">Student</option>
          <option value="REVIEWER">Reviewer</option>
          <option value="PENDING_REVIEWER">Pending Reviewer</option>
          <option value="ADMIN">Admin</option>
        </select>
      </div>
      
      {filteredUsers.length === 0 ? (
        <p className="text-slate-500">No users found matching the filter.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredUsers.map((user) => (
            <div key={user.id} className="border border-slate-200 rounded-xl p-4 hover:shadow-md transition bg-white flex flex-col justify-between">
              <div>
                <h3 className="text-lg font-bold text-slate-800">{user.name}</h3>
                <p className="text-slate-500 text-sm mb-2">{user.email}</p>
                <span className="inline-block bg-slate-100 text-slate-700 text-xs font-medium px-2 py-1 rounded">
                  {user.role}
                </span>
              </div>
              <button 
                onClick={() => viewUser(user.id)}
                className="mt-4 text-sm text-blue-600 hover:underline text-left"
              >
                View Details
              </button>
            </div>
          ))}
        </div>
      )}

      {selectedUser && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-xl p-6 w-full max-w-md">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold">User Details</h3>
              <button onClick={() => setSelectedUser(null)} className="text-slate-400 hover:text-slate-800">✕</button>
            </div>
            <div className="space-y-3 bg-slate-50 p-4 rounded-lg text-sm">
              <p><span className="font-semibold text-slate-600">ID:</span> {selectedUser.id}</p>
              <p><span className="font-semibold text-slate-600">Name:</span> {selectedUser.name}</p>
              <p><span className="font-semibold text-slate-600">Email:</span> {selectedUser.email}</p>
              <p><span className="font-semibold text-slate-600">Role:</span> {selectedUser.role}</p>
              <p><span className="font-semibold text-slate-600">Active:</span> {selectedUser.is_active ? "Yes" : "No"}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
