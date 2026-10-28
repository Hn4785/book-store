import { http, tokenStorage } from "./http";
import type { LoginPayload, LoginResponse, RegisterPayload, User } from "../types/user";

export const authApi = {
  async register(payload: RegisterPayload): Promise<User> {
    return http.post<User>("auth/register", payload, { auth: false });
  },
  async login(payload: LoginPayload): Promise<LoginResponse> {
    const result = await http.post<LoginResponse>("auth/login", payload, { auth: false });
    tokenStorage.set(result.access);
    return result;
  },
  me: () => http.get<User>("auth/me"),
  async logout(): Promise<void> {
    try {
      await http.post<void>("auth/logout", {});
    } finally {
      // JWT stateless có thể vẫn hợp lệ phía server nếu backend không triển khai blacklist.
      tokenStorage.clear();
    }
  },
};
