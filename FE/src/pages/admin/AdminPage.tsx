import { useEffect, useState } from "react";
import { http } from "../../api/http";
import type { Book } from "../../types/book";
import type { PaginatedResponse } from "../../types/api";
import type { OrderSummary, OrderStatus } from "../../types/order";
import { formatVnd, statusLabel } from "../../utils/format";
import { Loading } from "../../components/feedback/Loading";
import { ErrorState } from "../../components/feedback/ErrorState";

export default function AdminPage() {
  const [tab, setTab] = useState<"books" | "orders">("books");
  const [books, setBooks] = useState<Book[]>([]);
  const [orders, setOrders] = useState<OrderSummary[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [title, setTitle] = useState("");
  const [author, setAuthor] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");
  const [stock, setStock] = useState("0");
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState("");

  async function load() {
    setLoading(true); setError("");
    try {
      const [bookData, orderData] = await Promise.all([
        http.get<PaginatedResponse<Book>>("admin/books?page=1&page_size=100"),
        http.get<PaginatedResponse<OrderSummary>>("admin/orders?page=1&page_size=100"),
      ]);
      setBooks(bookData.results); setOrders(orderData.results);
    } catch (err) { setError(err instanceof Error ? err.message : "Không tải được dữ liệu quản trị."); }
    finally { setLoading(false); }
  }
  useEffect(() => { void load(); }, []);

  async function createBook(event: React.FormEvent) {
    event.preventDefault(); setBusy(true); setError(""); setNotice("");
    try {
      await http.post<Book>("admin/books", { title: title.trim(), author: author.trim(), description: description.trim(), price, stock: Number(stock) });
      setTitle(""); setAuthor(""); setDescription(""); setPrice(""); setStock("0"); setNotice("Đã tạo sách."); await load();
    } catch (err) { setError(err instanceof Error ? err.message : "Không tạo được sách."); }
    finally { setBusy(false); }
  }
  async function deactivate(book: Book) {
    if (!window.confirm(`Ngừng bán sách “${book.title}”?`)) return;
    try { await http.post(`admin/books/${book.id}/deactivate`, {}); setNotice("Đã ngừng bán sách."); await load(); }
    catch (err) { setError(err instanceof Error ? err.message : "Không thể ngừng bán sách."); }
  }
  async function updateStatus(order: OrderSummary, status: OrderStatus) {
    try { await http.patch(`admin/orders/${order.id}/status`, { status }); setNotice(`Đã cập nhật đơn ${order.order_code}.`); await load(); }
    catch (err) { setError(err instanceof Error ? err.message : "Không cập nhật được trạng thái."); }
  }

  return <section className="page"><div className="container"><div className="page-heading"><div><p className="eyebrow">ADMIN CONSOLE</p><h1>Quản trị BookShop</h1><p className="muted">Quản lý danh mục sách và xử lý đơn hàng.</p></div></div>
    <div className="admin-tabs"><button className={`btn ${tab === "books" ? "btn-primary" : "btn-outline"}`} onClick={() => setTab("books")}>Quản lý sách</button><button className={`btn ${tab === "orders" ? "btn-primary" : "btn-outline"}`} onClick={() => setTab("orders")}>Quản lý đơn hàng</button></div>
    {notice && <div className="alert alert-success">{notice}</div>}{error && <ErrorState message={error} onRetry={() => void load()} />}{loading ? <Loading /> : tab === "books" ? <div className="admin-grid"><form className="card panel" onSubmit={createBook}><h2>Thêm sách mới</h2><div className="field"><label htmlFor="title">Tên sách</label><input id="title" required maxLength={200} value={title} onChange={e => setTitle(e.target.value)} /></div><div className="field"><label htmlFor="author">Tác giả</label><input id="author" required maxLength={200} value={author} onChange={e => setAuthor(e.target.value)} /></div><div className="field"><label htmlFor="description">Mô tả</label><textarea id="description" maxLength={5000} value={description} onChange={e => setDescription(e.target.value)} /></div><div className="field"><label htmlFor="price">Giá (VND)</label><input id="price" required type="number" min="0" step="0.01" value={price} onChange={e => setPrice(e.target.value)} /></div><div className="field"><label htmlFor="stock">Tồn kho</label><input id="stock" required type="number" min="0" step="1" value={stock} onChange={e => setStock(e.target.value)} /></div><button className="btn btn-primary" disabled={busy}>{busy ? "Đang lưu..." : "Tạo sách"}</button></form><div className="table-wrap"><table><thead><tr><th>Sách</th><th>Giá</th><th>Tồn</th><th>Trạng thái</th><th></th></tr></thead><tbody>{books.map(book => <tr key={book.id}><td><strong>{book.title}</strong><br /><small>{book.author}</small></td><td>{formatVnd(book.price)}</td><td>{book.stock}</td><td>{book.is_active ? "Đang bán" : "Ngừng bán"}</td><td>{book.is_active && <button className="btn btn-outline btn-small" onClick={() => void deactivate(book)}>Ngừng bán</button>}</td></tr>)}</tbody></table></div></div> : <div className="table-wrap"><table><thead><tr><th>Mã đơn</th><th>Tổng tiền</th><th>Trạng thái</th><th>Cập nhật trạng thái</th></tr></thead><tbody>{orders.map(order => <tr key={order.id}><td><strong>{order.order_code}</strong></td><td>{formatVnd(order.total)}</td><td>{statusLabel(order.status)}</td><td><select aria-label={`Trạng thái đơn ${order.order_code}`} value={order.status} onChange={e => void updateStatus(order, e.target.value as OrderStatus)} disabled={order.status === "COMPLETED" || order.status === "CANCELED"}>{(["PENDING", "CONFIRMED", "SHIPPING", "COMPLETED", "CANCELED"] as OrderStatus[]).map(status => <option key={status} value={status}>{statusLabel(status)}</option>)}</select></td></tr>)}</tbody></table></div>}
  </div></section>;
}
