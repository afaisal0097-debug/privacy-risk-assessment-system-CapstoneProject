interface SensitiveAttributeSelectorProps {
  selected: string[];
  onChange: (updated: string[]) => void;
}

export const SENSITIVE_ATTRIBUTE_OPTIONS = [
  "Diagnosis Code",
  "Medical History",
  "Treatment Details",
  "Medication",
  "Lab Results",
  "Insurance Provider",
  "Admission Type",
  "Discharge Status",
];

export const DEFAULT_SENSITIVE_ATTRIBUTES = [
  "Diagnosis Code",
  "Medical History",
  "Treatment Details",
];

function SensitiveAttributeItem({
  label,
  checked,
  onToggle,
}: {
  label: string;
  checked: boolean;
  onToggle: () => void;
}) {
  return (
    <label
      className={[
        "flex items-center gap-3 h-12 px-4 rounded-[10px] border-2 cursor-pointer select-none transition-colors",
        checked
          ? "bg-[#f0fdfa] border-[#009689] hover:bg-[#e0faf5]"
          : "bg-white border-[#e5e7eb] hover:border-[#9ca3af] hover:bg-gray-50",
      ].join(" ")}
    >
      {/* Custom checkbox */}
      <div className="relative shrink-0 w-4 h-4">
        <input
          type="checkbox"
          checked={checked}
          onChange={onToggle}
          className="sr-only"
        />
        <div
          className={[
            "w-4 h-4 rounded flex items-center justify-center border-2 transition-colors",
            checked
              ? "bg-[#009689] border-[#009689]"
              : "bg-white border-[#d1d5dc]",
          ].join(" ")}
        >
          {checked && (
            <svg
              width="10"
              height="8"
              viewBox="0 0 10 8"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M1 4L3.5 6.5L9 1"
                stroke="white"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          )}
        </div>
      </div>

      <span
        className={[
          "text-sm font-medium leading-5",
          checked ? "text-[#007a6e]" : "text-[#364153]",
        ].join(" ")}
      >
        {label}
      </span>
    </label>
  );
}

export default function SensitiveAttributeSelector({
  selected,
  onChange,
}: SensitiveAttributeSelectorProps) {
  const toggle = (label: string) => {
    if (selected.includes(label)) {
      onChange(selected.filter((v) => v !== label));
    } else {
      onChange([...selected, label]);
    }
  };

  return (
    <div className="w-full max-w-5xl bg-white border border-[#e5e7eb] rounded-[14px] shadow-sm p-8 flex flex-col gap-6">
      {/* Section header */}
      <div className="flex flex-col gap-2">
        <h2 className="text-[#101828] text-lg font-semibold leading-7">
          Select Sensitive Attributes
        </h2>
        <p className="text-[#4a5565] text-sm leading-5">
          Choose attributes containing sensitive information that must be
          protected during analysis
        </p>
      </div>

      {/* Checkbox grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {SENSITIVE_ATTRIBUTE_OPTIONS.map((label) => (
          <SensitiveAttributeItem
            key={label}
            label={label}
            checked={selected.includes(label)}
            onToggle={() => toggle(label)}
          />
        ))}
      </div>

      {/* Helper note */}
      <p className="text-[#6a7282] text-xs leading-4">
        Sensitive attributes will be used to evaluate privacy disclosure risks
        and must not overlap with quasi-identifiers.
      </p>
    </div>
  );
}
