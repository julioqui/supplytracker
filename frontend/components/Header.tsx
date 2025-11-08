// frontend/components/Header.tsx
import { LogOut, User } from 'lucide-react';
import { Button } from './ui/button';

type HeaderProps = {
  userName: string;
  onLogout: () => void;
};

export default function Header({ userName, onLogout }: HeaderProps) {
  return (
    <header className="h-16 bg-white border-b border-gray-200 px-6 flex items-center justify-between">
      <div>
        <span className="text-sm text-gray-500">Bem-vindo,</span>
        <span className="ml-1 font-medium">{userName}</span>
      </div>
      
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 text-gray-600">
          <User className="w-5 h-5" />
          <span className="text-sm">{userName}</span>
        </div>

        <Button variant="ghost" size="sm" onClick={onLogout} className="flex items-center gap-1">
          <LogOut className="w-4 h-4" />
          Sair
        </Button>
      </div>
    </header>
  );
}
