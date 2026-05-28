from abc import ABC, abstractmethod
from typing import Callable

# ─── STRATEGY PATTERN: Các chiến lược thanh toán ───────────────────
def pay_via_momo(amount: float) -> bool:
    print(f"📱 [Strategy] Đang thanh toán {amount} VNĐ qua Momo...")
    return True  # Giả lập thanh toán THÀNH CÔNG

def pay_via_credit_card(amount: float) -> bool:
    print(f"💳 [Strategy] Đang thanh toán {amount} VNĐ qua Thẻ Tín Dụng...")
    # Giả lập tình huống: Khách hàng nhập sai mã OTP hoặc tài khoản không đủ tiền
    return False  # Giả lập thanh toán THẤT BẠI


# ─── TEMPLATE METHOD PATTERN: Bộ khung quy trình xử lý đơn hàng ─────
class OrderPipeline(ABC):
    
    def run_process(self, order_id: str, amount: float, payment_strategy: Callable[[float], bool]):
        """
        Template Method: Định nghĩa bộ khung quy trình nghiêm ngặt.
        Có tích hợp cơ chế tự động Rollback kho nếu xảy ra sự cố ở bước sau.
        """
        print(f"🏁 [Quy trình] Bắt đầu xử lý đơn hàng: {order_id}")
        
        self._validate_order(order_id)
        
        # Bước trừ kho bắt buộc phải chạy trước thanh toán
        self._deduct_stock(order_id)
        
        # Đặt quá trình thanh toán vào cơ chế kiểm soát an toàn
        try:
            payment_success = payment_strategy(amount)
            
            if payment_success:
                print("✅ Thanh toán thành công!")
                self._send_notification(order_id)
                print(f"🎉 [Quy trình] Đơn hàng {order_id} đã hoàn tất trọn vẹn.\n")
            else:
                print("❌ Thanh toán thất bại hoặc bị hủy bởi người dùng.")
                # THANH TOÁN THẤT BẠI -> Tự động kích hoạt cơ chế hoàn tác nhả kho
                self._rollback_stock(order_id)
                print(f"↩️ [Quy trình] Đã hủy đơn {order_id} an toàn, không lo kẹt kho.\n")
                
        except Exception as e:
            # PHÁT SINH LỖI HỆ THỐNG (Mất mạng, sập cổng thanh toán...) -> Vẫn phải rollback kho
            print(f"🚨 Phát sinh lỗi hệ thống nghiêm trọng trong lúc thanh toán: {e}")
            self._rollback_stock(order_id)
            print(f"↩️ [Quy trình] Đã kích hoạt khẩn cấp cơ chế Rollback cho đơn {order_id}.\n")

    def _validate_order(self, order_id: str):
        print(f"🔍 Bước 1: Xác thực thông tin đơn hàng {order_id} hợp lệ.")

    def _deduct_stock(self, order_id: str):
        print(f"📦 Bước 2: Giảm số lượng trong Database kho (-1 sản phẩm cho đơn {order_id}).")

    def _rollback_stock(self, order_id: str):
        """Hàm hoàn tác (Rollback): Trả lại trạng thái cũ cho kho dữ liệu nếu có sự cố xảy ra"""
        print(f"🔄 [Rollback Kho]: Khôi phục dữ liệu! Cộng trả lại (+1 sản phẩm) vào kho cho đơn {order_id}.")

    @abstractmethod
    def _send_notification(self, order_id: str):
        """Để class con tự quyết định kênh gửi thông báo (Email, SMS hoặc Zalo)"""
        pass


# ─── CLASS CON TRIỂN KHAI CHI TIẾT ─────────────────────────────────
class StandardOrderProcessor(OrderPipeline):
    def _send_notification(self, order_id: str):
        print(f"📧 Bước 4: Gửi email hóa đơn điện tử cho khách hàng đặt đơn {order_id}.")


# ─── CHẠY MÔ PHỎNG THỰC TẾ (DEMO) ──────────────────────────────────
if __name__ == "__main__":
    processor = StandardOrderProcessor()

    # KỊCH BẢN 1: Khách hàng chọn Momo và thanh toán thành công ngon lành
    print("=== KỊCH BẢN 1: THANH TOÁN THÀNH CÔNG ===")
    processor.run_process(
        order_id="ORD-SUCCESS-123", 
        amount=250000, 
        payment_strategy=pay_via_momo
    )

    # KỊCH BẢN 2: Khách hàng chọn Thẻ tín dụng nhưng thanh toán thất bại (Kích hoạt Rollback)
    print("=== KỊCH BẢN 2: THANH TOÁN THẤT BẠI -> TỰ ĐỘNG ROLLBACK ===")
    processor.run_process(
        order_id="ORD-FAILED-456", 
        amount=500000, 
        payment_strategy=pay_via_credit_card
    )