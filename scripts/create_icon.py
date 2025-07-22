#!/usr/bin/env python3
"""
YouTube Downloader 아이콘 생성기
YouTube 스타일의 아이콘을 생성하고 다양한 플랫폼 형식으로 변환
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_youtube_icon(size=512):
    """YouTube 스타일의 아이콘 생성"""
    
    # 배경색 (YouTube 빨간색)
    bg_color = (255, 0, 0)  # YouTube Red
    
    # 이미지 생성
    img = Image.new('RGBA', (size, size), bg_color)
    draw = ImageDraw.Draw(img)
    
    # 둥근 모서리 생성
    corner_radius = size // 8
    
    # 마스크 생성 (둥근 모서리)
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(
        [(0, 0), (size-1, size-1)], 
        radius=corner_radius, 
        fill=255
    )
    
    # 배경에 마스크 적용
    background = Image.new('RGBA', (size, size), bg_color)
    img = Image.composite(background, Image.new('RGBA', (size, size), (0,0,0,0)), mask)
    draw = ImageDraw.Draw(img)
    
    # 흰색 재생 삼각형 그리기
    triangle_size = size // 2.5
    center_x, center_y = size // 2, size // 2
    
    # 삼각형 좌표 계산 (약간 오른쪽으로 이동)
    offset_x = triangle_size // 8
    triangle_points = [
        (center_x - triangle_size//2 + offset_x, center_y - triangle_size//2),
        (center_x - triangle_size//2 + offset_x, center_y + triangle_size//2),
        (center_x + triangle_size//2 + offset_x, center_y)
    ]
    
    draw.polygon(triangle_points, fill=(255, 255, 255))
    
    # 그림자 효과 추가
    shadow_offset = size // 40
    shadow_triangle_points = [
        (p[0] + shadow_offset, p[1] + shadow_offset) 
        for p in triangle_points
    ]
    
    # 새 이미지에 그림자 그리기
    shadow_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_img)
    shadow_draw.polygon(shadow_triangle_points, fill=(0, 0, 0, 50))
    
    # 그림자를 원본 이미지 아래에 합성
    img = Image.alpha_composite(shadow_img, img)
    
    return img

def save_icon_formats(base_img):
    """다양한 형식으로 아이콘 저장"""
    
    # PNG 저장 (기본)
    base_img.save('youtube_downloader_icon.png', 'PNG')
    print("PNG 아이콘 저장: youtube_downloader_icon.png")
    
    # Windows ICO 형식
    sizes = [16, 24, 32, 48, 64, 128, 256]
    ico_images = []
    
    for size in sizes:
        ico_img = base_img.resize((size, size), Image.Resampling.LANCZOS)
        ico_images.append(ico_img)
    
    # ICO 파일 저장
    ico_images[0].save(
        'youtube_downloader_icon.ico',
        format='ICO',
        sizes=[(img.size[0], img.size[1]) for img in ico_images],
        append_images=ico_images[1:]
    )
    print("ICO 아이콘 저장: youtube_downloader_icon.ico")
    
    # macOS ICNS 형식을 위한 다양한 크기 생성
    icns_sizes = [16, 32, 64, 128, 256, 512, 1024]
    
    # 임시 디렉토리 생성
    os.makedirs('icon_temp', exist_ok=True)
    
    for size in icns_sizes:
        icns_img = base_img.resize((size, size), Image.Resampling.LANCZOS)
        icns_img.save(f'icon_temp/icon_{size}x{size}.png', 'PNG')
    
    print("ICNS 변환용 PNG 파일들 생성 완료")
    print("macOS에서 ICNS 생성을 위해 다음 명령을 실행하세요:")
    print("iconutil -c icns icon_temp -o youtube_downloader_icon.icns")

def create_icns_with_sips():
    """macOS sips를 사용해서 ICNS 생성"""
    try:
        import subprocess
        
        # iconutil을 사용해서 ICNS 생성
        cmd = ['iconutil', '-c', 'icns', 'icon_temp', '-o', 'youtube_downloader_icon.icns']
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("ICNS 아이콘 저장: youtube_downloader_icon.icns")
        
        # 임시 파일 정리
        import shutil
        shutil.rmtree('icon_temp')
        print("임시 파일 정리 완료")
        
        return True
        
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"ICNS 생성 실패: {e}")
        print("수동으로 다음 명령을 실행하세요:")
        print("iconutil -c icns icon_temp -o youtube_downloader_icon.icns")
        return False

if __name__ == "__main__":
    print("YouTube Downloader 아이콘 생성 중...")
    
    # 512x512 아이콘 생성
    icon = create_youtube_icon(512)
    
    # 다양한 형식으로 저장
    save_icon_formats(icon)
    
    # macOS ICNS 생성 시도
    if create_icns_with_sips():
        print("\n모든 아이콘 형식이 성공적으로 생성되었습니다!")
    else:
        print("\nICO와 PNG는 생성되었습니다. ICNS는 수동으로 생성하세요.")
    
    print("\n생성된 파일들:")
    print("- youtube_downloader_icon.png (기본 PNG)")
    print("- youtube_downloader_icon.ico (Windows용)")
    print("- youtube_downloader_icon.icns (macOS용, 생성되면)")