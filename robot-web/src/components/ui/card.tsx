import React from 'react';
interface CardProps {
  className?: string;
  children: React.ReactNode;
}
export function Card({
  className,
  children
}: CardProps) {
  return <div className={`rounded-xl border border-neutral-800 shadow-xl ${className || ''}`}>
      {children}
    </div>;
}