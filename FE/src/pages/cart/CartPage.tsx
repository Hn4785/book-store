import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { cartApi } from "../../api/cartApi";
import type { Cart } from "../../types/cart";
import { CartItem } from "../../components/cart/CartItem";
import { CartSummary } from "../../components/cart/CartSummary";
import { Loading } from "../../components/feedback/Loading";
import { ErrorState } from "../../components/feedback/ErrorState";
import { EmptyState } from "../../components/feedback/EmptyState";

export default function CartPage() {
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(true);
  const [busyId, setBusyId] = useState<number | null>(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const load = useCallback(async () => {
    setLoading(true); setError("");
    try { setCart(await cartApi.get()); }
    catch (err) { setError(err instanceof Error ? err.message : "Không tải được giỏ hàng."); }
    finally { setLoading(false); }
  }, []);
  useEffect(() => { void load(); }, [load]);

  async function changeQuantity(id: number, quantity: number) {
    setBusyId(id); setError("");
    try { await cartApi.update(id, { quantity }); await load(); }
    catch (err) { setError(err instanceof Error ? err.message : "Không cập nhật được số lượng."); }
    finally { setBusyId(null); }
  }
  async function remove(id: number) {
    setBusyId(id); setError("");
    try { await cartApi.remove(id); await load(); }
    catch (err) { setError(err instanceof Error ? err.message : "Không xóa được sản phẩm."); }
    finally { setBusyId(null); }
  }

  return <section className="page"><div className="container">
    <div className="page-heading"><div><p className="eyebrow">GIỎ HÀNG CỦA BẠN</p><h1>Giỏ hàng</h1><p className="muted">Kiểm tra sách và số lượng trước khi đặt hàng.</p></div><Link className="btn btn-outline" to="/">Tiếp tục mua sắm</Link></div>
    {loading ? <Loading /> : error && !cart ? <ErrorState message={error} onRetry={() => void load()} /> : !cart?.items.length ? <EmptyState title="Giỏ hàng đang trống" description="Hãy khám phá danh mục và thêm những cuốn sách bạn yêu thích." /> : <>
      {error && <ErrorState message={error} />}
      <div className="cart-layout"><div className="cart-items card"><div className="cart-items-header"><strong>Sản phẩm ({cart.items.length})</strong><span className="muted">Giá · Số lượng · Thành tiền</span></div>{cart.items.map(item => <CartItem key={item.id} item={item} busy={busyId === item.id} onQuantity={quantity => void changeQuantity(item.id, quantity)} onRemove={() => void remove(item.id)} />)}</div><CartSummary total={cart.total} busy={busyId !== null} onCheckout={() => navigate("/checkout")} /></div>
    </>}
  </div></section>;
}
