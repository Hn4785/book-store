import type { Book } from "../../types/book";
import { BookCard } from "./BookCard";
import { EmptyState } from "../feedback/EmptyState";

export function BookList({ books, onAdd }: { books: Book[]; onAdd?: (book: Book) => void }) {
  if (!books.length) return <EmptyState title="Chưa tìm thấy sách phù hợp" description="Thử thay đổi từ khóa tìm kiếm hoặc quay lại sau." />;
  return <div className="grid-books">{books.map(book => <BookCard key={book.id} book={book} onAdd={onAdd} />)}</div>;
}
