import type { Book } from "./book";

export interface CartItem {
  id: number;
  book: Pick<Book, "id" | "title" | "author" | "price" | "stock" | "is_active">;
  quantity: number;
  unit_price: string;
  subtotal: string;
}

export interface Cart {
  id: number;
  items: CartItem[];
  total: string;
}

export interface AddCartItemPayload {
  book_id: number;
  quantity: number;
}

export interface UpdateCartItemPayload {
  quantity: number;
}

export interface CartItemMutationResponse {
  id: number;
  book_id: number;
  quantity: number;
  unit_price: string;
  subtotal: string;
}
