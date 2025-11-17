import { TrendingDown, Zap, Shield, DollarSign } from 'lucide-react';
import { motion } from 'framer-motion';

const benefits = [
  {
    icon: TrendingDown,
    title: 'Cut LLM Costs by 84%',
    description: 'Use specialized, cheaper models (Groq) instead of expensive GPT-4 for every task',
    stat: '6.5x',
    statLabel: 'Cost Reduction',
    color: 'green'
  },
  {
    icon: Zap,
    title: '18% Higher Accuracy',
    description: 'Task specialization and dedicated QA review ensures superior output quality',
    stat: '92%',
    statLabel: 'Accuracy Rate',
    color: 'purple'
  },
  {
    icon: Shield,
    title: 'Production-Ready',
    description: 'Built-in error handling, metrics tracking, and real-time monitoring for reliability',
    stat: '99.9%',
    statLabel: 'Reliability',
    color: 'blue'
  },
  {
    icon: DollarSign,
    title: 'Save $1000s Monthly',
    description: 'No expensive APM tools needed. Full observability with SQLite and WebSockets',
    stat: '$0',
    statLabel: 'Infrastructure Cost',
    color: 'orange'
  }
];

export default function Benefits() {
  return (
    <section id="benefits" className="py-20 bg-gradient-to-b from-gray-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Why Teams Choose AgentFlow
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Proven results from enterprise-grade multi-agent orchestration
            </p>
          </motion.div>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {benefits.map((benefit, idx) => {
            const Icon = benefit.icon;
            return (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: idx % 2 === 0 ? -20 : 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
                className="relative overflow-hidden rounded-2xl bg-white p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100"
              >
                <div className="flex items-start gap-6">
                  <div className={`w-14 h-14 bg-${benefit.color}-100 rounded-xl flex items-center justify-center flex-shrink-0`}>
                    <Icon className={`w-7 h-7 text-${benefit.color}-600`} />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">
                      {benefit.title}
                    </h3>
                    <p className="text-gray-600 mb-4 leading-relaxed">
                      {benefit.description}
                    </p>
                    <div className="flex items-baseline gap-2">
                      <span className={`text-4xl font-bold text-${benefit.color}-600`}>
                        {benefit.stat}
                      </span>
                      <span className="text-sm text-gray-500 font-medium">
                        {benefit.statLabel}
                      </span>
                    </div>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
