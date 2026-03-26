"use client";

import { useEffect, useRef, useState, useMemo } from "react";
import Globe, { GlobeMethods } from "react-globe.gl";

export default function EarthGlobe() {
  const globeEl = useRef<GlobeMethods | undefined>(undefined);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    
    // Auto-rotate the globe slowly by default
    if (globeEl.current) {
      globeEl.current.controls().autoRotate = true;
      globeEl.current.controls().autoRotateSpeed = 1.0;
      globeEl.current.controls().enableZoom = false; // Disable zoom for parallax scroll effect
      
      // Make it look down dynamically
      globeEl.current.pointOfView({ altitude: 2 });
    }

    // Add extra spin when user scrolls (Parallax effect)
    let lastScroll = window.scrollY;
    const handleScroll = () => {
      if (globeEl.current) {
        const delta = window.scrollY - lastScroll;
        lastScroll = window.scrollY;
        
        const currentPov = globeEl.current.pointOfView();
        globeEl.current.pointOfView({ 
          ...currentPov, 
          lng: currentPov.lng + (delta * 0.05) // Spin earth based on scroll speed
        });
      }
    };
    window.addEventListener("scroll", handleScroll, { passive: true });

    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  if (!mounted) return null;

  return (
    <div className="w-[1000px] h-[1000px] md:w-[1600px] md:h-[1600px] pointer-events-auto cursor-grab active:cursor-grabbing flex items-center justify-center filter drop-shadow-[0_0_60px_rgba(77,166,255,0.4)]">
      <Globe
        ref={globeEl}
        globeImageUrl="//unpkg.com/three-globe/example/img/earth-blue-marble.jpg" // High-res vivid earth
        bumpImageUrl="//unpkg.com/three-globe/example/img/earth-topology.png"
        backgroundColor="rgba(0,0,0,0)" // Transparent background
        
        // Vivid Sky Atmosphere
        atmosphereColor="#4da6ff"
        atmosphereAltitude={0.15}
        
        width={1600} 
        height={1600}
        animateIn={true}
      />
    </div>
  );
}
