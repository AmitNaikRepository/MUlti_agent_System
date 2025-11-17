import { Activity, DollarSign, Shield, Zap, TrendingUp, Bell } from 'lucide-react';
import { motion } from 'framer-motion';

const features = [
  {
    icon: Activity,
    title: 'Real-Time Orchestration',
    description: 'Watch agents collaborate in real-time with visual workflow tracking and live execution logs',
    color: 'blue',
    gradient: 'from-blue-500 to-blue-600'
  },
  {
    icon: DollarSign,
    title: 'Cost Intelligence',
    description: '84% cheaper than GPT-4. Track per-agent costs with detailed metrics and optimization insights',
    color: 'green',
    gradient: 'from-green-500 to-emerald-600'
  },
  {
    icon: Shield,
    title: 'Enterprise Quality',
    description: 'Dedicated QA agent reviews every response. 92% accuracy with comprehensive quality scores',
    color: 'purple',
    gradient: 'from-purple-500 to-purple-600'
  },
  {
    icon: Zap,
    title: 'Specialized Agents',
    description: 'Classifier, Research, Validator, Writer, and QA agents each optimized for their specific role',
    color: 'yellow',
    gradient: 'from-yellow-500 to-orange-600'
  },
  {
    icon: TrendingUp,
    title: 'Full Observability',
    description: 'Complete metrics tracking with latency, confidence scores, and performance analytics',
    color: 'indigo',
    gradient: 'from-indigo-500 to-indigo-600'
  },
  {
    icon: Bell,
    title: 'WebSocket Updates',
    description: 'Real-time progress updates via WebSocket for instant visibility into agent execution',
    color: 'red',
    gradient: 'from-red-500 to-pink-600'
  }
];

export default function Features() {
  return (
    <section id="features" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Everything You Need for Multi-Agent AI
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Built for production environments requiring enterprise-grade agent orchestration
            </p>
          </motion.div>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, idx) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
                className="group p-6 rounded-2xl border-2 border-gray-100 hover:border-blue-200 hover:shadow-xl transition-all duration-300 cursor-pointer bg-white"
              >
                <div className={`w-12 h-12 bg-gradient-to-br ${feature.gradient} rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform shadow-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
