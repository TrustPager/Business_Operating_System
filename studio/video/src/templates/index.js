// Template registry for the Video Studio.
//
// The video studio has one template: VideoBeats, which renders a
// <slug>.script.json's beats as branded text-on-screen motion graphics, one
// frame at a time (driven by ?frame=N). Kept as a registry to mirror the still
// studios' shape and to leave room for future beat templates.

import { VideoBeats } from './VideoBeats.jsx';

export const TEMPLATES = {
  'video-beats': VideoBeats,
};

export const getTemplateMeta = () =>
  Object.values(TEMPLATES).map((T) => T.templateMeta);

export const resolveTemplate = (id) => {
  const Template = TEMPLATES[id];
  if (!Template) return null;
  return { Component: Template, meta: Template.templateMeta };
};
