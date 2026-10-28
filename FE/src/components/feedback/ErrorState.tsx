export function ErrorState({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return <div className="alert alert-error" role="alert"><strong>Có lỗi xảy ra.</strong> {message} {onRetry && <button className="btn btn-outline btn-small" onClick={onRetry} style={{ marginLeft: 8 }}>Thử lại</button>}</div>;
}
