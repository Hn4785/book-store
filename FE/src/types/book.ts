export interface Book {
  id: number;
  title: string;
  author: string;
  description: string;
  /** API trả decimal dưới dạng string để tránh sai số tiền tệ. */
  price: string;
  stock: number;
  is_active: boolean;
}

export interface BookQuery {
  search?: string;
  page?: number;
  page_size?: number;
}
