# Premium Metallic Theme - Quick Reference Guide

## 🎨 Color Palette

### Quick Copy-Paste Colors

```
Dark Background:     #0a0d14
Dark Card:          #131820
Accent Blue:        #3b82f6  ← PRIMARY ACTION COLOR
Metal Silver:       #7a8fa6  ← TEXT COLOR
```

## 🎯 Most Important Classes

### For Backgrounds
```html
<!-- Page background -->
<div class="bg-dark-bg">

<!-- Card backgrounds -->
<div class="card-glass">              <!-- Basic -->
<div class="card-glass-elevated">     <!-- Premium -->
```

### For Text
```html
<!-- Headings -->
<h1 class="text-white">Title</h1>

<!-- Body text -->
<p class="text-metal-silver">Content</p>

<!-- Gradient text (premium) -->
<h1 class="text-gradient">Premium Title</h1>
```

### For Buttons
```html
<!-- Primary action -->
<button class="btn-primary">Action</button>

<!-- Secondary action -->
<button class="btn-secondary">Alternative</button>
```

## 📐 Key Spacing Values

```
Grid gap:           gap-6      (24px)
Card padding:       p-6        (24px)
Section margin:     mb-8       (32px) or mb-12 (48px)
Page padding:       py-16      (64px)
```

## 🔄 Color Replacements

### If updating old code:
```
OLD → NEW
aqua (#00d4d4) → accent-blue (#3b82f6)
gray-400 → metal-silver
dark-border → dark-border (updated shade)
```

## ✨ Premium Effects

### Glow on hover
```jsx
hover:shadow-glow hover:border-accent-blue
```

### Glass effect
```jsx
class="backdrop-blur-xl border border-dark-border"
```

### Gradient text
```jsx
class="text-gradient"
```

## 📱 Responsive Grid

```jsx
// Problem cards grid
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
```

## 🎬 Animation Timing

```css
Default transition: 300ms cubic-bezier(0.4, 0, 0.2, 1)
Animations:       3s ease-in-out infinite
```

## 🔍 Visual Hierarchy

1. **Hero Heading**: 64px, gradient text
2. **Section Heading**: 32px, white
3. **Subsection**: 20px, white
4. **Body Text**: 16px, metal-silver
5. **Small Text**: 12px, lighter silver

## 🎨 Usage Examples

### Premium Card Layout
```jsx
<div className="card-glass-elevated mb-8">
  <h2 className="text-2xl font-bold mb-4 text-white">Title</h2>
  <p className="text-metal-silver">Content here</p>
</div>
```

### Problem Card
```jsx
<div className="card-glass-elevated group h-full flex flex-col">
  <h3 className="text-lg font-bold text-white mb-4">Problem Title</h3>
  <p className="text-metal-silver mb-6">Description</p>
  <div className="mt-auto flex gap-3">
    <button className="btn-primary flex-1">Action</button>
    <button className="btn-secondary flex-1">Alternative</button>
  </div>
</div>
```

### Navigation Link
```jsx
<Link className="text-metal-silver hover:text-accent-blue transition">
  Dashboard
</Link>
```

### Form Input
```jsx
<input
  className="w-full px-4 py-2.5 bg-dark-card border border-dark-border 
             focus:border-accent-blue focus:ring-2 focus:ring-accent-blue/20 
             transition text-white"
  placeholder="Search..."
/>
```

## 🎯 Common Patterns

### Primary Action Button
```jsx
className="px-6 py-3 bg-accent-blue hover:bg-accent-blue-light 
           text-white font-semibold rounded-lg transition"
```

### Secondary Action Button
```jsx
className="px-6 py-3 border-2 border-metal-silver text-metal-silver 
           hover:bg-metal-silver/10 rounded-lg transition"
```

### Section Header with Accent
```jsx
<div className="flex items-center gap-2 mb-6">
  <span className="w-1 h-6 bg-accent-blue rounded"></span>
  <h2 className="text-2xl font-bold text-white">Section</h2>
</div>
```

### Gradient Divider
```jsx
<div className="w-full h-px bg-gradient-to-r from-transparent 
                via-dark-border to-transparent my-8"></div>
```

### Icon Badge
```jsx
<div className="p-3 bg-accent-blue/10 rounded-lg hover:bg-accent-blue/20 transition">
  <Icon className="text-accent-blue" size={24} />
</div>
```

## 🌟 Premium Effects Combination

### Fully Premium Card
```jsx
<div className="card-glass-elevated border-2 border-dark-border-light 
                hover:border-accent-blue/50 hover:shadow-glow 
                transition p-6 rounded-xl">
  {/* Content */}
</div>
```

### Premium Button
```jsx
<button className="btn-primary hover:scale-105 hover:shadow-glow transition">
  Premium Button
</button>
```

## 🔧 Quick Customization

### Change primary color everywhere:
1. Edit `tailwind.config.js`
2. Update `accent-blue` value
3. Update related light/dark variants
4. All components automatically update

### Add more spacing:
1. Change `gap-6` to `gap-8` in grids
2. Change `p-6` to `p-8` in cards
3. Change `mb-8` to `mb-12` for sections

## 🚀 Performance Tips

✓ Use `gap-6` instead of individual margins
✓ Use `transition-all` for smooth effects
✓ Leverage CSS classes instead of inline styles
✓ Use `hover:` for interactive states
✓ Combine animations with transitions

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `FRONTEND_THEME_UPDATE.md` | Complete overview |
| `FRONTEND_THEME_VISUAL_GUIDE.md` | Design reference |
| `FRONTEND_THEME_TECHNICAL.md` | Implementation details |
| `FRONTEND_THEME_SUMMARY.md` | Quick summary |
| `FRONTEND_THEME_CHECKLIST.md` | Verification checklist |
| This file | Quick reference |

## ✅ Quality Checklist for New Components

When creating new components, ensure:
- [ ] Using `card-glass-elevated` for cards
- [ ] Text is either `text-white` or `text-metal-silver`
- [ ] Buttons use `btn-primary` or `btn-secondary`
- [ ] Spacing follows 24px pattern (gap-6, p-6, mb-8)
- [ ] Hover effects include `hover:shadow-glow`
- [ ] Colors are from metallic palette
- [ ] Transitions are 300ms
- [ ] Responsive grid when needed

## 🎓 Learning Path

1. **Start here**: This file (quick reference)
2. **Visual understanding**: `FRONTEND_THEME_VISUAL_GUIDE.md`
3. **Deep dive**: `FRONTEND_THEME_TECHNICAL.md`
4. **Full context**: `FRONTEND_THEME_UPDATE.md`

## 🐛 Troubleshooting

### Colors look wrong?
- Check if using old class names (aqua, gray-400)
- Replace with new names (accent-blue, metal-silver)

### Spacing looks off?
- Ensure using consistent gap and padding
- Check for hardcoded values instead of gap-6, p-6

### Buttons don't look right?
- Use `btn-primary` or `btn-secondary` classes
- Don't mix old and new color names

### Not seeing premium effects?
- Ensure using `card-glass-elevated` not `card-glass`
- Check that hover states are applied
- Verify shadows and glows are in CSS

---

**Theme Version**: 1.0 Premium Metallic
**Last Updated**: January 18, 2026
**Status**: Production Ready
