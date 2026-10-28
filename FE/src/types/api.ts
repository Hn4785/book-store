export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ApiErrorBody {
  error?: string;
  message?: string;
  detail?: string;
  fields?: Record<string, string[] | string>;
  [key: string]: unknown;
}

export class ApiError extends Error {
  status: number;
  code?: string;
  fields?: Record<string, string[] | string>;
  body?: ApiErrorBody;

  constructor(message: string, status: number, body?: ApiErrorBody) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = body?.error;
    this.fields = body?.fields;
    this.body = body;
  }
}

export interface PageState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}
