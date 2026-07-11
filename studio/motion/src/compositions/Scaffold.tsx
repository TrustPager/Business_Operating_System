import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";
import {
  NAME,
  TAGLINE,
  PRIMARY,
  PRIMARY_DEEP,
  PANEL,
  ACCENT,
  FONT_BODY,
} from "../brand.js";

// Phase-1 scaffold: proves the engine renders on the owner's brand.json.
// Every colour + the font come from brand.js -> brand/brand.json. No hex literals.
export const Scaffold: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const enter = spring({ frame, fps, config: { damping: 200 } });
  const opacity = interpolate(enter, [0, 1], [0, 1]);
  const lift = interpolate(enter, [0, 1], [24, 0]);

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(135deg, ${PRIMARY_DEEP} 0%, ${PRIMARY} 100%)`,
        alignItems: "center",
        justifyContent: "center",
        fontFamily: FONT_BODY,
      }}
    >
      <div
        style={{
          opacity,
          transform: `translateY(${lift}px)`,
          textAlign: "center",
          color: PANEL,
          padding: 80,
        }}
      >
        <div style={{ fontSize: 96, fontWeight: 800, letterSpacing: "-0.02em" }}>
          {NAME}
        </div>
        {TAGLINE ? (
          <div style={{ fontSize: 36, marginTop: 16, color: ACCENT, fontWeight: 600 }}>
            {TAGLINE}
          </div>
        ) : null}
        <div style={{ fontSize: 22, marginTop: 48, opacity: 0.75, letterSpacing: "0.08em", textTransform: "uppercase" }}>
          Content Creation Studio
        </div>
      </div>
    </AbsoluteFill>
  );
};
