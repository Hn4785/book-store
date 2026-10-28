export type OrderStatus = "PENDING" | "CONFIRMED" | "SHIPPING" | "COMPLETED" | "CANCELED";

export interface OrderItem {
  book_id: number;
  title: string;
  quantity: number;
  unit_price: string;
  subtotal: string;
}

export interface OrderSummary {
  id: number;
  order_code: string;
  status: OrderStatus;
  total: string;
  created_at?: string;
}

export interface OrderDetail extends OrderSummary {
  shipping_name: string;
  shipping_phone: string;
  shipping_address: string;
  items: OrderItem[];
}

export interface CreateOrderPayload {
  shipping_name: string;
  shipping_phone: string;
  shipping_address: string;
}

export interface CreateOrderResponse extends OrderSummary {
  items: OrderItem[];
}

export interface OrderListQuery {
  page?: number;
  page_size?: number;
}
