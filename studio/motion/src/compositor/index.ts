// Compositor primitives — top-level video stitching tools that work with any
// scene component. Brand-agnostic: colour flows from the token bridge, never a
// baked product colour.
export {ComposerOverlay} from './ComposerOverlay';
export type {
  ComposerOverlayProps,
  ComposerOverlayTiming,
  ComposerOverlayPosition,
} from './ComposerOverlay';
export {PictureInPicture} from './PictureInPicture';
export {ConnectorLine} from './ConnectorLine';
export {CrossHighlight} from './CrossHighlight';
export {CursorClick} from './CursorClick';
export type {Box, PictureInPictureProps} from './PictureInPicture';
export type {Point, ConnectorLineProps} from './ConnectorLine';
export type {CrossHighlightProps} from './CrossHighlight';
export type {CursorClickProps} from './CursorClick';

export {PipelineRewireGlow} from './PipelineRewireGlow';
export {StageAutomationBadges} from './StageAutomationBadges';
export type {PipelineRewireGlowProps} from './PipelineRewireGlow';
export type {StageAutomationBadgesProps, StageBadge} from './StageAutomationBadges';
export {AutomationLightningStrike} from './AutomationLightningStrike';
export {AutomationPreviewCard} from './AutomationPreviewCard';
export {CursorHover} from './CursorHover';
export {AutomationBuildSequence} from './AutomationBuildSequence';
export {CursorPath} from './CursorPath';
export {NoAutomationsCard} from './NoAutomationsCard';
export {DebugOverlay} from './DebugOverlay';
export {Callout} from './Callout';
export {ClickPulseRing, CLICK_COLORS} from './ClickPulseRing';
export type {ClickPulseRingProps, ClickPulseColor} from './ClickPulseRing';
export {ActOffsetWrapper} from './ActOffsetWrapper';
export type {StagePosition} from './positions';
export {buildBeatAudioSequences, validateBeatTiming} from './composition-helpers';
export type {BeatManifest, BeatManifestEntry} from './composition-helpers';
export {useTypewriter, usePasteFlash, useFadeIn} from './animations';
export type {FadeInOptions, FadeInResult} from './animations';
