import { createContext, useContext, useState, type ReactNode } from 'react';

interface RoleContextValue {
  isAdmin: boolean;
  setIsAdmin: (v: boolean) => void;
}

const RoleContext = createContext<RoleContextValue | null>(null);

export function RoleProvider({ children, initialAdmin = false }: { children: ReactNode; initialAdmin?: boolean }) {
  const [isAdmin, setIsAdmin] = useState(initialAdmin);

  return (
    <RoleContext.Provider value={{ isAdmin, setIsAdmin }}>
      {children}
    </RoleContext.Provider>
  );
}

export function useRoleContext(): RoleContextValue {
  const ctx = useContext(RoleContext);
  if (!ctx) throw new Error('useRoleContext must be used within RoleProvider');
  return ctx;
}
