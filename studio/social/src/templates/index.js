// Template Registry for the Social Studio.
// Each entry's value is a React component whose static .templateMeta
// describes its id, name, and size. All four formats are the same
// SocialPost component specialised by a `format` prop — one design
// language, four canvas sizes (see SocialPost.jsx).

import {
  SocialSquare,
  SocialPortrait,
  SocialLinkedIn,
  SocialX,
} from './SocialPost.jsx';
export const TEMPLATES = {
  'social-square':   SocialSquare,
  'social-portrait': SocialPortrait,
  'social-linkedin': SocialLinkedIn,
  'social-x':        SocialX,
};

export const getTemplateMeta = () =>
  Object.values(TEMPLATES).map((T) => T.templateMeta);

export const resolveTemplate = (id) => {
  const Template = TEMPLATES[id];
  if (!Template) return null;
  return { Component: Template, meta: Template.templateMeta };
};
