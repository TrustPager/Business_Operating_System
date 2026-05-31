// Template Registry for the Nurture CTA Studio.
// Each entry's value is a React component whose static .templateMeta
// describes its id, name, and size.

import { HeroCardCTA } from './HeroCardCTA.jsx';

export const TEMPLATES = {
  'hero-card-cta': HeroCardCTA,
};

export const getTemplateMeta = () =>
  Object.values(TEMPLATES).map((T) => T.templateMeta);

export const resolveTemplate = (id) => {
  const Template = TEMPLATES[id];
  if (!Template) return null;
  return { Component: Template, meta: Template.templateMeta };
};
