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
// FinalPiece rich posts — bespoke illustrated 1080×1350 designs with their own
// visual language (see finalpiece/shell.jsx). NOT brand.json-driven.
import { PlatformPost } from './finalpiece/PlatformPost.jsx';
import { WebsitePost } from './finalpiece/WebsitePost.jsx';
import { CrmPost } from './finalpiece/CrmPost.jsx';
import { AgentsPost } from './finalpiece/AgentsPost.jsx';

export const TEMPLATES = {
  'social-square':   SocialSquare,
  'social-portrait': SocialPortrait,
  'social-linkedin': SocialLinkedIn,
  'social-x':        SocialX,
  'fp-platform': PlatformPost,
  'fp-website':  WebsitePost,
  'fp-crm':      CrmPost,
  'fp-agents':   AgentsPost,
};

export const getTemplateMeta = () =>
  Object.values(TEMPLATES).map((T) => T.templateMeta);

export const resolveTemplate = (id) => {
  const Template = TEMPLATES[id];
  if (!Template) return null;
  return { Component: Template, meta: Template.templateMeta };
};
