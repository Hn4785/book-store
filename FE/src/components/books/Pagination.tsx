export function Pagination({ page, pageSize, count, onChange }: { page: number; pageSize: number; count: number; onChange: (page: number) => void }) {
  const totalPages = Math.max(1, Math.ceil(count / pageSize));
  if (totalPages <= 1) return null;
  return <div className="pagination"><button className="btn btn-outline" disabled={page <= 1} onClick={() => onChange(page - 1)}>Trước</button><span>Trang <strong>{page}</strong> / {totalPages}</span><button className="btn btn-outline" disabled={page >= totalPages} onClick={() => onChange(page + 1)}>Sau</button></div>;
}
