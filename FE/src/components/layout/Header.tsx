import { BookOpen, ShoppingCart, UserRound, LogOut, ShieldCheck } from "lucide-react";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";

export function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  async function handleLogout() {
    await logout();
    navigate("/");
  }
  const navClass = ({ isActive }: { isActive: boolean }) => `nav-link${isActive ? " active" : ""}`;
  return <header className="site-header">
    <div className="container header-inner">
      <Link to="/" className="brand"><span className="brand-icon"><BookOpen size={23} /></span><span>Book<span>Shop</span><small>Đọc sách, mở tương lai</small></span></Link>
      <nav className="main-nav" aria-label="Điều hướng chính">
        <NavLink className={navClass} to="/">Sách</NavLink>
        {user && user.role === "CUSTOMER" && <NavLink className={navClass} to="/cart"><ShoppingCart size={16} /> Giỏ hàng</NavLink>}
        {user && user.role === "CUSTOMER" && <NavLink className={navClass} to="/orders">Đơn hàng</NavLink>}
        {user?.role === "ADMIN" && <NavLink className={navClass} to="/admin"><ShieldCheck size={16} /> Quản trị</NavLink>}
      </nav>
      <div className="header-actions">
        {user ? <>
          <Link className="user-chip" to="/profile"><UserRound size={16} /><span>{user.username}</span></Link>
          <button className="btn btn-outline btn-small" onClick={() => void handleLogout()}><LogOut size={15} /> Đăng xuất</button>
        </> : <>
          <Link className="header-login" to="/login">Đăng nhập</Link>
          <Link className="btn btn-primary btn-small" to="/register">Đăng ký</Link>
        </>}
      </div>
    </div>
  </header>;
}
