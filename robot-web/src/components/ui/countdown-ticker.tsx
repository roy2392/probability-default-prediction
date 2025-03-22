import React, { useEffect, useState } from 'react';
interface TimeLeft {
  days: number;
  hours: number;
  minutes: number;
  seconds: number;
}
interface CountdownTickerProps {
  targetDate: Date;
}
export function CountdownTicker({
  targetDate
}: CountdownTickerProps) {
  const [timeLeft, setTimeLeft] = useState<TimeLeft>({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0
  });
  useEffect(() => {
    const calculateTimeLeft = () => {
      const difference = +targetDate - +new Date();
      if (difference > 0) {
        setTimeLeft({
          days: Math.floor(difference / (1000 * 60 * 60 * 24)),
          hours: Math.floor(difference / (1000 * 60 * 60) % 24),
          minutes: Math.floor(difference / 1000 / 60 % 60),
          seconds: Math.floor(difference / 1000 % 60)
        });
      }
    };
    calculateTimeLeft();
    const timer = setInterval(calculateTimeLeft, 1000);
    return () => clearInterval(timer);
  }, [targetDate]);
  const TimeUnit = ({
    value,
    label
  }: {
    value: number;
    label: string;
  }) => <div className="flex flex-col items-center mx-2 md:mx-4">
      <div className="text-2xl md:text-4xl font-bold bg-gradient-to-b from-purple-400 to-purple-600 bg-clip-text text-transparent">
        {value.toString().padStart(2, '0')}
      </div>
      <div className="text-xs md:text-sm text-neutral-400 mt-1">{label}</div>
    </div>;
  return <div className="flex justify-center items-center bg-neutral-900/50 rounded-lg py-4 backdrop-blur-sm">
      <TimeUnit value={timeLeft.days} label="DAYS" />
      <div className="text-xl md:text-2xl text-purple-500 mb-4">:</div>
      <TimeUnit value={timeLeft.hours} label="HOURS" />
      <div className="text-xl md:text-2xl text-purple-500 mb-4">:</div>
      <TimeUnit value={timeLeft.minutes} label="MINUTES" />
      <div className="text-xl md:text-2xl text-purple-500 mb-4">:</div>
      <TimeUnit value={timeLeft.seconds} label="SECONDS" />
    </div>;
}