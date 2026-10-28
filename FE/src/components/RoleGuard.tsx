import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { Loading } from "./feedback/Loading";

export default function RoleGuard({ role }: { role: "ADMIN" | "CUSTOMER" }) {
  const { user, loading } = useAuth();
  if (loading) return <Loading label="Đang kiểm tra quyền..." />;
  if (!user) return <Navigate to="/login" replace />;
  if (user.role !== role) return <Navigate to="/" replace />;
  return <Outlet />;
}
