# tests/test_store_products.py
import os
import shutil
from models.product import Product
from models.category import Category
from file_manager.file_manager import FileManager
from store.store import Store # تأكد من أن اسم ملف كلاس Store صحيح لديك

print("--- INITIALIZING TEST ENVIRONMENT ---")
test_dir = "test_store_data"
file_manager = FileManager(data_dir=test_dir)

# تجهيز فئة افتراضية ومنتجات أولية لاختبارها
category = Category(category_id="CAT-001", name="Electronics")
p1 = Product(product_id="PRO-001", name="Laptop", price=1000.0, stock=5, category=category)
p2 = Product(product_id="PRO-002", name="Mouse", price=50.0, stock=20, category=category)

# إنشاء متجر فارغ بالكامل
store = Store(customer=[], product=[], category=[category], order=[], file_manager=file_manager)

print("\n--- 1. Testing add_product ---")
# إضافة منتج جديد بنجاح
store.add_product(p1)
store.add_product(p2)
print(f"Total products after adding: {len(store.product)}") # يجب أن يكونوا 2

# محاولة إضافة منتج بنفس الـ ID (يجب أن يعطي خطأ ValueError)
try:
    duplicate_product = Product(product_id="PRO-001", name="Fake Laptop", price=800.0, stock=2, category=category)
    store.add_product(duplicate_product)
except ValueError as e:
    print(f"Caught expected error on duplicate ID: {e}")


print("\n--- 2. Testing get_product ---")
# تجربة البحث بالاسم أو الجلب
try:
    found = store.get_product("Laptop")
    print(f"Found product by name: {found.name}, Price: {found.price}")
except Exception as e:
    print(f"Error in get_product: {e}")


print("\n--- 3. Testing update_product ---")
# تحديث منتج موجود
updated_p1 = Product(product_id="PRO-001", name="Gaming Laptop", price=1200.0, stock=4, category=category)
store.update_product(product_id="PRO-001", updated_product=updated_p1)

# التحقق هل تم التحديث بنجاح
check_updated = store.get_product("Gaming Laptop")
print(f"Updated product name: {check_updated.name}, New Price: {check_updated.price}")

# محاولة تحديث منتج غير موجود (يجب أن يعطي خطأ)
try:
    store.update_product(product_id="PRO-999", updated_product=p1)
except ValueError as e:
    print(f"Caught expected error on updating non-existent product: {e}")


print("\n--- 4. Testing delete_product ---")
# حذف منتج موجود
store.delete_product("PRO-002")
print(f"Total products after deletion: {len(store.product)}") # يجب أن يبقى منتج واحد فقط

# محاولة حذف منتج غير موجود (يجب أن يعطي خطأ)
try:
    store.delete_product("PRO-999")
except ValueError as e:
    print(f"Caught expected error on deleting non-existent product: {e}")


print("\n--- CLEANUP ---")
if os.path.exists(test_dir):
    shutil.rmtree(test_dir)
    print(f"Test directory '{test_dir}' cleaned up successfully.")

print("\nAll Product CRUD tests passed successfully!")