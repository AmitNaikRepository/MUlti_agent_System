import { Activity, Github, Twitter, Linkedin } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <Link to="/" className="flex items-center gap-2 mb-4">
              <Activity className="w-8 h-8 text-blue-400" />
              <span className="text-xl font-bold text-white">AgentFlow</span>
            </Link>
            <p className="text-gray-400 max-w-md mb-4">
              Enterprise-grade multi-agent AI orchestration system. 
              Watch specialized agents collaborate to solve complex tasks.
            </p>
            <div className="flex gap-4">
              <a
                href="https://github.com/yourusername/multi-agent-system"
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-gray-700 transition-colors"
              >
                <Github className="w-5 h-5" />
              </a>
              <a
                href="https://twitter.com/yourusername"
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-gray-700 transition-colors"
              >
                <Twitter className="w-5 h-5" />
              </a>
              <a
                href="https://linkedin.com/in/yourprofile"
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-gray-700 transition-colors"
              >
                <Linkedin className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Links */}
          <div>
            <h3 className="text-white font-semibold mb-4">Product</h3>
            <ul className="space-y-2">
              <li><a href="#features" className="hover:text-white transition-colors">Features</a></li>
              <li><a href="#how-it-works" className="hover:text-white transition-colors">How It Works</a></li>
              <li><a href="#benefits" className="hover:text-white transition-colors">Benefits</a></li>
              <li><Link to="/dashboard" className="hover:text-white transition-colors">Dashboard</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-4">Resources</h3>
            <ul className="space-y-2">
              <li><a href="https://github.com/yourusername/multi-agent-system#readme" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">Documentation</a></li>
              <li><a href="https://github.com/yourusername/multi-agent-system" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">GitHub</a></li>
              <li><a href="https://github.com/yourusername/multi-agent-system/issues" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">Report Issue</a></li>
              <li><a href="mailto:your.email@example.com" className="hover:text-white transition-colors">Contact</a></li>
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-sm text-gray-400">
            © {currentYear} AgentFlow. Built with ❤️ for enterprise AI.
          </p>
          <div className="flex gap-6 mt-4 md:mt-0">
            <a href="#" className="text-sm text-gray-400 hover:text-white transition-colors">Privacy</a>
            <a href="#" className="text-sm text-gray-400 hover:text-white transition-colors">Terms</a>
            <a href="#" className="text-sm text-gray-400 hover:text-white transition-colors">License</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
