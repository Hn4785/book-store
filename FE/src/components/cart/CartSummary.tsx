import { formatVnd } from "../../utils/format";

export function CartSummary({ total, busy, onCheckout }: { total: string; busy?: boolean; onCheckout: () => void }) {
  return <aside className="cart-summary card"><h2>Tóm tắt đơn hàng</h2><div className="summary-row"><span>Tạm tính</span><strong>{formatVnd(total)}</strong></div><div className="summary-row"><span>Phí vận chuyển</span><span>Chưa áp dụng</span></div><div className="summary-row summary-total"><span>Tổng cộng</span><strong>{formatVnd(total)}</strong></div><p className="muted summary-note">Tổng tiền chính thức sẽ do máy chủ tính lại khi tạo đơn hàng.</p><button className="btn btn-primary checkout-button" disabled={busy} onClick={onCheckout}>Tiến hành đặt hàng</button></aside>;
}
