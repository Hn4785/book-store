import { useAuth } from "../../contexts/AuthContext";

export default function ProfilePage() {
  const { user } = useAuth();
  return <section className="page"><div className="container"><div className="page-heading"><div><p className="eyebrow">TÀI KHOẢN</p><h1>Thông tin cá nhân</h1></div></div><div className="profile-card card panel"><div className="profile-avatar">{user?.username.slice(0, 1).toUpperCase()}</div><div className="profile-details"><div><span className="muted">Tên người dùng</span><strong>{user?.username}</strong></div><div><span className="muted">Email</span><strong>{user?.email}</strong></div><div><span className="muted">Vai trò</span><strong>{user?.role === "ADMIN" ? "Quản trị viên (Admin)" : "Khách hàng (Customer)"}</strong></div></div></div></div></section>;
}
