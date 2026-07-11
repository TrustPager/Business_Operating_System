// Overlay — the talking-head compositing composition (Mode B, design spec §5.2).
//
// One props-driven composition, exactly like `Video`/FacelessFromPlan: the plan
// arrives as Remotion input props (scripts/render.js hands it in inline), and
// `calculateMetadata` derives fps/dimensions/duration from that plan. The plan
// carries ONE owner recording plus a list of graphics + caption overlay items and
// an optional music bed.
//
// Compositing model (all in Remotion, one mixed MP4 out):
//   1. The recording is one layer, rendered with <Video> from @remotion/media
//      (frame-perfect, and it carries its OWN audio track). Full-frame by default;
//      in webcam-bubble mode it sits inside a PictureInPicture box over a brand
//      background.
//   2. Graphics layer over it via AbsoluteFill DOM order (later children paint on
//      top) — the ported Annotations engine (headlines / lower-thirds / captions).
//   3. Caption band over that — CaptionTrack, driven by useCurrentFrame().
//   4. Audio: the recording's track flows through <Video>. If a music bed is
//      supplied, it is DUCKED under the recording via a per-frame volume callback
//      (a low constant bed with short fades), never competing with the voice.
//
// Duration is NEVER hardcoded: it comes from the recording's real length, probed
// in Node by scripts/render.js and injected as `durationInFrames` (calculateMetadata
// runs in a headless browser and cannot read the file off disk).
import React from "react";
import { AbsoluteFill, Audio, staticFile, useVideoConfig, interpolate } from "remotion";
import { Video } from "@remotion/media";
import { Annotations } from "../overlays/Annotations";
import { CaptionTrack, type Caption } from "../overlays/CaptionTrack";
import { PictureInPicture, type Box } from "../compositor/PictureInPicture";
import { bg } from "../tokens";

const ASPECT_DIMS: Record<string, { width: number; height: number }> = {
  "16:9": { width: 1920, height: 1080 },
  "9:16": { width: 1080, height: 1920 },
  "1:1": { width: 1080, height: 1080 },
};

// A low music bed sitting UNDER the voice — the recording's own audio is the hero.
const MUSIC_DUCK_LEVEL = 0.12;

export interface OverlayPip {
  box: Box; // proportional {x,y,w,h} bubble position (see PictureInPicture)
  borderRadius?: number;
  shadow?: boolean;
}

export interface OverlayPlan {
  slug?: string;
  mode?: string;
  aspect?: string;
  fps?: number;
  durationInFrames?: number; // injected by render.js from the probed recording length
  recording?: string | null; // path under public/ (e.g. "recordings/<slug>.mp4")
  music?: string | null; // path under public/ (e.g. "audio/<slug>/music-bed.mp3")
  pip?: OverlayPip | null; // present => webcam-bubble mode
  graphics?: unknown[]; // Annotations items (headline / caption / cursor / highlight)
  captions?: Caption[]; // whisper / script-derived caption track
}

export interface OverlayMeta {
  fps: number;
  durationInFrames: number;
  dims: { width: number; height: number };
}

/**
 * The ONE place overlay metadata is computed, so Root's calculateMetadata and
 * render.js never disagree on fps / dimensions / duration. `durationInFrames`
 * comes from the plan (render.js probes the recording and injects it); a small
 * fallback keeps the Studio preview alive when no recording is wired yet.
 */
export const computeOverlayMeta = (rawPlan: unknown): OverlayMeta => {
  const plan = (rawPlan ?? {}) as OverlayPlan;
  const fps = plan.fps ?? 30;
  const dims = ASPECT_DIMS[plan.aspect ?? "9:16"] ?? ASPECT_DIMS["9:16"];
  const durationInFrames =
    typeof plan.durationInFrames === "number" && plan.durationInFrames > 0
      ? Math.round(plan.durationInFrames)
      : fps * 5; // fallback: a 5s placeholder when no recording is probed yet
  return { fps, durationInFrames, dims };
};

const RecordingLayer: React.FC<{ recording: string; pip?: OverlayPip | null }> = ({
  recording,
  pip,
}) => {
  const src = staticFile(recording);
  if (pip) {
    // Webcam-bubble mode: the recording sits inside a static PiP box over a brand
    // background. from==to boxes hold it still; a caller could animate later.
    return (
      <AbsoluteFill style={{ background: bg }}>
        <PictureInPicture
          fromBox={pip.box}
          toBox={pip.box}
          fromFrame={0}
          toFrame={1}
          borderRadius={pip.borderRadius ?? 24}
          shadow={pip.shadow ?? true}
        >
          <Video src={src} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        </PictureInPicture>
      </AbsoluteFill>
    );
  }
  // Full-frame: the recording IS the background layer.
  return (
    <AbsoluteFill style={{ background: bg }}>
      <Video
        src={src}
        style={{ width: "100%", height: "100%", objectFit: "cover" }}
      />
    </AbsoluteFill>
  );
};

const MusicBed: React.FC<{ music: string }> = ({ music }) => {
  const { fps, durationInFrames } = useVideoConfig();
  const fadeF = Math.max(Math.round(0.5 * fps), 1);
  // A per-frame volume callback: a low, constant bed under the voice, with short
  // fades at the head and tail so the music never competes with the recording.
  const volume = (f: number) => {
    const inGain = interpolate(f, [0, fadeF], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    const outGain = interpolate(
      f,
      [durationInFrames - fadeF, durationInFrames],
      [1, 0],
      { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
    );
    return MUSIC_DUCK_LEVEL * Math.min(inGain, outGain);
  };
  return <Audio src={staticFile(music)} volume={volume} />;
};

const MissingRecording: React.FC = () => (
  <AbsoluteFill
    style={{
      background: bg,
      alignItems: "center",
      justifyContent: "center",
      color: "#94a3b8",
      fontSize: 28,
      fontFamily: "system-ui, sans-serif",
      textAlign: "center",
      padding: 40,
    }}
  >
    No recording wired yet — run `npm run ingest` to add one.
  </AbsoluteFill>
);

/**
 * Props-driven talking-head composition. Layers, in DOM/paint order:
 *   recording (background or PiP) → graphics (Annotations) → captions (CaptionTrack)
 *   → music bed (audio-only, ducked).
 */
export const Overlay: React.FC<OverlayPlan> = (plan) => {
  const recording = plan.recording;
  const graphics = Array.isArray(plan.graphics) ? plan.graphics : [];
  const captions = Array.isArray(plan.captions) ? plan.captions : [];

  return (
    <AbsoluteFill style={{ background: bg }}>
      {recording ? (
        <RecordingLayer recording={recording} pip={plan.pip} />
      ) : (
        <MissingRecording />
      )}

      {/* Graphics over the recording (headlines / lower-thirds) — paint order = on top. */}
      {graphics.length > 0 ? <Annotations annotations={graphics} /> : null}

      {/* Caption band over the graphics. */}
      {captions.length > 0 ? <CaptionTrack captions={captions} /> : null}

      {/* Music bed, ducked under the recording's own audio. Audio-only, no visual. */}
      {plan.music ? <MusicBed music={plan.music} /> : null}
    </AbsoluteFill>
  );
};
