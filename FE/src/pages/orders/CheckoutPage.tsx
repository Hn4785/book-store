import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { orderApi } from "../../api/orderApi";
import { ApiError } from "../../types/api";

export default function CheckoutPage() {
  const [shipping_name, setName] = useState("");
  const [shipping_phone, setPhone] = useState("");
  const [shipping_address, setAddress] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const navigate = useNavigate();

  async function submit(event: React.FormEvent) {
    event.preventDefault(); setError(""); setBusy(true);
    try {
      const order = await orderApi.create({ shipping_name: shipping_name.trim(), shipping_phone: shipping_phone.trim(), shipping_address: shipping_address.trim() });
      navigate(`/orders/${order.id}`, { state: { created: true } });
    } catch (err) { setError(err instanceof ApiError ? err.message : "Không thể tạo đơn hàng."); }
    finally { setBusy(false); }
  }
  return <section className="page"><div className="container"><div className="page-heading"><div><p className="eyebrow">HOÀN TẤT ĐẶT HÀNG</p><h1>Thông tin nhận hàng</h1><p className="muted">BookShop MVP không tích hợp thanh toán trực tuyến.</p></div></div><form className="form-card card checkout-form" onSubmit={submit}>
    {error && <div className="alert alert-error" role="alert">{error}</div>}
    <div className="field"><label htmlFor="shipping_name">Tên người nhận</label><input id="shipping_name" required minLength={2} maxLength={100} value={shipping_name} onChange={e => setName(e.target.value)} /></div>
    <div className="field"><label htmlFor="shipping_phone">Số điện thoại</label><input id="shipping_phone" required minLength={8} maxLength={15} pattern="^\+?[0-9]{8,14}$" title="Nhập 8–15 chữ số, có thể có dấu + ở đầu" value={shipping_phone} onChange={e => setPhone(e.target.value)} /></div>
    <div className="field"><label htmlFor="shipping_address">Địa chỉ nhận hàng</label><textarea id="shipping_address" required minLength={5} maxLength={255} value={shipping_address} onChange={e => setAddress(e.target.value)} /></div>
    <p className="muted">Giá và tồn kho sẽ được backend kiểm tra lại khi tạo đơn.</p>
    <button className="btn btn-primary form-submit" disabled={busy}>{busy ? "Đang tạo đơn..." : "Xác nhận đặt hàng"}</button><Link className="back-link centered" to="/cart">Quay lại giỏ hàng</Link>
  </form></div></section>;
}
