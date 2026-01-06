# Oregon Grant Automation - Frontend

React frontend for the Oregon Grant Automation System.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Start development server:
```bash
npm run dev
```

The app will be available at http://localhost:5173

## Project Structure

- `src/`
  - `components/` - React components
    - `auth/` - Login, Register
    - `dashboard/` - Dashboard view
    - `common/` - Shared components
  - `hooks/` - Custom React hooks
  - `services/` - API services
  - `styles/` - CSS files
- `public/` - Static assets

## Build for Production

```bash
npm run build
```

Built files will be in `dist/` directory.

## Features

- User authentication (login/register)
- Protected routes
- JWT token management with auto-refresh
- Responsive design with Tailwind CSS
