# CLAUDE.md

## Repository Overview

This is a TradingView **Pine Script v5** repository containing trading indicator scripts. Scripts are pasted directly into TradingView's Pine Editor and run as chart overlays or panels — there is no build system, runtime, or test framework.

## Current Scripts

### `kelly_position_sizer.pine`
An overlay `indicator` (not a `strategy`) that calculates position sizing using the Kelly Criterion. It plots horizontal lines for Entry, Stop, and Target on the chart, and renders a summary table in the top-right corner.

**Key inputs:**
- Position side (Long/Short), entry price (manual or last close), stop, target
- Bankroll/equity, fixed risk % of equity
- Win probability `p`, fractional Kelly multiplier, lot step, contract multiplier

**Core logic flow:**
1. Resolve entry price → compute per-unit risk and reward → derive R ratio
2. Calculate Kelly fraction: `f* = p - (1-p)/R`, scaled by `kellyScale`
3. Optionally cap Kelly allocation with fixed risk % (whichever is smaller)
4. Round position size down to nearest `lotStep` via `roundDownToStep()`
5. Display results in a `table` on `barstate.islast`, plot price levels with `plot()`

## Pine Script Conventions

- **Always use `@version=5`** at the top of every file.
- **Indicators vs Strategies:** Use `indicator()` for display-only tools; use `strategy()` only when backtesting execution logic is needed. This repo currently uses `indicator()` exclusively.
- **`var` keyword:** Use `var` for variables that should persist across bars (e.g., `var table t = table.new(...)`). Omitting `var` re-initializes on every bar.
- **`barstate.islast`:** All table writes and label placements must be gated on `barstate.islast` to avoid creating thousands of objects.
- **`na` handling:** Check `validPrices` or explicit `na(v)` guards before computing derived values. Pine Script will silently propagate `na` through arithmetic.
- **`plot()` with `na`:** Use a ternary like `validPrices ? value : na` to suppress lines when inputs are incomplete.
- **`plot.style_linebr`:** Use this style to break the plotted line when the value is `na` rather than connecting across gaps.
- **`table.clear(t)`** must be called inside `barstate.islast` before rebuilding the table to avoid stale rows after input changes.
- **`table.merge_cells()`** must be called before `table.cell()` for the same cell range.
- **User-defined functions** must be declared before they are called. Pine Script processes the script top-to-bottom; forward references are not allowed.
- **`max_labels_count` / `max_bars_back`:** Set these in `indicator()` when the script creates labels or needs historical bar access beyond the default.

## Naming & Style

- Variable names: `camelCase` for locals, descriptive names that encode units or role (e.g., `riskPerUnit`, `riskCashKelly`).
- Input variables: suffix `In` for raw user inputs that require post-processing (e.g., `entryIn`, `pWinInp`).
- Helper functions: lowercase camelCase (e.g., `roundDownToStep`, `fmt`, `fmtPct`).
- Keep formatting helpers (`fmt`, `fmtPct`) small and purely functional — no side effects.

## Development Workflow

1. **Edit** the `.pine` file locally in this repo.
2. **Copy** the full file contents.
3. **Paste** into TradingView Pine Editor (open any chart → Pine Editor tab at the bottom → New → paste).
4. Click **Add to chart** to test.
5. Adjust inputs via the indicator settings dialog to validate edge cases.
6. Commit changes back to this repo with a descriptive message.

There is no linter, formatter, or automated test runner. Validation is manual via the TradingView Pine Editor's built-in compiler (red error bar at the bottom of the editor on syntax errors).

## Common Pitfalls

- **Reassigning `na`-typed variables:** Declare with an explicit type or initial value to avoid type errors (e.g., `float riskPerUnit = na` not `riskPerUnit = na`).
- **Series vs scalar:** Many Pine built-ins return series values; you cannot pass a series where a simple (scalar) is required (e.g., `table.new()` size arguments). Inputs from `input.*()` are always simple.
- **`if` block scoping:** Variables assigned inside an `if` block are not visible outside it unless declared before the block.
- **Position sizing direction:** For Short trades, risk = stop − entry and reward = entry − target. Getting these backwards produces negative R ratios.

## Repository Structure

```
/
├── CLAUDE.md                    # This file
├── README.md                    # Minimal project title
└── kelly_position_sizer.pine    # Kelly Criterion position sizing indicator
```

New scripts should be added as individual `.pine` files at the repo root, named in `snake_case` describing their purpose.
