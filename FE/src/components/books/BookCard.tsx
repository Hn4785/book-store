import { BookOpen, ShoppingCart } from "lucide-react";
import { Link } from "react-router-dom";
import type { Book } from "../../types/book";
import { formatVnd } from "../../utils/format";

export function BookCard({ book, onAdd }: { book: Book; onAdd?: (book: Book) => void }) {
  return <article className="book-card card">
    <Link to={`/books/${book.id}`} className="book-cover" aria-label={`Xem ${book.title}`}>
      <div className="cover-art"><BookOpen size={42} strokeWidth={1.4} /><span>BOOKSHOP</span></div>
    </Link>
    <div className="book-card-body">
      <p className="book-author">{book.author}</p>
      <Link to={`/books/${book.id}`}><h3>{book.title}</h3></Link>
      <strong className="book-price">{formatVnd(book.price)}</strong>
      <p className={`stock-text ${book.stock > 0 ? "" : "out-of-stock"}`}>{book.stock > 0 ? `Còn ${book.stock} cuốn` : "Tạm hết hàng"}</p>
      <div className="book-card-actions">
        <Link className="btn btn-secondary btn-small" to={`/books/${book.id}`}>Chi tiết</Link>
        {onAdd && <button className="btn btn-primary btn-small" aria-label={`Thêm ${book.title} vào giỏ`} disabled={book.stock < 1 || !book.is_active} onClick={() => onAdd(book)}><ShoppingCart size={15} /></button>}
      </div>
    </div>
  </article>;
}
