/**
 * ActOffsetWrapper — shifts children's useCurrentFrame() view by a negative
 * offset so a per-act Test composition can render the act's GLOBAL-frame
 * content starting at local frame 0.
 *
 * Background
 * ----------
 * Multi-act compositions use composition-wide GLOBAL frame numbers in their
 * beat sequences (e.g. an act whose beats start at frame 3352). Mounting an act
 * directly in its own *-Test composition means frames 0 through ACT_START render
 * blank.
 *
 * Wrapping the act in `<ActOffsetWrapper offset={-ACT_START}>` shifts the frame
 * context: at outer frame 0, the act's useCurrentFrame() returns ACT_START, so
 * the first beat renders immediately. The Test composition's `durationInFrames`
 * can then be set to just the act's actual length.
 *
 * Remotion 4.x supports negative `from` on `<Sequence>`; this wrapper is
 * effectively a one-line passthrough to that, with named-intent semantics.
 *
 * Usage:
 *   <ActOffsetWrapper offset={-ACT_START} durationInFrames={ACT_END - ACT_START}>
 *     <MyAct />
 *   </ActOffsetWrapper>
 */
import React from 'react';
import {Sequence} from 'remotion';

export const ActOffsetWrapper: React.FC<{
  /** Negative value matching the act's GLOBAL first-beat frame. */
  offset: number;
  /** The act's actual length (last beat global frame - first beat global frame + tail). */
  durationInFrames: number;
  children: React.ReactNode;
}> = ({offset, durationInFrames, children}) => (
  <Sequence from={offset} durationInFrames={durationInFrames - offset}>
    {children}
  </Sequence>
);
