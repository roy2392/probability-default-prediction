import React from 'react';
interface SpotlightProps {
  className?: string;
  fill?: string;
}
export function Spotlight({
  className,
  fill = 'white'
}: SpotlightProps) {
  return <div className={`pointer-events-none absolute inset-0 z-0 transition-all ${className || ''}`} style={{
    background: `radial-gradient(600px circle at var(--mouse-x, 0px) var(--mouse-y, 0px), ${fill}/0.1, transparent 40%)`
  }} />;
}