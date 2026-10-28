import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { bookApi } from "../../api/bookApi";
import { cartApi } from "../../api/cartApi";
import { useAuth } from "../../contexts/AuthContext";
import type { Book } from "../../types/book";
import { ApiError } from "../../types/api";
import { BookList } from "../../components/books/BookList";
import { BookSearch } from "../../components/books/BookSearch";
import { Pagination } from "../../components/books/Pagination";
import { Loading } from "../../components/feedback/Loading";
import { ErrorState } from "../../components/feedback/ErrorState";

const PAGE_SIZE = 10;
export default function BookListPage() {
  const [searchInput, setSearchInput] = useState("");
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [books, setBooks] = useState<Book[]>([]);
  const [count, setCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const { user } = useAuth();
  const navigate = useNavigate();

  const load = useCallback(async () => {
    setLoading(true); setError("");
    try {
      const result = await bookApi.list({ search, page, page_size: PAGE_SIZE });
      setBooks(result.results); setCount(result.count);
    } catch (err) { setError(err instanceof Error ? err.message : "Không tải được danh sách sách."); }
    finally { setLoading(false); }
  }, [search, page]);

  useEffect(() => { void load(); }, [load]);

  async function addToCart(book: Book) {
    setNotice("");
    if (!user) { navigate("/login", { state: { from: { pathname: "/cart" } } }); return; }
    if (user.role !== "CUSTOMER") { setNotice("Tài khoản Admin không sử dụng chức năng giỏ hàng."); return; }
    try { await cartApi.add({ book_id: book.id, quantity: 1 }); setNotice(`Đã thêm “${book.title}” vào giỏ hàng.`); }
    catch (err) { setNotice(err instanceof ApiError ? err.message : "Không thể thêm sách vào giỏ."); }
  }

  return <section className="page"><div className="container">
    <div className="hero"><div><span className="eyebrow">KHÔNG GIAN TRI THỨC</span><h1>Mỗi cuốn sách,<br /><em>một hành trình mới.</em></h1><p>Khám phá những cuốn sách phù hợp cho hành trình học tập và phát triển của bạn.</p></div><div className="hero-illustration"><div className="hero-book hero-book-one" /><div className="hero-book hero-book-two" /><div className="hero-book hero-book-three" /></div></div>
    <div className="page-heading"><div><h2>Danh mục sách</h2><p className="muted">Tìm kiếm theo tên sách hoặc tác giả.</p></div></div>
    <BookSearch value={searchInput} onChange={setSearchInput} onSubmit={() => { setPage(1); setSearch(searchInput.trim()); }} onClear={() => { setSearchInput(""); setSearch(""); setPage(1); }} />
    {notice && <div className="alert alert-success" role="status">{notice}</div>}
    {loading ? <Loading label="Đang tải danh sách sách..." /> : error ? <ErrorState message={error} onRetry={() => void load()} /> : <>
      <div className="results-meta">Hiển thị {books.length} / {count} đầu sách</div>
      <BookList books={books} onAdd={addToCart} />
      <Pagination page={page} pageSize={PAGE_SIZE} count={count} onChange={setPage} />
    </>}
  </div></section>;
}
