// composition-helpers.tsx — small helpers to reduce boilerplate when assembling
// a new composition from a VO manifest.
//
// `buildBeatAudioSequences` reads a manifest (the JSON that drives a video's VO)
// and produces an array of <Sequence><Audio /></Sequence> elements. Each beat's
// start_seconds + audio_duration_seconds drives the frame timing.
//
// `validateBeatTiming` returns issues if any beat overlaps the next — call
// during development to catch sync problems before rendering.

import React from "react";
import {Sequence, Audio, staticFile} from "remotion";

export interface BeatManifestEntry {
  id: string;
  start_seconds: number;
  /** Authored target duration (script-level). */
  duration_seconds: number;
  /** Actual MP3 duration (from the TTS response). Used for overlap detection. */
  audio_duration_seconds?: number;
  /** Remote audio URL (only used during a download workflow). */
  audio_url?: string;
}

export interface BeatManifest {
  meta: {id: string; voice?: string};
  beats: BeatManifestEntry[];
}

const FPS = 30;

/**
 * Build per-beat <Sequence><Audio /></Sequence> elements from a video manifest.
 * Expects MP3s at `public/audio/<manifest.meta.id>/beat<N>.mp3` (1-indexed).
 */
export const buildBeatAudioSequences = (manifest: BeatManifest) => {
  const videoId = manifest.meta.id;
  return manifest.beats.map((beat, i) => {
    const beatIndex = i + 1;
    const fromFrame = Math.round(beat.start_seconds * FPS);
    return (
      <Sequence key={beat.id} from={fromFrame}>
        <Audio src={staticFile(`audio/${videoId}/beat${beatIndex}.mp3`)} volume={1} />
      </Sequence>
    );
  });
};

/**
 * Detect overlaps in beat timing. Returns a list of problem descriptions.
 * Returns empty array when timing is clean.
 */
export const validateBeatTiming = (manifest: BeatManifest): string[] => {
  const issues: string[] = [];
  for (let i = 0; i < manifest.beats.length - 1; i++) {
    const cur = manifest.beats[i];
    const next = manifest.beats[i + 1];
    const dur = cur.audio_duration_seconds ?? cur.duration_seconds;
    const curEnd = cur.start_seconds + dur;
    if (curEnd > next.start_seconds) {
      const overlap = (curEnd - next.start_seconds).toFixed(2);
      issues.push(
        `Beat "${cur.id}" overlaps "${next.id}" by ${overlap}s. Push "${next.id}".start_seconds to at least ${curEnd.toFixed(2)}.`,
      );
    }
  }
  return issues;
};
