#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║           سكريبت تحسين وضغط الصور - الوسيلة الذكية              ║
║         Image Optimization Script - Al-Wasila Al-Thakiya        ║
╚══════════════════════════════════════════════════════════════════╝

الوصف:
    يقوم هذا السكريبت بتقليل حجم جميع الصور (JPG و WEBP) في المشروع
    مع الحفاظ على الجودة البصرية العالية المناسبة لعرض الكتب المدرسية.

المميزات:
    ✅ يحتفظ بنفس المسارات وأسماء الملفات
    ✅ يحتفظ بنفس الترتيب والتنسيق
    ✅ ينشئ نسخة احتياطية قبل أي تعديل
    ✅ يُنتج تقريراً مفصلاً بالنتائج
    ✅ يتخطى الصور الصغيرة التي لا تحتاج ضغط
    ✅ يدعم استعادة النسخ الاحتياطية

الاستخدام:
    python optimize_images.py                  # تشغيل الضغط
    python optimize_images.py --dry-run        # معاينة بدون تعديل
    python optimize_images.py --restore        # استعادة النسخ الاحتياطية
    python optimize_images.py --quality 80     # تحديد جودة مخصصة (1-100)
    python optimize_images.py --no-backup      # بدون نسخ احتياطية (غير مستحسن)
    python optimize_images.py --report-only    # إنشاء تقرير فقط بدون ضغط
"""

import os
import sys
import io
import json
import shutil
import argparse
import hashlib

# اصلاح ترميز وحدة التحكم على Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
import time
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from PIL import Image, ImageFile
    # السماح بتحميل الصور المقطوعة/التالفة جزئياً
    ImageFile.LOAD_TRUNCATED_IMAGES = True
except ImportError:
    print("❌ مكتبة Pillow غير مثبتة. قم بتثبيتها:")
    print("   pip install Pillow")
    sys.exit(1)


# ══════════════════════════════════════════════════════════════════
# الإعدادات الافتراضية
# ══════════════════════════════════════════════════════════════════

# المسار الجذري للمشروع (نفس مجلد السكريبت)
ROOT_DIR = Path(__file__).parent.resolve()

# مجلد النسخ الاحتياطية
BACKUP_DIR = ROOT_DIR / "_نسخ_احتياطية_الصور"

# ملف التقرير
REPORT_FILE = ROOT_DIR / "تقرير_تحسين_الصور.json"

# امتدادات الصور المدعومة
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.webp', '.png'}

# الحد الأدنى لحجم الملف بالبايت (الصور الأصغر من هذا يتم تخطيها)
MIN_FILE_SIZE = 20 * 1024  # 20 KB

# الحد الأدنى للتوفير بالنسبة المئوية (إذا كان التوفير أقل، يُحتفظ بالأصلي)
MIN_SAVINGS_PERCENT = 5  # 5%

# عدد المعالجات المتزامنة
MAX_WORKERS = 4


class ImageOptimizer:
    """محسّن الصور الرئيسي"""

    def __init__(self, quality=85, dry_run=False, no_backup=False, report_only=False):
        """
        المعاملات:
            quality (int): جودة الضغط (1-100). الافتراضي 85 (توازن ممتاز بين الجودة والحجم)
            dry_run (bool): معاينة فقط بدون تعديل
            no_backup (bool): عدم إنشاء نسخ احتياطية
            report_only (bool): إنشاء تقرير فقط بالأحجام الحالية
        """
        self.quality = quality
        self.dry_run = dry_run
        self.no_backup = no_backup
        self.report_only = report_only

        # إحصائيات
        self.stats = {
            "total_files": 0,
            "processed": 0,
            "skipped": 0,
            "errors": 0,
            "original_total_bytes": 0,
            "optimized_total_bytes": 0,
            "details": [],
            "errors_list": [],
        }

    def _get_file_hash(self, filepath):
        """حساب hash للملف للتحقق من سلامته"""
        h = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
        return h.hexdigest()

    def _backup_file(self, filepath):
        """إنشاء نسخة احتياطية للملف مع الحفاظ على هيكل المجلدات"""
        if self.no_backup or self.dry_run:
            return True

        try:
            rel_path = filepath.relative_to(ROOT_DIR)
            backup_path = BACKUP_DIR / rel_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(filepath), str(backup_path))
            return True
        except Exception as e:
            print(f"  ⚠️ فشل النسخ الاحتياطي: {e}")
            return False

    def _optimize_jpg(self, img, filepath):
        """
        تحسين صور JPG

        الاستراتيجية:
        - إزالة بيانات EXIF غير الضرورية
        - إعادة الضغط بجودة محسّنة
        - تفعيل progressive JPEG للتحميل التدريجي على الويب
        - تفعيل optimize لأفضل ضغط Huffman
        """
        # تحويل إلى RGB إذا كانت بصيغة أخرى (مثل RGBA أو P)
        if img.mode in ('RGBA', 'P', 'LA'):
            img = img.convert('RGB')
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # حفظ بالإعدادات المحسّنة
        img.save(
            str(filepath),
            format='JPEG',
            quality=self.quality,
            optimize=True,       # أفضل ضغط Huffman
            progressive=True,    # تحميل تدريجي (أفضل لتجربة الويب)
            subsampling=1,       # 4:2:2 chroma subsampling (توازن جيد)
        )

    def _optimize_webp(self, img, filepath):
        """
        تحسين صور WEBP

        الاستراتيجية:
        - إعادة الضغط بجودة محسّنة
        - استخدام method=6 لأبطأ وأفضل ضغط
        - WEBP أصلاً كفؤ، فنستخدم جودة أعلى قليلاً
        """
        # WEBP يدعم الشفافية (RGBA)، نحتفظ بها إن وُجدت
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')

        # جودة أعلى قليلاً لـ WEBP لأنه أكفأ أصلاً
        webp_quality = min(self.quality + 3, 95)

        img.save(
            str(filepath),
            format='WEBP',
            quality=webp_quality,
            method=6,  # أبطأ لكن أفضل ضغط (0-6)
        )

    def _optimize_single(self, filepath):
        """تحسين صورة واحدة"""
        filepath = Path(filepath)
        ext = filepath.suffix.lower()
        original_size = filepath.stat().st_size

        result = {
            "file": str(filepath.relative_to(ROOT_DIR)),
            "original_size": original_size,
            "optimized_size": original_size,
            "savings_bytes": 0,
            "savings_percent": 0,
            "status": "unknown",
        }

        # تخطي الصور الصغيرة جداً
        if original_size < MIN_FILE_SIZE:
            result["status"] = "skipped_small"
            return result

        try:
            if self.report_only:
                result["status"] = "report_only"
                return result

            if self.dry_run:
                # في وضع المعاينة، نقدّر الحجم الجديد
                img = Image.open(str(filepath))
                img.close()
                result["status"] = "dry_run"
                return result

            # إنشاء نسخة احتياطية
            if not self._backup_file(filepath):
                result["status"] = "backup_failed"
                return result

            # حساب hash الأصلي للتحقق
            original_hash = self._get_file_hash(filepath)

            # فتح الصورة
            img = Image.open(str(filepath))
            img.load()  # تحميل البيانات بالكامل قبل الحفظ

            # التحسين حسب النوع
            if ext in ('.jpg', '.jpeg'):
                self._optimize_jpg(img, filepath)
            elif ext == '.webp':
                self._optimize_webp(img, filepath)
            elif ext == '.png':
                # تحويل PNG إلى نفس الامتداد مع ضغط أفضل
                img.save(str(filepath), format='PNG', optimize=True)

            img.close()

            # التحقق من الحجم الجديد
            new_size = filepath.stat().st_size
            savings = original_size - new_size
            savings_percent = (savings / original_size) * 100 if original_size > 0 else 0

            # إذا لم يكن التوفير كافياً، نستعيد الأصل
            if savings_percent < MIN_SAVINGS_PERCENT or new_size >= original_size:
                # استعادة الأصل من النسخة الاحتياطية
                if not self.no_backup:
                    rel_path = filepath.relative_to(ROOT_DIR)
                    backup_path = BACKUP_DIR / rel_path
                    if backup_path.exists():
                        shutil.copy2(str(backup_path), str(filepath))

                result["optimized_size"] = original_size
                result["status"] = "skipped_minimal_savings"
                return result

            # التحقق من سلامة الصورة المحسّنة
            try:
                verify_img = Image.open(str(filepath))
                verify_img.verify()
            except Exception:
                # الصورة تالفة! استعادة النسخة الاحتياطية
                if not self.no_backup:
                    rel_path = filepath.relative_to(ROOT_DIR)
                    backup_path = BACKUP_DIR / rel_path
                    if backup_path.exists():
                        shutil.copy2(str(backup_path), str(filepath))
                result["status"] = "error_corrupted"
                return result

            result["optimized_size"] = new_size
            result["savings_bytes"] = savings
            result["savings_percent"] = round(savings_percent, 1)
            result["status"] = "optimized"

        except Exception as e:
            result["status"] = f"error: {str(e)}"
            # محاولة استعادة من النسخة الاحتياطية
            if not self.no_backup:
                try:
                    rel_path = filepath.relative_to(ROOT_DIR)
                    backup_path = BACKUP_DIR / rel_path
                    if backup_path.exists():
                        shutil.copy2(str(backup_path), str(filepath))
                except Exception:
                    pass

        return result

    def _collect_images(self):
        """جمع جميع ملفات الصور"""
        images = []
        for dirpath, dirnames, filenames in os.walk(str(ROOT_DIR)):
            # تخطي مجلد النسخ الاحتياطية
            dirpath_p = Path(dirpath)
            if BACKUP_DIR.name in dirpath_p.parts:
                continue
            # تخطي المجلدات المخفية
            if any(part.startswith('.') or part.startswith('_') for part in dirpath_p.parts
                   if part != ROOT_DIR.name and part != BACKUP_DIR.name):
                # لا نتخطى كل ما يبدأ بـ _ إلا مجلد النسخ الاحتياطية
                pass

            for fname in sorted(filenames):
                fpath = Path(dirpath) / fname
                if fpath.suffix.lower() in IMAGE_EXTENSIONS:
                    images.append(fpath)
        return images

    def run(self):
        """تشغيل عملية التحسين"""
        start_time = time.time()

        print()
        print("═" * 65)
        print("     🖼️  سكريبت تحسين وضغط الصور - الوسيلة الذكية")
        print("═" * 65)
        print()

        if self.dry_run:
            print("⚡ وضع المعاينة (Dry Run) — لن يتم تعديل أي ملف")
            print()
        elif self.report_only:
            print("📊 وضع التقرير فقط — جمع معلومات بدون تعديل")
            print()

        # جمع الصور
        print("🔍 جاري البحث عن الصور...")
        images = self._collect_images()
        self.stats["total_files"] = len(images)
        print(f"   تم العثور على {len(images)} صورة")
        print()

        if not images:
            print("❌ لم يتم العثور على أي صور!")
            return

        # حساب الحجم الأصلي الإجمالي
        total_original = sum(f.stat().st_size for f in images)
        self.stats["original_total_bytes"] = total_original
        print(f"📦 الحجم الإجمالي الحالي: {self._format_size(total_original)}")
        print(f"🎯 جودة الضغط: {self.quality}%")
        print()

        if not self.dry_run and not self.report_only and not self.no_backup:
            print(f"💾 جاري إنشاء النسخ الاحتياطية في: {BACKUP_DIR.name}/")
            print()

        # معالجة الصور
        print("⚙️  جاري معالجة الصور...")
        print("─" * 65)

        processed_count = 0
        jpg_count = 0
        webp_count = 0

        # استخدام معالجة متزامنة لتسريع العملية
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(self._optimize_single, img): img for img in images}

            for future in as_completed(futures):
                result = future.result()
                self.stats["details"].append(result)
                processed_count += 1

                status = result["status"]
                filepath = result["file"]

                if status == "optimized":
                    self.stats["processed"] += 1
                    self.stats["optimized_total_bytes"] += result["optimized_size"]
                    savings_pct = result["savings_percent"]
                    icon = "✅"
                    # عدّ حسب النوع
                    if filepath.lower().endswith(('.jpg', '.jpeg')):
                        jpg_count += 1
                    elif filepath.lower().endswith('.webp'):
                        webp_count += 1
                    status_text = f"وُفّر {savings_pct}%"
                elif status in ("skipped_small", "skipped_minimal_savings", "report_only", "dry_run"):
                    self.stats["skipped"] += 1
                    self.stats["optimized_total_bytes"] += result["original_size"]
                    icon = "⏭️"
                    status_text = "تم تخطيه"
                else:
                    self.stats["errors"] += 1
                    self.stats["errors_list"].append(result)
                    self.stats["optimized_total_bytes"] += result["original_size"]
                    icon = "❌"
                    status_text = f"خطأ"

                # طباعة التقدم كل 50 صورة أو عند الأخطاء
                if processed_count % 100 == 0 or status.startswith("error") or processed_count == len(images):
                    progress = (processed_count / len(images)) * 100
                    print(f"   [{progress:5.1f}%] {processed_count}/{len(images)} — "
                          f"✅ {self.stats['processed']} محسّنة | "
                          f"⏭️ {self.stats['skipped']} متخطاة | "
                          f"❌ {self.stats['errors']} أخطاء")

        print("─" * 65)
        print()

        # حساب النتائج النهائية
        total_optimized = self.stats["optimized_total_bytes"]
        total_savings = total_original - total_optimized
        savings_percent = (total_savings / total_original) * 100 if total_original > 0 else 0

        elapsed = time.time() - start_time

        # عرض الملخص
        print("═" * 65)
        print("                    📊 ملخص النتائج")
        print("═" * 65)
        print()
        print(f"  📁 إجمالي الصور:           {self.stats['total_files']}")
        print(f"  ✅ تم تحسينها:             {self.stats['processed']}")
        print(f"     ├─ JPG:                 {jpg_count}")
        print(f"     └─ WEBP:                {webp_count}")
        print(f"  ⏭️  تم تخطيها:             {self.stats['skipped']}")
        print(f"  ❌ أخطاء:                  {self.stats['errors']}")
        print()
        print(f"  📦 الحجم الأصلي:           {self._format_size(total_original)}")
        print(f"  📦 الحجم بعد التحسين:      {self._format_size(total_optimized)}")
        print(f"  💰 التوفير:                {self._format_size(total_savings)} ({savings_percent:.1f}%)")
        print()
        print(f"  ⏱️  الوقت المستغرق:        {elapsed:.1f} ثانية")
        print()

        if self.stats["errors"] > 0:
            print("  ⚠️  الملفات التي بها أخطاء:")
            for err in self.stats["errors_list"][:10]:
                print(f"     - {err['file']}: {err['status']}")
            print()

        # حفظ التقرير
        self._save_report(elapsed)
        print(f"  📄 تم حفظ التقرير المفصل: {REPORT_FILE.name}")
        print()
        print("═" * 65)
        print("  ✅ اكتملت العملية بنجاح!")
        if not self.no_backup and not self.dry_run and not self.report_only:
            print(f"  💾 النسخ الاحتياطية محفوظة في: {BACKUP_DIR.name}/")
            print(f"     لاستعادتها: python optimize_images.py --restore")
        print("═" * 65)
        print()

    def _save_report(self, elapsed):
        """حفظ تقرير مفصل بصيغة JSON"""
        report = {
            "تاريخ_التشغيل": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "الوقت_المستغرق_ثانية": round(elapsed, 1),
            "جودة_الضغط": self.quality,
            "الوضع": "معاينة" if self.dry_run else ("تقرير_فقط" if self.report_only else "تحسين"),
            "إحصائيات": {
                "إجمالي_الصور": self.stats["total_files"],
                "تم_تحسينها": self.stats["processed"],
                "تم_تخطيها": self.stats["skipped"],
                "أخطاء": self.stats["errors"],
                "الحجم_الأصلي_بايت": self.stats["original_total_bytes"],
                "الحجم_الأصلي": self._format_size(self.stats["original_total_bytes"]),
                "الحجم_المحسّن_بايت": self.stats["optimized_total_bytes"],
                "الحجم_المحسّن": self._format_size(self.stats["optimized_total_bytes"]),
                "التوفير_بايت": self.stats["original_total_bytes"] - self.stats["optimized_total_bytes"],
                "التوفير": self._format_size(
                    self.stats["original_total_bytes"] - self.stats["optimized_total_bytes"]
                ),
                "نسبة_التوفير": round(
                    ((self.stats["original_total_bytes"] - self.stats["optimized_total_bytes"])
                     / self.stats["original_total_bytes"] * 100)
                    if self.stats["original_total_bytes"] > 0 else 0, 1
                ),
            },
            "تفاصيل_الملفات": sorted(
                self.stats["details"],
                key=lambda x: x.get("savings_percent", 0),
                reverse=True
            ),
        }

        with open(str(REPORT_FILE), 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _format_size(size_bytes):
        """تنسيق حجم الملف بطريقة مقروءة"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def restore_backups():
    """استعادة جميع النسخ الاحتياطية"""
    print()
    print("═" * 65)
    print("     🔄 استعادة النسخ الاحتياطية")
    print("═" * 65)
    print()

    if not BACKUP_DIR.exists():
        print("❌ لا يوجد مجلد نسخ احتياطية!")
        print(f"   المسار المتوقع: {BACKUP_DIR}")
        return

    restored = 0
    errors = 0

    for dirpath, _, filenames in os.walk(str(BACKUP_DIR)):
        for fname in filenames:
            backup_file = Path(dirpath) / fname
            rel_path = backup_file.relative_to(BACKUP_DIR)
            original_file = ROOT_DIR / rel_path

            try:
                original_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(backup_file), str(original_file))
                restored += 1
            except Exception as e:
                print(f"  ❌ فشل استعادة {rel_path}: {e}")
                errors += 1

    print(f"  ✅ تم استعادة {restored} ملف")
    if errors > 0:
        print(f"  ❌ فشل استعادة {errors} ملف")
    print()

    # سؤال عن حذف مجلد النسخ الاحتياطية
    answer = input("  هل تريد حذف مجلد النسخ الاحتياطية؟ (y/n): ").strip().lower()
    if answer == 'y':
        shutil.rmtree(str(BACKUP_DIR))
        print("  🗑️  تم حذف مجلد النسخ الاحتياطية")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="سكريبت تحسين وضغط الصور - الوسيلة الذكية",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة:
  python optimize_images.py                  # تشغيل الضغط بالإعدادات الافتراضية
  python optimize_images.py --dry-run        # معاينة النتائج بدون تعديل
  python optimize_images.py --quality 80     # ضغط أقوى (حجم أصغر، جودة أقل)
  python optimize_images.py --quality 90     # ضغط أخف (حجم أكبر، جودة أعلى)
  python optimize_images.py --restore        # استعادة النسخ الاحتياطية
  python optimize_images.py --report-only    # تقرير بالأحجام الحالية فقط
        """
    )

    parser.add_argument(
        '--quality', '-q',
        type=int,
        default=85,
        help='جودة الضغط (1-100). الافتراضي: 85 — توازن ممتاز بين الجودة والحجم'
    )
    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='معاينة فقط بدون تعديل أي ملف'
    )
    parser.add_argument(
        '--restore', '-r',
        action='store_true',
        help='استعادة الصور من النسخ الاحتياطية'
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='عدم إنشاء نسخ احتياطية (غير مستحسن)'
    )
    parser.add_argument(
        '--report-only',
        action='store_true',
        help='إنشاء تقرير فقط بأحجام الصور الحالية'
    )

    args = parser.parse_args()

    # التحقق من صحة جودة الضغط
    if not 1 <= args.quality <= 100:
        print("❌ جودة الضغط يجب أن تكون بين 1 و 100")
        sys.exit(1)

    # وضع الاستعادة
    if args.restore:
        restore_backups()
        return

    # تشغيل التحسين
    optimizer = ImageOptimizer(
        quality=args.quality,
        dry_run=args.dry_run,
        no_backup=args.no_backup,
        report_only=args.report_only,
    )
    optimizer.run()


if __name__ == '__main__':
    main()
