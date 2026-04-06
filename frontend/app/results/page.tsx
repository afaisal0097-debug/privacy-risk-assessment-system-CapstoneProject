"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import SummaryCard from "@/app/components/SummaryCard";
import UploadedFilePanel from "@/app/components/UploadedFilePanel";
import RiskOverviewCard from "@/app/components/RiskOverviewCard";
import RiskBadge from "@/app/components/RiskBadge";
import ResultsCharts from "@/app/components/ResultsCharts";
import { mockResults } from "@/app/results/mockData";

// ─── Shared icons ────────────────────────────────────────────────────────────

function ShieldIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
      fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    </svg>
  );
}

function RowsIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
      fill="none" stroke="#155dfc" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
      <line x1="3" y1="9" x2="21" y2="9" />
      <line x1="3" y1="15" x2="21" y2="15" />
    </svg>
  );
}

function ColumnsIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
      fill="none" stroke="#009689" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
      <line x1="9" y1="3" x2="9" y2="21" />
      <line x1="15" y1="3" x2="15" y2="21" />
    </svg>
  );
}

function MissingIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
      fill="none" stroke="#f97316" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="8" x2="12" y2="12" />
      <line x1="12" y1="16" x2="12.01" y2="16" />
    </svg>
  );
}

function PlayIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
      fill="white" stroke="none">
      <polygon points="5 3 19 12 5 21 5 3" />
    </svg>
  );
}

function DownloadIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
      fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <polyline points="7 10 12 15 17 10" />
      <line x1="12" y1="15" x2="12" y2="3" />
    </svg>
  );
}

function RefreshIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
      fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="1 4 1 10 7 10" />
      <path d="M3.51 15a9 9 0 1 0 .49-3.46" />
    </svg>
  );
}

// ─── Section title ────────────────────────────────────────────────────────────

function SectionTitle({ children }: { children: React.ReactNode }) {
  return (
    <h2 className="text-[#101828] text-lg font-semibold leading-7">{children}</h2>
  );
}

// ─── Results page ─────────────────────────────────────────────────────────────

export default function ResultsPage() {
  const router = useRouter();

  /**
   * TODO: Replace `mockResults` with real API data.
   * Example:
   *   const results = await fetch("/api/analyze").then(r => r.json());
   */
  const results = mockResults;

  return (
    <div className="min-h-screen bg-[#f9fafb] flex flex-col">

      {/* ── Header ── */}
      <header className="bg-white border-b border-[#e5e7eb] w-full">
        <div className="max-w-5xl mx-auto px-6 py-6 flex items-center gap-3">
          <div className="bg-[#155dfc] w-10 h-10 rounded-[10px] flex items-center justify-center shrink-0">
            <ShieldIcon />
          </div>
          <div className="flex flex-col gap-0.5">
            <h1 className="text-[#101828] text-2xl font-semibold leading-8">
              Privacy Risk Assessment System
            </h1>
            <p className="text-[#4a5565] text-sm leading-5">
              Evaluate privacy risks in synthetic healthcare datasets
            </p>
          </div>
        </div>
      </header>

      {/* ── Main ── */}
      <main className="flex-1 flex flex-col items-center px-6 py-10 gap-8">
        <div className="w-full max-w-5xl flex flex-col gap-8">

          {/* ── Section 1: Uploaded Datasets ── */}
          <div className="bg-white border border-[#e5e7eb] rounded-[14px] shadow-sm p-8 flex flex-col gap-6">
            <div className="flex flex-col gap-2">
              <SectionTitle>Upload Datasets</SectionTitle>
              <p className="text-[#4a5565] text-sm leading-5">
                Upload both real and synthetic datasets to compare privacy risks
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-6">
              <UploadedFilePanel
                title="Real Dataset"
                fileName={results.uploadedDatasets.real.name}
                fileSize={results.uploadedDatasets.real.size}
                accent="blue"
              />
              <UploadedFilePanel
                title="Synthetic Dataset"
                fileName={results.uploadedDatasets.synthetic.name}
                fileSize={results.uploadedDatasets.synthetic.size}
                accent="teal"
              />
            </div>
          </div>

          {/* ── Section 2: Dataset Summary ── */}
          <div className="flex flex-col gap-4">
            <SectionTitle>Dataset Summary</SectionTitle>
            <div className="flex flex-col sm:flex-row gap-6">
              <SummaryCard
                icon={<RowsIcon />}
                iconBg="bg-[#dbeafe]"
                value={results.datasetSummary.rows}
                label="Number of Rows"
              />
              <SummaryCard
                icon={<ColumnsIcon />}
                iconBg="bg-[#cbfbf1]"
                value={results.datasetSummary.columns}
                label="Number of Columns"
              />
              <SummaryCard
                icon={<MissingIcon />}
                iconBg="bg-[#ffedd4]"
                value={results.datasetSummary.missingValues}
                label="Missing Values"
              />
            </div>
          </div>

          {/* ── Section 3: Privacy Risk Overview ── */}
          <div className="flex flex-col gap-4">
            <SectionTitle>Privacy Risk Overview</SectionTitle>
            <div className="flex flex-col sm:grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {results.riskOverview.map((item) => (
                <RiskOverviewCard
                  key={item.label}
                  label={item.label}
                  value={item.value}
                  level={item.level}
                />
              ))}
            </div>
          </div>

          {/* ── Section 4: Risk Analysis ── */}
          <div className="flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <SectionTitle>Risk Analysis</SectionTitle>
              <button
                type="button"
                onClick={() => router.push("/")}
                className="bg-[#155dfc] hover:bg-[#1151d6] text-white text-sm font-medium h-9 px-4 rounded-[10px] flex items-center gap-2 transition-colors"
              >
                <PlayIcon />
                Run Again
              </button>
            </div>
            <ResultsCharts
              variableRiskChart={results.variableRiskChart}
              ageGroupChart={results.ageGroupChart}
            />
          </div>

          {/* ── Section 5: Variable Risk Ranking ── */}
          <div className="flex flex-col gap-4">
            <SectionTitle>Variable Risk Ranking</SectionTitle>
            <div className="bg-white border border-[#e5e7eb] rounded-[14px] shadow-sm overflow-hidden">
              <table className="w-full text-sm border-collapse">
                <thead>
                  <tr className="bg-[#f9fafb] border-b border-[#e5e7eb]">
                    <th className="text-left text-[#364153] text-xs font-semibold tracking-wide uppercase px-6 py-3">
                      Rank
                    </th>
                    <th className="text-left text-[#364153] text-xs font-semibold tracking-wide uppercase px-6 py-3">
                      Variable Name
                    </th>
                    <th className="text-left text-[#364153] text-xs font-semibold tracking-wide uppercase px-6 py-3">
                      Risk Score
                    </th>
                    <th className="text-left text-[#364153] text-xs font-semibold tracking-wide uppercase px-6 py-3">
                      Risk Level
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {results.variableRiskRanking.map((row, idx) => {
                    const isHighRow = row.level === "High";
                    const isLast = idx === results.variableRiskRanking.length - 1;
                    return (
                      <tr
                        key={row.rank}
                        className={[
                          isHighRow ? "bg-[#fef2f2]" : "bg-white",
                          !isLast ? "border-b border-[#e5e7eb]" : "",
                        ].join(" ")}
                      >
                        <td className="text-[#4a5565] px-6 py-4">{row.rank}</td>
                        <td className="text-[#101828] font-medium px-6 py-4">
                          {row.variable}
                        </td>
                        <td className="text-[#101828] px-6 py-4">{row.score}</td>
                        <td className="px-6 py-4">
                          <RiskBadge level={row.level} />
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* ── Section 6: Bottom Action Buttons ── */}
          <div className="flex items-center justify-center gap-4 pb-4">
            {/* Disabled — analysis is already done on this page */}
            <button
              type="button"
              disabled
              className="bg-[#d1d5dc] text-white text-base font-medium h-12 px-6 rounded-[10px] flex items-center gap-2 cursor-not-allowed"
              aria-label="Run Analysis (already completed)"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
                fill="white" stroke="none">
                <polygon points="5 3 19 12 5 21 5 3" />
              </svg>
              Run Analysis
            </button>

            {/* Download Report — placeholder, no backend yet */}
            <button
              type="button"
              onClick={() => {
                /* TODO: wire to backend report download endpoint */
                alert("Download Report — backend not connected yet.");
              }}
              className="bg-[#009689] hover:bg-[#007a6e] text-white text-base font-medium h-12 px-6 rounded-[10px] flex items-center gap-2 transition-colors"
            >
              <DownloadIcon />
              Download Report
            </button>

            {/* Reset — navigates back to upload page */}
            <Link
              href="/"
              className="bg-white hover:bg-gray-50 text-[#364153] text-base font-medium h-12 px-6 rounded-[10px] border border-[#d1d5dc] flex items-center gap-2 transition-colors"
            >
              <RefreshIcon />
              Reset
            </Link>
          </div>

        </div>
      </main>
    </div>
  );
}
