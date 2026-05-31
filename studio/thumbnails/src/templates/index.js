// Template Registry for the YouTube Thumbnail Studio.
// Each entry's value is a React component whose static .templateMeta
// describes its id, name, and size.

import { YouTubeThumbnail } from './YouTubeThumbnail.jsx';

export const TEMPLATES = {
  'youtube-thumbnail': YouTubeThumbnail,
};

export const getTemplateMeta = () =>
  Object.values(TEMPLATES).map((T) => T.templateMeta);

export const resolveTemplate = (id) => {
  const Template = TEMPLATES[id];
  if (!Template) return null;
  return { Component: Template, meta: Template.templateMeta };
};
