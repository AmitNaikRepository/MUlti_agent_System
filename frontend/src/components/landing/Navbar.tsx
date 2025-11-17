import { Link } from 'react-router-dom';
import { Activity, Menu, X } from 'lucide-react';
import { useState } from 'react';

interface NavbarProps {
  onGetStarted: () => void;
}

export default function Navbar({ onGetStarted }: NavbarProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <Activity className="w-8 h-8 text-blue-600" />
            <span className="text-xl font-bold text-gray-900">
              AgentFlow
            </span>
          </Link>

          {/* Desktop Nav Links */}
          <div className="hidden md:flex items-center gap-8">
            <a href="#features" className="text-gray-600 hover:text-gray-900 font-medium transition-colors">
              Features
            </a>
            <a href="#how-it-works" className="text-gray-600 hover:text-gray-900 font-medium transition-colors">
              How It Works
            </a>
            <a href="#benefits" className="text-gray-600 hover:text-gray-900 font-medium transition-colors">
              Benefits
            </a>
            <a
              href="https://github.com/AmitNaikRepository/MUlti_agent_System"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
            >
              GitHub
            </a>
          </div>

          {/* Desktop CTA Button */}
          <button
            onClick={onGetStarted}
            className="hidden md:block px-6 py-2.5 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-sm hover:shadow-md"
          >
            View Dashboard →
          </button>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            {mobileMenuOpen ? (
              <X className="w-6 h-6 text-gray-700" />
            ) : (
              <Menu className="w-6 h-6 text-gray-700" />
            )}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-200">
            <div className="flex flex-col space-y-3">
              <a href="#features" className="px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors">
                Features
              </a>
              <a href="#how-it-works" className="px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors">
                How It Works
              </a>
              <a href="#benefits" className="px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors">
                Benefits
              </a>
              <button
                onClick={onGetStarted}
                className="mx-4 px-6 py-2.5 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors text-center"
              >
                View Dashboard →
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
