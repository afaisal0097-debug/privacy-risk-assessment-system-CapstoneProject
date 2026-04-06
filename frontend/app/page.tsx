"use client";

import { useState } from "react";
import UploadCard from "@/app/components/UploadCard";
import SummaryCard from "@/app/components/SummaryCard";
import ActionButtons from "@/app/components/ActionButtons";
import QuasiIdentifierSelector from "@/app/components/QuasiIdentifierSelector";

/* Default quasi-identifiers selected on first load */
const DEFAULT_QUASI_IDENTIFIERS = [
  "Age",
  "Gender",
  "Date of Birth",
  "Ethnicity",
  "Diagnosis Code",
];

/* ── Icons ── */
function ShieldIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="white"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    </svg>
  );
}

function RowsIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="#155dfc"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
      <line x1="3" y1="9" x2="21" y2="9" />
      <line x1="3" y1="15" x2="21" y2="15" />
    </svg>
  );
}

function ColumnsIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="#009689"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
      <line x1="9" y1="3" x2="9" y2="21" />
      <line x1="15" y1="3" x2="15" y2="21" />
    </svg>
  );
}

function MissingIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="#f97316"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="8" x2="12" y2="12" />
      <line x1="12" y1="16" x2="12.01" y2="16" />
    </svg>
  );
}

/* ── Mock summary data ── */
const SUMMARY = [
  {
    icon: <RowsIcon />,
    iconBg: "bg-[#dbeafe]",
    value: "10,542",
    label: "Number of Rows",
  },
  {
    icon: <ColumnsIcon />,
    iconBg: "bg-[#cbfbf1]",
    value: "18",
    label: "Number of Columns",
  },
  {
    icon: <MissingIcon />,
    iconBg: "bg-[#ffedd4]",
    value: "2.3%",
    label: "Missing Values",
  },
];

export default function Home() {
  const [realFile, setRealFile] = useState<File | null>(null);
  const [syntheticFile, setSyntheticFile] = useState<File | null>(null);
  const [selectedQIs, setSelectedQIs] = useState<string[]>(
    DEFAULT_QUASI_IDENTIFIERS
  );

  const bothUploaded = realFile !== null && syntheticFile !== null;

  const handleReset = () => {
    setRealFile(null);
    setSyntheticFile(null);
    setSelectedQIs(DEFAULT_QUASI_IDENTIFIERS);
  };

  return (
    <div className="min-h-screen bg-[#f9fafb] flex flex-col">
      {/* Header */}
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

      {/* Main content */}
      <main className="flex-1 flex flex-col items-center px-6 py-10 gap-8">
        {/* Upload card */}
        <div className="w-full max-w-5xl bg-white border border-[#e5e7eb] rounded-[14px] shadow-sm p-8 flex flex-col gap-6">
          <div className="flex flex-col gap-2">
            <h2 className="text-[#101828] text-lg font-semibold leading-7">
              Upload Datasets
            </h2>
            <p className="text-[#4a5565] text-sm leading-5">
              Upload both real and synthetic datasets to compare privacy risks
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-6">
            <UploadCard
              title="Real Dataset"
              accent="blue"
              file={realFile}
              onFileSelect={setRealFile}
              onRemove={() => setRealFile(null)}
            />
            <UploadCard
              title="Synthetic Dataset"
              accent="teal"
              file={syntheticFile}
              onFileSelect={setSyntheticFile}
              onRemove={() => setSyntheticFile(null)}
            />
          </div>
        </div>

        {/* Quasi-identifier selector + summary — only visible when both files are uploaded */}
        {bothUploaded && (
          <>
            {/* Section: Select Quasi Identifiers */}
            <QuasiIdentifierSelector
              selected={selectedQIs}
              onChange={setSelectedQIs}
            />

            {/* Section: Dataset Summary */}
            <div className="w-full max-w-5xl flex flex-col gap-4">
              <h2 className="text-[#101828] text-lg font-semibold leading-7">
                Dataset Summary
              </h2>
              <div className="flex flex-col sm:flex-row gap-6">
                {SUMMARY.map((item) => (
                  <SummaryCard
                    key={item.label}
                    icon={item.icon}
                    iconBg={item.iconBg}
                    value={item.value}
                    label={item.label}
                  />
                ))}
              </div>
            </div>

            {/* Action buttons — passes selected QIs for future API use */}
            <ActionButtons
              onReset={handleReset}
              quasiIdentifiers={selectedQIs}
            />
          </>
        )}
      </main>
    </div>
  );
}
