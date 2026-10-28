export function Loading({ label = "Đang tải dữ liệu..." }: { label?: string }) {
  return <div className="loading" role="status"><span className="spinner" aria-hidden="true" /> <span style={{ marginLeft: 10 }}>{label}</span></div>;
}
