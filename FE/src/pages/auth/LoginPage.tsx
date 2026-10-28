import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { ApiError } from "../../types/api";
import { useAuth } from "../../contexts/AuthContext";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = (location.state as { from?: { pathname?: string } } | null)?.from?.pathname || "/";

  async function submit(event: React.FormEvent) {
    event.preventDefault(); setError(""); setBusy(true);
    try { await login({ email: email.trim().toLowerCase(), password }); navigate(from, { replace: true }); }
    catch (err) { setError(err instanceof ApiError ? err.message : "Đăng nhập thất bại."); }
    finally { setBusy(false); }
  }

  return <section className="page"><div className="container"><form className="form-card card" onSubmit={submit}>
    <p className="eyebrow">CHÀO MỪNG TRỞ LẠI</p><h1>Đăng nhập</h1><p className="muted">Đăng nhập để quản lý giỏ hàng và đơn hàng của bạn.</p>
    {error && <div className="alert alert-error" role="alert">{error}</div>}
    <div className="field"><label htmlFor="email">Email</label><input id="email" type="email" autoComplete="email" required value={email} onChange={e => setEmail(e.target.value)} placeholder="ban@email.com" /></div>
    <div className="field"><label htmlFor="password">Mật khẩu</label><input id="password" type="password" autoComplete="current-password" required value={password} onChange={e => setPassword(e.target.value)} placeholder="Nhập mật khẩu" /></div>
    <button className="btn btn-primary form-submit" type="submit" disabled={busy}>{busy ? "Đang đăng nhập..." : "Đăng nhập"}</button>
    <p className="form-switch">Chưa có tài khoản? <Link to="/register">Đăng ký ngay</Link></p>
  </form></div></section>;
}
