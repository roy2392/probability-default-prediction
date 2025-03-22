import React from 'react';
import { Card } from './ui/card';
import { Spotlight } from './ui/spotlight';
import { SplineScene } from './ui/spline';
import { CountdownTicker } from './ui/countdown-ticker';
export function HeroSection() {
  // Set target date to 30 days from now
  const targetDate = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000);
  return <div className="container mx-auto px-4 py-12">
      <Card className="w-full h-[600px] bg-black/[0.96] relative overflow-hidden border-neutral-800">
        <Spotlight className="-top-40 left-0 md:left-60 md:-top-20" fill="white" />
        <div className="flex flex-col md:flex-row h-full">
          {/* Left content */}
          <div className="md:flex-1 p-8 relative z-10 flex flex-col justify-center">
            <h1 className="text-5xl md:text-7xl font-bold bg-clip-text text-transparent bg-gradient-to-b from-neutral-50 to-neutral-400 leading-tight">
              Largest Hackathon in the world
            </h1>
            <p className="mt-6 text-neutral-300 max-w-lg text-lg">
              Join thousands of developers, designers, and innovators for an
              unforgettable experience of creation, collaboration, and
              breakthrough technologies.
            </p>
            <div className="mt-8 max-w-lg">
              <CountdownTicker targetDate={targetDate} />
            </div>
            <div className="mt-8">
              <button className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-medium rounded-lg hover:opacity-90 transition-all">
                Register Now
              </button>
            </div>
          </div>
          {/* Right content */}
          <div className="md:flex-1 relative h-[300px] md:h-full">
            <SplineScene scene="https://prod.spline.design/kZDDjO5HuC9GJUM2/scene.splinecode" className="w-full h-full" />
          </div>
        </div>
      </Card>
    </div>;
}