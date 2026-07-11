import { Config } from "@remotion/cli/config";

// =============================================================================
// Content Creation Studio — render defaults
//
// Keyless, brand-agnostic. Owner-laptop-friendly defaults; a per-render flag can
// override any of these for a premium 4K cut.
// =============================================================================

// Software GL backend (SwiftShader-via-ANGLE). HARD DEFAULT for owner machines:
// deterministic, machine-independent, no GPU-driver dependency. `--gl=angle` is an
// OPT-IN speed lever only, and only on a machine with a verified working GPU.
Config.setChromiumOpenGlRenderer("swangle");

// Conservative concurrency — a modest 8-16GB owner laptop must not thrash. Bump
// per-render on capable hardware.
Config.setConcurrency(2);

// H.264 — universal playback (YouTube, LinkedIn, socials).
Config.setCodec("h264");

// Owner-reasonable quality (premium cuts override to a lower CRF + slower preset).
Config.setCrf(18);

// Lossless frame screenshots into the encoder.
Config.setVideoImageFormat("png");
Config.setStillImageFormat("png");

// Widest player compatibility.
Config.setPixelFormat("yuv420p");
Config.setColorSpace("bt709");
