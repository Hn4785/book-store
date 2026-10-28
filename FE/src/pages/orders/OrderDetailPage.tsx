import { useEffect, useState } from "react";
import { Link, useLocation, useParams } from "react-router-dom";
import { orderApi } from "../../api/orderApi";
import type { OrderDetail } from "../../types/order";
import { formatVnd, formatDate, statusLabel } from "../../utils/format";
import { Loading } from "../../components/feedback/Loading";
import { ErrorState } from "../../components/feedback/ErrorState";

export default function OrderDetailPage() {
  const { id } = useParams();
  const location = useLocation();
  const [order, setOrder] = useState<OrderDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState((location.state as { created?: boolean } | null)?.created ? "Đặt hàng thành công!" : "");
  async function load() {
    setLoading(true); setError("");
    try { setOrder(await orderApi.detail(Number(id))); }
    catch (err) { setError(err instanceof Error ? err.message : "Không tải được đơn hàng."); }
    finally { setLoading(false); }
  }
  useEffect(() => { void load(); }, [id]);
  async function cancel() {
    if (!order || !window.confirm("Bạn chắc chắn muốn hủy đơn hàng này?")) return;
    setBusy(true); setError("");
    try { await orderApi.cancel(order.id); setNotice("Đã gửi yêu cầu hủy đơn."); await load(); }
    catch (err) { setError(err instanceof Error ? err.message : "Không thể hủy đơn."); }
    finally { setBusy(false); }
  }
  return <section className="page"><div className="container"><div className="page-heading"><div><p className="eyebrow">CHI TIẾT ĐƠN HÀNG</p><h1>Đơn hàng #{id}</h1></div><Link className="btn btn-outline" to="/orders">Danh sách đơn</Link></div>{loading ? <Loading /> : error && !order ? <ErrorState message={error} /> : order && <div className="order-detail-layout">
    <div className="card panel"><div className="order-title-row"><div><h2>{order.order_code}</h2><p className="muted">Tạo lúc {formatDate(order.created_at)}</p></div><span className={`status status-${order.status === "COMPLETED" ? "success" : order.status === "CANCELED" ? "danger" : "warning"}`}>{statusLabel(order.status)}</span></div>{notice && <div className="alert alert-success">{notice}</div>}{error && <ErrorState message={error} />}
      <h3>Sản phẩm</h3><div className="order-lines">{order.items.map((item, index) => <div className="order-line" key={`${item.book_id}-${index}`}><div><strong>{item.title}</strong><p className="muted">{formatVnd(item.unit_price)} × {item.quantity}</p></div><strong>{formatVnd(item.subtotal)}</strong></div>)}</div><div className="summary-row summary-total"><span>Tổng đơn</span><strong>{formatVnd(order.total)}</strong></div>{order.status === "PENDING" && <button className="btn btn-danger" disabled={busy} onClick={() => void cancel()}>{busy ? "Đang xử lý..." : "Hủy đơn hàng"}</button>}
    </div><aside className="card panel"><h3>Thông tin nhận hàng</h3><p><span className="muted">Người nhận</span><br /><strong>{order.shipping_name}</strong></p><p><span className="muted">Số điện thoại</span><br /><strong>{order.shipping_phone}</strong></p><p><span className="muted">Địa chỉ</span><br /><strong>{order.shipping_address}</strong></p></aside>
  </div>}</div></section>;
}
