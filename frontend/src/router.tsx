import { createBrowserRouter, RouterProvider } from 'react-router';

import { AdminBookings } from './pages/AdminBookings.tsx';
import { AdminEventTypes } from './pages/AdminEventTypes.tsx';
import { AppLayout } from './App.tsx';
import { BookingForm } from './pages/BookingForm.tsx';
import { BookSlot } from './pages/BookSlot.tsx';
import { Welcome } from './pages/Welcome.tsx';

const router = createBrowserRouter([
  {
    element: <AppLayout />,
    children: [
      { index: true, element: <Welcome /> },
      { path: '/event-types/:id/book', element: <BookSlot /> },
      { path: '/event-types/:id/book/confirm', element: <BookingForm /> },
      { path: '/admin/bookings', element: <AdminBookings /> },
      { path: '/admin/event-types', element: <AdminEventTypes /> },
    ],
  },
]);

export function Router() {
  return <RouterProvider router={router} />;
}
