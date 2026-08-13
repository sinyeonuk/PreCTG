# UI Accessibility

This document defines accessibility and adaptive-layout requirements for user interfaces.

## Accessibility

- Use semantic elements and a logical reading order whenever possible.
- Ensure sufficient color contrast and do not rely solely on color to communicate meaning.
- Support complete keyboard operation and visible, predictable focus states for relevant interactions.
- Keep focus order aligned with the visual and task order; do not use positive tab order to repair a structurally incorrect layout.
- Move focus deliberately when opening, closing, adding, or removing interface regions, and restore it to a meaningful control when a temporary layer closes.
- Keep focus within a modal interaction while it is active without trapping users in non-modal content.
- Provide accessible names, labels, descriptions, instructions, and error feedback for interactive elements.
- Programmatically associate field errors, help text, required state, and status with the controls they describe.
- Announce dynamic loading, completion, error, and validation changes to assistive technology when visual updates alone would not be discoverable.
- Provide useful text alternatives for informative images and icons, and hide purely decorative graphics from assistive technology.
- Ensure controls have practical pointer and touch targets with enough separation to avoid accidental activation.
- Support text enlargement, zoom, and reflow without clipping, overlap, loss of content, or forced two-dimensional scrolling except where the content inherently requires it.
- Preserve essential meaning in high-contrast and forced-color modes when those environments apply.
- Respect reduced-motion preferences when motion is used.
- Avoid flashing, unexpected automatic movement, and time limits that prevent users from completing the task; provide control when timing is necessary.
- Do not disable browser, platform, or assistive-technology behavior solely to enforce a custom interaction.

## Adaptive and Responsive Design

- Design for the relevant range of screen sizes from the beginning.
- Avoid layouts that work only at one fixed resolution.
- Preserve content priority and task completion on smaller screens.
- Use breakpoints based on layout needs rather than arbitrary device labels.
- Support the relevant keyboard, pointer, touch, pen, and assistive input methods rather than assuming hover or precise pointing is always available.
- Account for virtual keyboards, safe areas, display cutouts, orientation changes, and browser or system interface overlays when they affect the target platform.
- Do not hide required information or actions merely because the viewport or input method changes.
