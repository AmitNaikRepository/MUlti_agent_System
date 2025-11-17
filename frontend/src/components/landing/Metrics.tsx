import { motion, useInView } from 'framer-motion';
import { useRef, useState, useEffect } from 'react';

interface CounterProps {
  end: number;
  duration?: number;
  suffix?: string;
  prefix?: string;
}

function Counter({ end, duration = 2, suffix = '', prefix = '' }: CounterProps) {
  const [count, setCount] = useState(0);
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true });

  useEffect(() => {
    if (!isInView) return;

    let startTime: number;
    let animationFrame: number;

    const animate = (currentTime: number) => {
      if (!startTime) startTime = currentTime;
      const progress = Math.min((currentTime - startTime) / (duration * 1000), 1);
      
      setCount(Math.floor(progress * end));

      if (progress < 1) {
        animationFrame = requestAnimationFrame(animate);
      }
    };

    animationFrame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animationFrame);
  }, [end, duration, isInView]);

  return (
    <span ref={ref}>
      {prefix}{count}{suffix}
    </span>
  );
}

const metrics = [
  { value: 5, suffix: 'ms', label: 'Avg Overhead', description: 'Minimal performance impact' },
  { value: 92, suffix: '%', label: 'Accuracy', description: 'vs 78% single LLM' },
  { value: 84, suffix: '%', label: 'Cost Reduction', description: '6.5x cheaper than GPT-4' },
  { value: 100, suffix: '%', label: 'Coverage', description: 'Every request tracked' }
];

export default function Metrics() {
  return (
    <section className="py-20 bg-gradient-to-b from-white to-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Proven Performance Metrics
            </h2>
            <p className="text-lg text-gray-600">
              Real results from our multi-agent orchestration system
            </p>
          </motion.div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {metrics.map((metric, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: idx * 0.1 }}
              className="text-center p-6 rounded-xl bg-white shadow-lg hover:shadow-xl transition-shadow"
            >
              <div className="text-4xl md:text-5xl font-bold text-blue-600 mb-2">
                <Counter end={metric.value} suffix={metric.suffix} prefix={metric.value < 10 ? '<' : ''} />
              </div>
              <div className="text-sm font-semibold text-gray-900 mb-1">
                {metric.label}
              </div>
              <div className="text-xs text-gray-500">
                {metric.description}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
