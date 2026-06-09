"use client";

import { useEffect } from "react";
import type { DependencyList } from "react";

export function useDebouncedEffect(effect: () => void, deps: DependencyList, delay: number) {
  useEffect(() => {
    const handle = window.setTimeout(effect, delay);
    return () => window.clearTimeout(handle);
    // The caller owns the dependency list, mirroring useEffect with a debounce delay.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
}
