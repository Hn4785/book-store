import { useEffect, useState } from "react";
import { ArrowLeft, BookOpen, ShoppingCart } from "lucide-react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { bookApi } from "../../api/bookApi";
import { cartApi } from "../../api/cartApi";
import { useAuth } from "../../contexts/AuthContext";
import type { Book } from "../../types/book";
import { formatVnd } from "../../utils/format";
import { Loading } from "../../components/feedback/Loading";
import { ErrorState } from "../../components/feedback/ErrorState";

export default function BookDetailPage() {
  const { id } = useParams();
  const [book, setBook] = useState<Book | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    let alive = true;
    setLoading(true);
    bookApi.detail(Number(id)).then(data => { if (alive) setBook(data); })
      .catch(err => { if (alive) setError(err instanceof Error ? err.message : "Không tải được sách."); })
      .finally(() => { if (alive) setLoading(false); });
    return () => { alive = false; };
  }, [id]);

  async function add() {
    if (!book) return;
    if (!user) { navigate("/login", { state: { from: { pathname: "/cart" } } }); return; }
    if (user.role !== "CUSTOMER") { setNotice("Tài khoản Admin không sử dụng chức năng giỏ hàng."); return; }
    try { await cartApi.add({ book_id: book.id, quantity: 1 }); setNotice("Đã thêm sách vào giỏ hàng."); }
    catch (err) { setNotice(err instanceof Error ? err.message : "Không thể thêm sách."); }
  }

  return <section className="page"><div className="container">
    <Link to="/" className="back-link"><ArrowLeft size={17} /> Quay lại danh mục</Link>
    {loading ? <Loading /> : error ? <ErrorState message={error} /> : book && <div className="book-detail card">
      <div className="detail-cover"><div className="cover-art cover-art-large"><BookOpen size={68} /><span>BOOKSHOP</span></div></div>
      <div className="detail-content"><p className="eyebrow">CHI TIẾT SÁCH</p><h1>{book.title}</h1><p className="detail-author">Tác giả: {book.author}</p><div className="detail-price">{formatVnd(book.price)}</div><p className="detail-stock">{book.stock > 0 ? <span className="status status-success">Còn hàng · {book.stock} cuốn</span> : <span className="status status-danger">Tạm hết hàng</span>}</p><div className="detail-description"><h3>Mô tả sách</h3><p>{book.description || "Chưa có mô tả cho cuốn sách này."}</p></div>{notice && <div className="alert alert-success">{notice}</div>}<button className="btn btn-primary detail-add" disabled={book.stock < 1 || !book.is_active} onClick={() => void add()}><ShoppingCart size={18} /> Thêm vào giỏ hàng</button></div>
    </div>}
  </div></section>;
}
