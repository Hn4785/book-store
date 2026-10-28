import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { authApi } from "../api/authApi";
import { tokenStorage } from "../api/http";
import type { LoginPayload, RegisterPayload, User } from "../types/user";

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (payload: LoginPayload) => Promise<void>;
  register: (payload: RegisterPayload) => Promise<User>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}
const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshUser = useCallback(async () => {
    if (!tokenStorage.get()) { setUser(null); return; }
    try { setUser(await authApi.me()); }
    catch { tokenStorage.clear(); setUser(null); }
  }, []);

  useEffect(() => {
    void refreshUser().finally(() => setLoading(false));
  }, [refreshUser]);

  const login = useCallback(async (payload: LoginPayload) => {
    const response = await authApi.login(payload);
    setUser(response.user);
  }, []);

  const register = useCallback(async (payload: RegisterPayload) => authApi.register(payload), []);

  const logout = useCallback(async () => {
    try { await authApi.logout(); } finally { setUser(null); }
  }, []);

  const value = useMemo(() => ({ user, loading, isAuthenticated: !!user, login, register, logout, refreshUser }), [user, loading, login, register, logout, refreshUser]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth phải được dùng bên trong AuthProvider.");
  return context;
}
