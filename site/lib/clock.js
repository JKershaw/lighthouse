// The build's clock. Every date-relative block (This week, the day's line,
// On watch, a checkpoint's "recent" mark, the schedule's readiness and an
// investigation's next read) is computed from this one instant, so a build is
// reproducible for any moment: LIGHTHOUSE_NOW=2026-11-19T00:05:00Z npm run build.
export function buildNow(env = process.env) {
  const value = env.LIGHTHOUSE_NOW;
  if (!value) return new Date();
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) throw new Error(`LIGHTHOUSE_NOW is not a date: ${value}`);
  return d;
}
