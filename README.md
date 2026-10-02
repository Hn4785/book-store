
# Xây dựng hệ thống quản lý và bán sách trực tuyến

## 1. Giới thiệu

Đây là dự án xây dựng hệ thống quản lý và bán sách trực tuyến nhằm thực hành quy trình phát triển phần mềm và kiểm thử phần mềm (Software Testing).

Dự án hướng đến việc xây dựng các chức năng bán sách cơ bản, đồng thời tạo môi trường để thực hành kiểm thử thủ công (Manual Testing) và kiểm thử tự động (Automation Testing).

## 2. Mục tiêu dự án

- Xây dựng ứng dụng bán sách với các chức năng cơ bản.
- Thực hành phân tích yêu cầu phần mềm.
- Thực hành viết test scenario và test case.
- Thực hành kiểm thử thủ công.
- Thực hành ghi nhận và báo cáo lỗi (Bug Report).
- Thực hành kiểm thử hồi quy (Regression Testing).
- Tìm hiểu và áp dụng tự động hóa kiểm thử bằng Puppeteer.

## 3. Chức năng dự kiến

### 3.1. Chức năng dành cho người dùng

- Đăng ký tài khoản.
- Đăng nhập và đăng xuất.
- Xem danh sách sách.
- Tìm kiếm sách theo tên hoặc tác giả.
- Xem thông tin chi tiết của sách.
- Thêm sách vào giỏ hàng.
- Cập nhật số lượng sách trong giỏ hàng.
- Xóa sách khỏi giỏ hàng.
- Tính tổng tiền đơn hàng.
- Tạo đơn hàng giả lập.
- Xem lịch sử đơn hàng.

### 3.2. Chức năng dành cho quản trị viên

- Đăng nhập quản trị.
- Thêm sách mới.
- Chỉnh sửa thông tin sách.
- Xóa sách.
- Quản lý danh sách sách.
- Xem danh sách đơn hàng.
- Cập nhật trạng thái đơn hàng.

## 4. Phạm vi kiểm thử dự kiến

### 4.1. Kiểm thử chức năng (Functional Testing)

- Kiểm thử đăng ký, đăng nhập và đăng xuất.
- Kiểm thử tìm kiếm sách.
- Kiểm thử xem chi tiết sách.
- Kiểm thử giỏ hàng.
- Kiểm thử đặt hàng.
- Kiểm thử chức năng quản lý sách.
- Kiểm thử quản lý đơn hàng.

### 4.2. Kiểm thử dữ liệu đầu vào (Validation Testing)

- Kiểm tra trường bắt buộc.
- Kiểm tra định dạng email.
- Kiểm tra độ dài mật khẩu.
- Kiểm tra giới hạn số lượng sách.
- Kiểm tra dữ liệu không hợp lệ.
- Kiểm tra dữ liệu trùng lặp.

### 4.3. Kiểm thử giao diện (UI Testing)

- Kiểm tra bố cục giao diện.
- Kiểm tra nút bấm, liên kết và biểu mẫu.
- Kiểm tra thông báo thành công và thất bại.
- Kiểm tra hiển thị trên các kích thước màn hình khác nhau.

### 4.4. Kiểm thử tự động (Automation Testing)

- Tự động kiểm thử đăng nhập.
- Tự động kiểm thử tìm kiếm sách.
- Tự động kiểm thử thêm sách vào giỏ hàng.
- Tự động kiểm thử cập nhật số lượng và tính tổng tiền.

## 5. Công nghệ dự kiến

Các công nghệ sẽ được lựa chọn và cập nhật trong quá trình phát triển dự án.

- Frontend: HTML, CSS, JavaScript.
- Backend: Django hoặc Node.js/Express.
- Cơ sở dữ liệu: SQLite.
- Kiểm thử thủ công: Test case, Test scenario, Bug Report.
- Kiểm thử API: Postman (nếu có).
- Kiểm thử tự động: Puppeteer.
- Quản lý mã nguồn: Git và GitHub.

## 6. Cấu trúc thư mục dự kiến

```text
book-management-and-sales/
├── README.md
├── .gitignore
├── docs/
│   ├── requirements.md
│   ├── test-scenarios.md
│   ├── test-cases/
│   └── bug-reports/
├── src/
└── tests/
```

Cấu trúc thư mục trên là dự kiến và sẽ được điều chỉnh theo công nghệ thực tế của dự án.


