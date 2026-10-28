import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ApiError } from "../../types/api";
import { useAuth } from "../../contexts/AuthContext";

export default function RegisterPage() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  async function submit(event: React.FormEvent) {
    event.preventDefault(); setError("");
    if (password.length < 8) { setError("Mật khẩu phải có ít nhất 8 ký tự."); return; }
    if (password !== confirm) { setError("Mật khẩu xác nhận không khớp."); return; }
    setBusy(true);
    try { await register({ username: username.trim(), email: email.trim().toLowerCase(), password }); navigate("/login", { state: { registered: true } }); }
    catch (err) { setError(err instanceof ApiError ? err.message : "Đăng ký thất bại."); }
    finally { setBusy(false); }
  }

  return <section className="page"><div className="container"><form className="form-card card" onSubmit={submit}>
    <p className="eyebrow">TẠO TÀI KHOẢN MỚI</p><h1>Đăng ký</h1><p className="muted">Tài khoản đăng ký công khai có vai trò Customer.</p>
    {error && <div className="alert alert-error" role="alert">{error}</div>}
    <div className="field"><label htmlFor="username">Tên người dùng</label><input id="username" minLength={3} maxLength={30} required value={username} onChange={e => setUsername(e.target.value)} placeholder="ten_nguoi_dung" /></div>
    <div className="field"><label htmlFor="email">Email</label><input id="email" type="email" autoComplete="email" required value={email} onChange={e => setEmail(e.target.value)} placeholder="ban@email.com" /></div>
    <div className="field"><label htmlFor="password">Mật khẩu</label><input id="password" type="password" autoComplete="new-password" minLength={8} required value={password} onChange={e => setPassword(e.target.value)} placeholder="Ít nhất 8 ký tự" /></div>
    <div className="field"><label htmlFor="confirm">Xác nhận mật khẩu</label><input id="confirm" type="password" autoComplete="new-password" required value={confirm} onChange={e => setConfirm(e.target.value)} placeholder="Nhập lại mật khẩu" /></div>
    <button className="btn btn-primary form-submit" type="submit" disabled={busy}>{busy ? "Đang tạo tài khoản..." : "Tạo tài khoản"}</button>
    <p className="form-switch">Đã có tài khoản? <Link to="/login">Đăng nhập</Link></p>
  </form></div></section>;
}
