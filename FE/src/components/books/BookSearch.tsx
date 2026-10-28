import { Search, X } from "lucide-react";

export function BookSearch({ value, onChange, onSubmit, onClear }: { value: string; onChange: (value: string) => void; onSubmit: () => void; onClear: () => void }) {
  return <form className="toolbar search-form" onSubmit={event => { event.preventDefault(); onSubmit(); }}>
    <div className="search-wrap"><Search size={19} /><input className="search-input" aria-label="Tìm sách" placeholder="Tìm theo tên sách hoặc tác giả..." value={value} onChange={event => onChange(event.target.value)} />{value && <button className="clear-search" type="button" aria-label="Xóa tìm kiếm" onClick={onClear}><X size={17} /></button>}</div>
    <button className="btn btn-primary" type="submit">Tìm kiếm</button>
  </form>;
}
