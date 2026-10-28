import { Navigate, Route, Routes } from "react-router-dom";
import { MainLayout } from "./components/layout/MainLayout";
import ProtectedRoute from "./components/ProtectedRoute";
import RoleGuard from "./components/RoleGuard";
import BookListPage from "./pages/books/BookListPage";
import BookDetailPage from "./pages/books/BookDetailPage";
import CartPage from "./pages/cart/CartPage";
import LoginPage from "./pages/auth/LoginPage";
import RegisterPage from "./pages/auth/RegisterPage";
import ProfilePage from "./pages/auth/ProfilePage";
import CheckoutPage from "./pages/orders/CheckoutPage";
import OrderListPage from "./pages/orders/OrderListPage";
import OrderDetailPage from "./pages/orders/OrderDetailPage";
import AdminPage from "./pages/admin/AdminPage";

function NotFoundPage() {
  return <section className="page"><div className="container empty-state"><h1>Không tìm thấy trang</h1><p>Đường dẫn bạn truy cập không tồn tại.</p><a className="btn btn-primary" href="/">Về trang chủ</a></div></section>;
}

export default function App() {
  return <Routes><Route element={<MainLayout />}>
    <Route index element={<BookListPage />} />
    <Route path="books/:id" element={<BookDetailPage />} />
    <Route path="login" element={<LoginPage />} />
    <Route path="register" element={<RegisterPage />} />
    <Route element={<ProtectedRoute />}>
      <Route path="profile" element={<ProfilePage />} />
      <Route path="cart" element={<RoleGuard role="CUSTOMER" />}><Route index element={<CartPage />} /></Route>
      <Route path="checkout" element={<RoleGuard role="CUSTOMER" />}><Route index element={<CheckoutPage />} /></Route>
      <Route path="orders" element={<RoleGuard role="CUSTOMER" />}><Route index element={<OrderListPage />} /></Route>
      <Route path="orders/:id" element={<RoleGuard role="CUSTOMER" />}><Route index element={<OrderDetailPage />} /></Route>
      <Route path="admin" element={<RoleGuard role="ADMIN" />}><Route index element={<AdminPage />} /></Route>
    </Route>
    <Route path="*" element={<NotFoundPage />} />
  </Route></Routes>;
}
