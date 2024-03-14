// Delays the execution of a `func` by `waitMs` milliseconds, clearing
// any previous unexecuted calls.
export function debounce<F extends (...args: Parameters<F>) => ReturnType<F>>(
  func: F,
  waitMs = 300
): F {
  let timeoutId: ReturnType<typeof setTimeout>;
  return function (this: ThisParameterType<F>, ...args: Parameters<F>) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func.apply(this, args), waitMs);
  } as F;
}
