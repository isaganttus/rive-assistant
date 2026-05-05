# Rive Best Practices Reference
> Last verified: 2026-04-23
> Source docs: `getting-started/best-practices.mdx`, `getting-started/introduction.mdx`

## Overview

Performance and asset optimization guidelines for Rive files and runtime integration.

## Design-Time: Asset Optimization

### Fonts
- **Select only needed glyphs** — reduce font data in .riv file
- Remove unused characters to minimize file size
- Consider out-of-band font loading for very large character sets

### Raster Images
- **Size appropriately** — don't use 8192px images for 100px display
- **Compress** — WebP recommended over PNG/JPG
- **Memory impact** — especially on mobile devices; images decompress to full resolution in memory
- **Break large images** into chunks or mix with vector elements
- **Consider out-of-band loading** — keep .riv small, load images separately

### Vector Graphics
- **Minimize vertex count** — fewer vertices = better performance
- **Caution with AI-generated / auto-traced imports** — often have excessive vertices
- **Prefer procedural shapes** when possible (rect, ellipse)

### Lottie Imports
- Rive files are typically smaller than equivalent Lottie
- Convert PNG to WebP when importing
- Select only needed font glyphs
- Load assets out-of-band for size reduction

## Design-Time: Editor Optimization

### Blend Modes
- **Expensive on web** — requires framebuffer copy per blend mode
- Use sparingly, especially in web deployments
- Test performance on target devices

### Artboards
- **Minimize clipping** — evaluates every object; clip specific objects/groups instead of artboard
- **Remove unused artboards** — still parsed on load, consuming memory and CPU

### Animation Optimization
- **One-shot animations for idle** — state machine auto-pauses when no active animations (very low CPU)
- **Solos over opacity** — Solo groups skip computation/rendering entirely; opacity still processes
- **Transition out of blend states** — leaving a blend state active prevents idle pause
- **Avoid long idle timelines** — use one-shot with appropriate loop settings

## Runtime: Performance Optimization

### Out-of-Band Assets
- Reduce .riv file size significantly
- Reuse assets across multiple .riv files
- Preload and cache for faster display
- Swap by resolution/locale/device capability

### .riv File Caching
- **Parse once, reuse many times** — significant performance gain
- Critical for lists/grids showing many instances
- All runtimes support caching patterns

### Programmatic Pausing
- **Offscreen**: Pause animations scrolled out of view; resume when visible
- **Accessibility**: Respect `prefers-reduced-motion` user setting
- **Idle waiting**: Pause when waiting for user interaction
- **Web**: Set `autoplay: false` for reduced-motion media query

### Low-End Devices
- **Test on target devices** — don't assume desktop performance
- **Alternative artboards/state machines** for reduced motion
- **Static graphics** (`autoplay: false`) as ultimate fallback
- **Reduce animating entities** — fewer simultaneous animations

## Architecture Best Practices

### Project Structure
- One artboard = one self-contained interactive scene
- Use components for reusable elements
- Use view models as the contract between design and code
- Keep state machines focused — split complex logic across layers

### Data Binding First
- Always use Data Binding for new projects
- Plan migration from legacy Inputs/Events
- Exported view model instances = the developer API
- One view model per artboard as default; nested view models for components

### Designer-Developer Workflow
- Designers define view models and bindings
- Developers consume exported instances and properties
- Listeners handle in-editor interactivity
- Runtime code handles data fetching and business logic

### Communication & Documentation
When advocating for Rive solutions:
- Emphasize the designer-developer contract (Data Binding)
- Highlight responsive capabilities (Layouts)
- Show performance advantages (idle pause, GPU rendering, small file sizes)
- Demonstrate cross-platform consistency (same .riv on all platforms)
- Compare file sizes to equivalent Lottie/video/GIF alternatives

## Common Pitfalls

1. **Forgetting cleanup** — always dispose Rive instances when removing views (memory leaks)
2. **Not calling resizeDrawingSurfaceToCanvas()** on web — blurry rendering
3. **Using legacy Inputs** in new projects — use Data Binding instead
4. **Embedding large assets** — use out-of-band loading
5. **Overusing blend modes on web** — significant performance cost
6. **Not testing on mobile** — performance varies dramatically by device
7. **Leaving blend states active** — prevents idle CPU savings
8. **Clipping at artboard level** — clips every object; prefer targeted clipping
