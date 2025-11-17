import { useNavigate } from 'react-router-dom';
import Navbar from '../components/landing/Navbar';
import Hero from '../components/landing/Hero';
import Features from '../components/landing/Features';
import Benefits from '../components/landing/Benefits';
import HowItWorks from '../components/landing/HowItWorks';
import Metrics from '../components/landing/Metrics';
import CTA from '../components/landing/CTA';
import Footer from '../components/landing/Footer';

export default function LandingPage() {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-white">
      <Navbar onGetStarted={handleGetStarted} />
      <Hero onViewDashboard={handleGetStarted} />
      <Features />
      <Benefits />
      <HowItWorks />
      <Metrics />
      <CTA onGetStarted={handleGetStarted} />
      <Footer />
    </div>
  );
}
