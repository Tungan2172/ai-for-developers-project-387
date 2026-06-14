import { createBrowserRouter, RouterProvider } from 'react-router';

import { AppLayout } from './App.tsx';
import { Welcome } from './pages/Welcome.tsx';

const router = createBrowserRouter([
  {
    element: <AppLayout />,
    children: [{ index: true, element: <Welcome /> }],
  },
]);

export function Router() {
  return <RouterProvider router={router} />;
}
