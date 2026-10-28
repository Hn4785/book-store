export type UserRole = "CUSTOMER" | "ADMIN";

export interface User {
  id: number;
  username: string;
  email: string;
  role: UserRole;
}

export interface RegisterPayload {
  username: string;
  email: string;
  password: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  user: User;
}
