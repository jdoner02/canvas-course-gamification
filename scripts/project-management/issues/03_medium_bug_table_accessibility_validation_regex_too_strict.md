# [MEDIUM BUG] Table accessibility validation regex too strict

**Priority:** P1
**Labels:** bug, medium, accessibility, validation

## 🐛 Bug Description
Accessibility validator marks properly formatted tables as having missing headers due to overly strict regex pattern.

## 🔄 Steps to Reproduce
1. Run validation on pages with properly formatted tables
2. Tables have `<thead>`, `<th>` elements, and proper structure
3. Validator still flags as "Data tables without proper headers"

## ✅ Expected Behavior
Tables with proper semantic markup should pass accessibility validation.

## ❌ Actual Behavior
Validator regex `r"<table(?![^>]*<th)[^>]*>.*?</table>"` doesn't detect nested `<th>` elements.

## 🎯 Impact Assessment
- [x] **Medium** - Minor impact on functionality

## 🏷️ Component Areas
- [x] Validation System
- [x] Accessibility/UDL

## 🔬 Technical Details
Regex pattern in src/validators/__init__.py line ~327 needs improvement to handle:
- Nested table structures
- `<thead>/<tbody>` semantic markup
- Complex table layouts

## 📋 Acceptance Criteria
- [ ] Update regex pattern to properly detect headers
- [ ] Test with various table structures
- [ ] Maintain WCAG 2.1 AA compliance
- [ ] Add unit tests for table validation

## 🎓 Educational Impact
**Medium** - Accessibility compliance important for inclusive education.

## ⏱️ Estimated Effort
**2-3 hours** - Regex improvement and testing