#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rafat Emad - Professional Tech Intro Video Generator
مولد فيديوهات تقديمية احترافية مع صورة شخصية و دوائر ملونة

Author: Rafat Emad
Email: rafatalazawi86@gmail.com
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw
import os
import sys
from pathlib import Path
from math import cos, sin, pi, sqrt
import urllib.request
from datetime import datetime

class RafatIntroVideoGenerator:
    def __init__(self, profile_image_path=None, output_path='output/rafat_intro_video.mp4'):
        """
        إنشاء مولد الفيديو التقديمي
        
        Args:
            profile_image_path: مسار صورة الملف الشخصي
            output_path: مسار حفظ الفيديو النهائي
        """
        self.profile_image_path = profile_image_path or 'assets/profile_pic.jpg'
        self.output_path = output_path
        
        # إعدادات الفيديو
        self.width = 1920
        self.height = 1080
        self.fps = 60
        self.duration = 8  # ثواني
        self.total_frames = int(self.fps * self.duration)
        
        # إنشاء مجلد الإخراج
        Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # معلومات رافات
        self.name = "Rafat Emad"
        self.subtitle = "Digital Creator"
        
        # الألوان (BGR)
        self.colors = {
            'circle_1': (255, 100, 150),   # وردي
            'circle_2': (100, 200, 255),   # أزرق فاتح
            'circle_3': (100, 255, 150),   # أخضر فاتح
            'circle_4': (255, 200, 100),   # برتقالي
            'circle_5': (200, 100, 255),   # بنفسجي
            'circle_6': (255, 255, 100),   # أصفر فاتح
            'white': (255, 255, 255),
            'text_main': (255, 255, 255),
        }
        
        # منصات التواصل الاجتماعي
        self.social_media = [
            {'name': 'Instagram', 'icon': 'I', 'color': (100, 200, 255)},
            {'name': 'Facebook', 'icon': 'F', 'color': (100, 150, 200)},
            {'name': 'Twitter', 'icon': 'X', 'color': (100, 200, 200)},
            {'name': 'LinkedIn', 'icon': 'L', 'color': (100, 180, 255)},
            {'name': 'YouTube', 'icon': 'Y', 'color': (100, 100, 255)},
            {'name': 'TikTok', 'icon': 'T', 'color': (200, 100, 200)},
        ]
    
    def load_profile_image(self, size=300):
        """
        تحميل صورة الملف الشخصي وتحويلها إلى دائرة
        """
        try:
            # تحميل الصورة
            img = Image.open(self.profile_image_path)
            
            # تحويل إلى RGB إذا لزم الأمر
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # تغيير الحجم
            img = img.resize((size, size), Image.Resampling.LANCZOS)
            
            # إنشاء قناع دائري
            mask = Image.new('L', (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse([0, 0, size, size], fill=255)
            
            # تطبيق القناع
            img.putalpha(mask)
            
            return np.array(img)
        except Exception as e:
            print(f"⚠️ خطأ في تحميل الصورة: {e}")
            return self.create_placeholder_circle(size)
    
    def create_placeholder_circle(self, size=300):
        """
        إنشاء دائرة بديلة في حالة عدم وجود الصورة
        """
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([0, 0, size, size], fill=(100, 150, 255, 200))
        return np.array(img)
    
    def create_background(self, frame_idx):
        """
        إنشاء خلفية متدرجة ومتحركة
        """
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        progress = frame_idx / self.total_frames
        
        # خلفية متدرجة ديناميكية
        for y in range(self.height):
            for x in range(self.width):
                ratio = (x + y) / (self.width + self.height)
                
                # ألوان متغيرة بناءً على التقدم
                b = int(40 + 60 * sin(progress * pi) + 30 * cos(ratio * pi))
                g = int(50 + 50 * sin(progress * pi + 1) + 20 * cos(ratio * pi))
                r = int(100 + 80 * sin(progress * pi + 2) + 40 * cos(ratio * pi))
                
                frame[y, x] = [b, g, r]
        
        return frame
    
    def draw_colored_circles(self, frame, frame_idx):
        """
        رسم دوائر ملونة تدور حول الصورة
        """
        center_x = self.width // 2
        center_y = self.height // 2
        progress = frame_idx / self.total_frames
        
        circle_colors = list(self.colors.values())[:6]
        num_circles = len(circle_colors)
        
        for i, color in enumerate(circle_colors):
            # حساب الزاوية (تدوير سلس)
            angle = (2 * pi * i / num_circles) + (progress * 2 * pi)
            
            # المسافة من المركز
            distance = 280 + 40 * sin(progress * 2 * pi)
            
            # إحداثيات الدائرة
            circle_x = int(center_x + distance * cos(angle))
            circle_y = int(center_y + distance * sin(angle))
            
            # حجم الدائرة (نبض)
            base_radius = 60
            pulse = 20 * sin(progress * 4 * pi + i * pi / 3)
            radius = int(base_radius + pulse)
            
            # رسم الدائرة مع توهج
            cv2.circle(frame, (circle_x, circle_y), radius + 5, color, -1)
            cv2.circle(frame, (circle_x, circle_y), radius, color, -1)
            
            # إضافة حدود براقة
            cv2.circle(frame, (circle_x, circle_y), radius + 10, 
                      tuple(min(255, c + 50) for c in color), 2)
        
        return frame
    
    def blend_image_on_frame(self, frame, img_overlay, x, y, alpha):
        """
        دمج صورة شفافة على الإطار
        """
        h, w = img_overlay.shape[:2]
        
        if w + x > frame.shape[1] or h + y > frame.shape[0]:
            # تقليص الحجم إذا كان يتجاوز الحدود
            w = min(w, frame.shape[1] - x)
            h = min(h, frame.shape[0] - y)
            img_overlay = img_overlay[:h, :w]
        
        if img_overlay.shape[2] == 4:  # RGBA
            img_alpha = img_overlay[:, :, 3] / 255.0 * alpha
            img_rgb = img_overlay[:, :, :3]
        else:
            img_alpha = np.ones((h, w)) * alpha
            img_rgb = img_overlay
        
        for c in range(3):
            frame[y:y+h, x:x+w, c] = (
                frame[y:y+h, x:x+w, c] * (1 - img_alpha) +
                img_rgb[:, :, c] * img_alpha
            ).astype(np.uint8)
    
    def add_text(self, frame, text, position, font_size, thickness, color, font=None):
        """
        إضافة نص إلى الإطار مع تأثير توهج
        """
        if font is None:
            font = cv2.FONT_HERSHEY_BOLD
        
        # النص الرئيسي
        cv2.putText(frame, text, position, font, font_size, color, thickness, cv2.LINE_AA)
        
        return frame
    
    def draw_social_icons(self, frame, frame_idx):
        """
        رسم أيقونات التواصل الاجتماعي مع حركات
        """
        progress = frame_idx / self.total_frames
        
        if progress < 0.5:  # ظهور الأيقونات بعد 4 ثوان
            return frame
        
        icons_progress = (progress - 0.5) * 2
        icon_y = self.height - 120
        spacing = self.width // (len(self.social_media) + 1)
        
        for idx, social in enumerate(self.social_media):
            icon_x = spacing * (idx + 1)
            
            # حركة القفز
            bounce = abs(sin(icons_progress * pi * 2 - idx * pi / len(self.social_media)))
            offset_y = int(bounce * 30)
            
            final_y = icon_y - offset_y
            radius = int(45 + 15 * bounce)
            
            # رسم خلفية الأيقونة
            cv2.circle(frame, (icon_x, final_y), radius, social['color'], -1)
            
            # إضافة حدود براقة
            cv2.circle(frame, (icon_x, final_y), radius + 3, (255, 255, 255), 2)
            
            # كتابة الحرف
            text = social['icon']
            cv2.putText(frame, text, (icon_x - 20, final_y + 25),
                       cv2.FONT_HERSHEY_BOLD, 2, (255, 255, 255), 3, cv2.LINE_AA)
        
        return frame
    
    def generate_video(self):
        """
        إنشاء الفيديو التقديمي الكامل
        """
        print("\n" + "="*60)
        print("🎬 مولد الفيديو التقديمي - Rafat Emad")
        print("="*60)
        print(f"📹 الدقة: {self.width}x{self.height}")
        print(f"⏱️ المدة: {self.duration} ثواني")
        print(f"📊 عدد الإطارات: {self.total_frames}")
        print(f"🎥 معدل الإطارات: {self.fps} fps")
        print("="*60)
        
        # تحميل الصورة
        print("\n📸 جاري تحميل صورة الملف الشخصي...")
        profile_img = self.load_profile_image(size=300)
        print("✅ تم تحميل الصورة بنجاح")
        
        # إنشاء كاتب الفيديو
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.output_path, fourcc, self.fps,
                              (self.width, self.height))
        
        if not out.isOpened():
            print("❌ خطأ: لم يتمكن من فتح كاتب الفيديو")
            return False
        
        center_x = self.width // 2
        center_y = self.height // 2 - 100
        
        print("\n🎨 جاري إنشاء الفيديو...")
        
        for frame_idx in range(self.total_frames):
            # إنشاء الخلفية
            frame = self.create_background(frame_idx)
            
            # رسم الدوائر الملونة
            frame = self.draw_colored_circles(frame, frame_idx)
            
            # حساب التقدم
            progress = frame_idx / self.total_frames
            
            # عرض الصورة الشخصية (تكبير وتصغير وتلاشي)
            if progress > 0.1:
                scale = 0.5 + 0.5 * sin((progress - 0.1) * pi)
                profile_size = int(300 * scale)
                alpha = min(1.0, (progress - 0.1) * 4)
                
                profile_resized = cv2.resize(profile_img, (profile_size, profile_size))
                x = center_x - profile_size // 2
                y = center_y - profile_size // 2
                
                self.blend_image_on_frame(frame, profile_resized, x, y, alpha)
            
            # عرض الاسم
            if progress > 0.2:
                name_alpha = min(1.0, (progress - 0.2) * 3)
                name_color = tuple(int(c * name_alpha) for c in self.colors['text_main'])
                
                text_size = cv2.getTextSize(self.name, cv2.FONT_HERSHEY_BOLD, 3, 3)[0]
                text_x = (self.width - text_size[0]) // 2
                text_y = center_y + 200
                
                frame = self.add_text(frame, self.name, (text_x, text_y), 3, 4, 
                                    name_color)
            
            # عرض الترجمة
            if progress > 0.35:
                subtitle_alpha = min(1.0, (progress - 0.35) * 3)
                subtitle_color = (int(200 * subtitle_alpha), 
                                int(200 * subtitle_alpha), 
                                int(255 * subtitle_alpha))
                
                text_size = cv2.getTextSize(self.subtitle, cv2.FONT_HERSHEY_SIMPLEX, 2, 2)[0]
                text_x = (self.width - text_size[0]) // 2
                text_y = center_y + 260
                
                cv2.putText(frame, self.subtitle, (text_x, text_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 2, subtitle_color, 2, cv2.LINE_AA)
            
            # رسم أيقونات التواصل
            frame = self.draw_social_icons(frame, frame_idx)
            
            # كتابة الإطار
            out.write(frame)
            
            # عرض التقدم
            if (frame_idx + 1) % 30 == 0:
                percent = int((frame_idx + 1) / self.total_frames * 100)
                bar_length = 40
                filled = int(bar_length * (frame_idx + 1) / self.total_frames)
                bar = '█' * filled + '░' * (bar_length - filled)
                print(f"\r[{bar}] {percent}% ({frame_idx + 1}/{self.total_frames})", end='')
        
        # إغلاق الكاتب
        out.release()
        
        print("\n\n" + "="*60)
        print(f"✅ تم إنشاء الفيديو بنجاح!")
        print(f"📁 المسار: {os.path.abspath(self.output_path)}")
        print(f"📊 الحجم: {os.path.getsize(self.output_path) / (1024*1024):.2f} MB")
        print("="*60 + "\n")
        
        return True

def main():
    """
    الدالة الرئيسية
    """
    print("\n🎬 مرحباً بك في مولد الفيديوهات التقديمية الاحترافي")
    print("برنامج متخصص لـ: Rafat Emad\n")
    
    # تحديد مسار الصورة
    profile_pic = 'assets/profile_pic.jpg'
    
    # التحقق من وجود الصورة
    if not os.path.exists(profile_pic):
        print(f"⚠️ تحذير: لم يتم العثور على الصورة في {profile_pic}")
        print("سيتم استخدام صورة بديلة...\n")
    
    # إنشاء المولد
    generator = RafatIntroVideoGenerator(
        profile_image_path=profile_pic,
        output_path='output/rafat_intro_video.mp4'
    )
    
    # إنشاء الفيديو
    success = generator.generate_video()
    
    if success:
        print("🎉 تم إنشاء الفيديو بنجاح!")
        print("📺 يمكنك الآن استخدام الفيديو في بداية فيديوهاتك التقنية")
    else:
        print("❌ حدث خطأ أثناء إنشاء الفيديو")
        sys.exit(1)

if __name__ == '__main__':
    main()
