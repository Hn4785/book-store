import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { orderApi } from "../../api/orderApi";
import type { OrderSummary } from "../../types/order";
import { formatVnd, formatDate, statusLabel } from "../../utils/format";
import { Loading } from "../../components/feedback/Loading";
import { ErrorState } from "../../components/feedback/ErrorState";
import { EmptyState } from "../../components/feedback/EmptyState";

export default function OrderListPage() {
  const [orders, setOrders] = useState<OrderSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  useEffect(() => { orderApi.list().then(data => setOrders(data.results)).catch(err => setError(err instanceof Error ? err.message : "Không tải được đơn hàng.")).finally(() => setLoading(false)); }, []);
  return <section className="page"><div className="container"><div className="page-heading"><div><p className="eyebrow">THEO DÕI MUA HÀNG</p><h1>Đơn hàng của tôi</h1></div></div>{loading ? <Loading /> : error ? <ErrorState message={error} /> : !orders.length ? <EmptyState title="Bạn chưa có đơn hàng nào" description="Đơn hàng của bạn sẽ xuất hiện tại đây sau khi đặt mua." /> : <div className="table-wrap"><table><thead><tr><th>Mã đơn</th><th>Ngày tạo</th><th>Trạng thái</th><th>Tổng tiền</th><th></th></tr></thead><tbody>{orders.map(order => <tr key={order.id}><td><strong>{order.order_code}</strong></td><td>{formatDate(order.created_at)}</td><td><span className={`status status-${order.status === "COMPLETED" ? "success" : order.status === "CANCELED" ? "danger" : "warning"}`}>{statusLabel(order.status)}</span></td><td>{formatVnd(order.total)}</td><td><Link className="btn btn-outline btn-small" to={`/orders/${order.id}`}>Chi tiết</Link></td></tr>)}</tbody></table></div>}</div></section>;
}
