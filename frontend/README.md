# SupplyTracker - Frontend

The frontend for SupplyTracker, an inventory management system built with Next.js and React.

## 🚀 Technologies

- **Next.js 16** - React framework with App Router
- **React 19** - JavaScript library for building user interfaces
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Re-usable components built using Radix UI and Tailwind CSS
- **Supabase** - Authentication and real-time database

## 📁 Project Structure

```
frontend/
├── app/                    # App Router routes and pages
├── components/             # Reusable UI components
├── lib/                    # Utility functions and API clients
├── public/                 # Static assets
├── .env.example           # Example environment variables
└── package.json           # Project dependencies and scripts
```

## 🛠️ Setup and Installation

### Prerequisites

- Node.js 18.17 or later
- npm or yarn
- A running instance of the SupplyTracker backend
- Supabase project (for authentication)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/supplytracker.git
cd supplytracker/frontend
```

### 2. Install dependencies

```bash
npm install
# or
yarn install
```

### 3. Set up environment variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env.local
   ```

2. Update the `.env.local` file with your Supabase credentials:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

### 4. Run the development server

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## 🚀 Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the application for production
- `npm start` - Start the production server
- `npm run lint` - Run ESLint

## 📦 Dependencies

### Main Dependencies

- `next` - React framework
- `react` & `react-dom` - Core React libraries
- `@supabase/supabase-js` - JavaScript client for Supabase
- `@supabase/auth-helpers-nextjs` - Authentication helpers for Next.js
- `tailwindcss` - Utility-first CSS framework
- `lucide-react` - Beautiful icons

### Development Dependencies

- `typescript` - Type checking
- `eslint` - Code linting
- `@types/*` - TypeScript type definitions

## 🎨 Styling

This project uses:

- **Tailwind CSS** for utility-first styling
- **shadcn/ui** for pre-built, accessible components
- Custom CSS variables for theming

## 🔐 Authentication

Authentication is handled through Supabase Auth. The application uses:

- Email/Password authentication
- Social logins (Google, GitHub, etc.) - [Guide for setting up Google Sign-In](https://www.youtube.com/watch?v=gHXThLyUTBI)
- Protected routes using middleware

## 📝 Environment Variables

Create a `.env.local` file in the root of the frontend directory with the following variables:

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
