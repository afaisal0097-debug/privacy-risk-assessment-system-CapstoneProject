"use client";

import { useRouter } from "next/navigation";

interface ActionButtonsProps {
  onReset: () => void;
  /**
   * Quasi-identifiers and sensitive attributes selected by the user.
   * Persisted to sessionStorage before navigating to /results so the results
   * page (and future API calls) can read them after navigation.
   *
   * TODO (backend integration): replace the sessionStorage writes with a real
   * API call when the backend is ready, e.g.:
   *   await fetch("/api/analyze", {
   *     method: "POST",
   *     body: JSON.stringify({ quasiIdentifiers, sensitiveAttributes }),
   *   })
   */
  quasiIdentifiers?: string[];
  sensitiveAttributes?: string[];
}

function PlayIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="white"
      stroke="none"
    >
      <polygon points="5 3 19 12 5 21 5 3" />
    </svg>
  );
}

function RefreshIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <polyline points="1 4 1 10 7 10" />
      <path d="M3.51 15a9 9 0 1 0 .49-3.46" />
    </svg>
  );
}

export default function ActionButtons({
  onReset,
  quasiIdentifiers = [],
  sensitiveAttributes = [],
}: ActionButtonsProps) {
  const router = useRouter();

  const handleRunAnalysis = () => {
    // Persist selections so the results page can access them after navigation.
    // TODO: replace these writes with a real API call when the backend is ready.
    sessionStorage.setItem(
      "selectedQuasiIdentifiers",
      JSON.stringify(quasiIdentifiers)
    );
    sessionStorage.setItem(
      "selectedSensitiveAttributes",
      JSON.stringify(sensitiveAttributes)
    );
    router.push("/results");
  };

  return (
    <div className="flex items-center justify-center gap-4">
      <button
        type="button"
        onClick={handleRunAnalysis}
        className="bg-[#155dfc] hover:bg-[#1151d6] text-white text-base font-medium leading-6 h-12 px-6 rounded-[10px] flex items-center gap-2 transition-colors"
      >
        <PlayIcon />
        Run Analysis
      </button>

      <button
        type="button"
        onClick={onReset}
        className="bg-white hover:bg-gray-50 text-[#364153] text-base font-medium leading-6 h-12 px-6 rounded-[10px] border border-[#d1d5dc] flex items-center gap-2 transition-colors"
      >
        <RefreshIcon />
        Reset
      </button>
    </div>
  );
}
