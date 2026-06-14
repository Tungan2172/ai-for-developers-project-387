import { createBrowserRouter, RouterProvider } from 'react-router';

import { AppLayout } from './App.tsx';
import { BookingForm } from './pages/BookingForm.tsx';
import { BookSlot } from './pages/BookSlot.tsx';
import { EventTypeDetail } from './pages/EventTypeDetail.tsx';
import { Welcome } from './pages/Welcome.tsx';

const router = createBrowserRouter([
  {
    element: <AppLayout />,
    children: [
      { index: true, element: <Welcome /> },
      { path: '/event-types/:id', element: <EventTypeDetail /> },
      { path: '/event-types/:id/book', element: <BookSlot /> },
      { path: '/event-types/:id/book/confirm', element: <BookingForm /> },
    ],
  },
]);

export function Router() {
  return <RouterProvider router={router} />;
}
