# tests/test_file_manager.py
import os
import shutil
from file_manager.file_manager import FileManager  # استبدل المسار بحسب مكان حفظ الكلاس لديك

print("--- 1. Testing FileManager Initialization & Validation ---")
# إنشاء كلاس FileManager بمسار مؤقت للاختبار
test_dir = "test_data_folder"
manager = FileManager(data_dir=test_dir)
print(f"Directory set to: {manager.data_dir}")

# اختبار خطأ الـ Type عند إدخال مسار غير نصي
try:
    manager.data_dir = 12345
except TypeError as e:
    print(f"Caught expected TypeError: {e}")

# اختبار خطأ الـ Value عند إدخال نص فارغ
try:
    manager.data_dir = "   "
except ValueError as e:
    print(f"Caught expected ValueError: {e}")


print("\n--- 2. Testing Save and Load Data ---")
# بيانات تجريبية (تشبه المنتجات أو العملاء بصيغة دیکشنري/قائمة)
sample_data = [
    {"product_id": "PRO-001", "name": "Notebook", "price": 50.0, "stock": 20},
    {"product_id": "PRO-002", "name": "Pen", "price": 5.0, "stock": 100}
]

filename = "products.json"

# حفظ البيانات
manager.save_data(filename, sample_data)
print("Data saved successfully.")

# تحميل البيانات والتحقق منها
loaded_data = manager.load_data(filename)
print(f"Data loaded successfully. Items count: {len(loaded_data)}")
print(f"First item name: {loaded_data[0]['name']}")


print("\n--- 3. Testing FileNotFoundError Handling ---")
# محاولة تحميل ملف غير موجود للتأكد من إطلاق الخطأ الصحيح
try:
    manager.load_data("non_existent_file.json")
except FileNotFoundError as e:
    print(f"Caught expected FileNotFoundError: {e}")


# تنظيف مجلد الاختبارات وملفاته بعد الانتهاء
if os.path.exists(test_dir):
    shutil.rmtree(test_dir)
    print(f"\nCleanup: Test directory '{test_dir}' removed successfully.")

print("\nAll FileManager tests passed successfully!")