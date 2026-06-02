// Template registry for the OG Image studio.
//
// One template: OgImage (1200×630, the Open Graph / social-share standard).
// Every sample in data/samples.json uses it; the differences live in the
// sample data (headline, accent word, hero). The registry shape matches the
// social + thumbnail studios so the shared App.jsx editor renders it as-is.

import { OgImage } from './OgImage.jsx';

export const TEMPLATES = {
  'og-image': OgImage,
};

export const getTemplateMeta = () =>
  Object.values(TEMPLATES).map((T) => T.templateMeta);

export const resolveTemplate = (id) => {
  const Template = TEMPLATES[id];
  if (!Template) return null;
  return { Component: Template, meta: Template.templateMeta };
};
