import { Minus, Plus, Trash2 } from "lucide-react";
import type { CartItem as CartItemType } from "../../types/cart";
import { formatVnd } from "../../utils/format";

export function CartItem({ item, busy, onQuantity, onRemove }: { item: CartItemType; busy: boolean; onQuantity: (quantity: number) => void; onRemove: () => void }) {
  return <div className="cart-item">
    <div className="mini-book"><span>BOOK</span></div>
    <div className="cart-item-info"><strong>{item.book.title}</strong><span className="muted">{item.book.author}</span><span>{formatVnd(item.unit_price)}</span></div>
    <div className="quantity-control"><button aria-label="Giảm số lượng" disabled={busy || item.quantity <= 1} onClick={() => onQuantity(item.quantity - 1)}><Minus size={14} /></button><span>{item.quantity}</span><button aria-label="Tăng số lượng" disabled={busy || item.quantity >= item.book.stock} onClick={() => onQuantity(item.quantity + 1)}><Plus size={14} /></button></div>
    <strong className="cart-subtotal">{formatVnd(item.subtotal)}</strong>
    <button className="icon-button danger-icon" aria-label={`Xóa ${item.book.title}`} disabled={busy} onClick={onRemove}><Trash2 size={17} /></button>
  </div>;
}
