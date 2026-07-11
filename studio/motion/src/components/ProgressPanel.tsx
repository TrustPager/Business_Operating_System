// ProgressPanel — persistent task-progress widget.
// Completed items: filled accent circle + check + strikethrough text.
// Active item: outlined circle with number + bold dark text.
// Pending items: light circle with number + muted text.
import React from "react";
import {colors, fonts, shadows} from "../tokens";

// Progress accent — the brand accent (the "being-done-for-you" colour).
const ACCENT = colors.accentBrand;

export interface ProgressTask {
  id?: string;
  label: string;
}

export interface ProgressPanelProps {
  tasks: ProgressTask[];
  completedCount?: number;
  activeIndex?: number | null;
  opacity?: number;
  title?: string;
}

const CheckIcon: React.FC = () => (
  <svg width={16} height={16} viewBox="0 0 16 16" fill="none">
    <path
      d="M3.5 8.5L6.5 11.5L12.5 5"
      stroke="white"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

const ChevronIcon: React.FC = () => (
  <svg width={16} height={16} viewBox="0 0 16 16" fill="none">
    <path
      d="M4 6L8 10L12 6"
      stroke={colors.text400}
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

type Status = "completed" | "active" | "pending";

const TaskItem: React.FC<{index: number; label: string; status: Status}> = ({
  index,
  label,
  status,
}) => {
  const num = index + 1;

  const circleBase: React.CSSProperties = {
    width: 32,
    height: 32,
    borderRadius: "50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
  };

  const circleStyle: React.CSSProperties =
    status === "completed"
      ? {...circleBase, backgroundColor: ACCENT}
      : status === "active"
      ? {...circleBase, backgroundColor: "transparent", border: `2px solid ${ACCENT}`}
      : {...circleBase, backgroundColor: colors.bg300};

  const numStyle: React.CSSProperties = {
    fontFamily: fonts.ui,
    fontSize: 13,
    fontWeight: 600,
    color: status === "active" ? ACCENT : colors.text400,
    lineHeight: 1,
  };

  const labelStyle: React.CSSProperties = {
    fontFamily: fonts.ui,
    fontSize: 15,
    lineHeight: 1.35,
    ...(status === "completed"
      ? {color: colors.text400, textDecoration: "line-through"}
      : status === "active"
      ? {color: colors.text100, fontWeight: 600}
      : {color: colors.text300, fontWeight: 400}),
  };

  return (
    <div style={{display: "flex", alignItems: "center", gap: 12, padding: "7px 0"}}>
      <div style={circleStyle}>
        {status === "completed" ? <CheckIcon /> : <span style={numStyle}>{num}</span>}
      </div>
      <span style={labelStyle}>{label}</span>
    </div>
  );
};

export const ProgressPanel: React.FC<ProgressPanelProps> = ({
  tasks,
  completedCount = 0,
  activeIndex = null,
  opacity = 1,
  title = "Progress",
}) => {
  const active = activeIndex !== null ? activeIndex : completedCount;

  return (
    <div
      style={{
        backgroundColor: colors.bg000,
        borderRadius: 16,
        boxShadow: `${shadows.overlay}, 0 1px 4px rgba(0,0,0,0.06)`,
        padding: "16px 20px",
        width: 300,
        opacity,
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          paddingBottom: 10,
          borderBottom: `1px solid ${colors.border100}`,
          marginBottom: 4,
        }}
      >
        <span style={{fontFamily: fonts.ui, fontSize: 16, fontWeight: 600, color: colors.text100}}>
          {title}
        </span>
        <ChevronIcon />
      </div>

      <div style={{display: "flex", flexDirection: "column"}}>
        {tasks.map((task, i) => {
          const status: Status =
            i < completedCount ? "completed" : i === active ? "active" : "pending";
          return <TaskItem key={task.id ?? i} index={i} label={task.label} status={status} />;
        })}
      </div>
    </div>
  );
};
