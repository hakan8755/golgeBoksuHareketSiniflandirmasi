
import argparse, time, sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from yt_dlp import YoutubeDL
from tqdm import tqdm

def get_driver(headless: bool = True) -> webdriver.Chrome:
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")

   
    chromedriver_path = "C:/Users/firat/OneDrive/Masaüstü/chromedriver-win64/chromedriver.exe"
    service = Service(chromedriver_path)

    return webdriver.Chrome(service=service, options=opts)


def download_video(url: str, dest: Path):
    ydl_opts = {
        "outtmpl": str(dest / "%(title).60s.%(ext)s"), 
        "format": "mp4",
        "quiet": True,
        "noplaylist": True,
        "retries": 3,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"✔ İndirildi: {url}")
    except Exception as e:
        print(f"✘ İndirme hatası: {e} | {url}")


def scrape(search: str, dest: Path, limit: int | None, delay: float = 1.5):
    dest.mkdir(parents=True, exist_ok=True)
    driver = get_driver(headless=True)

    search_url = f"https://www.youtube.com/results?search_query={search.replace(' ', '+')}"
    driver.get(search_url)
    time.sleep(3)

    seen, count = set(), 0
    pbar = tqdm(total=limit or 0, unit="video", desc="İndirilen")

    try:
        while True:
            for a in driver.find_elements(By.CSS_SELECTOR, "a#video-title"):
                href = a.get_attribute("href")
                if not href or "watch?v=" not in href:
                    continue

                href = href.split("&")[0]
                if href in seen:
                    continue

                seen.add(href)
                download_video(href, dest)
                count += 1
                pbar.update(1)

                if limit and count >= limit:
                    raise KeyboardInterrupt

            driver.execute_script("window.scrollBy(0, document.documentElement.scrollHeight);")
            time.sleep(delay)

    except KeyboardInterrupt:
        print("\n⏹️  Kullanıcı tarafından durduruldu.")
    finally:
        driver.quit()
        pbar.close()
        print(f"🟢 Toplam indirilen video: {count}")


def parse_args():
    parser = argparse.ArgumentParser(description="Gölge boksu video indirici (yt-dlp + selenium)")
    parser.add_argument("-s", "--search", default="uppercut boxing",
                        help="YouTube arama terimi (varsayılan: uppercut boxing)")
    parser.add_argument("-l", "--limit", type=int, default=None,
                        help="Kaç video indirilsin (örnek: -l 10)")
    parser.add_argument("-o", "--output", default="raw_videos",
                        help="İndirilen videoların klasörü (varsayılan: ./raw_videos)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        scrape(args.search, Path(args.output), args.limit)
    except Exception as e:
        print("⚠️  Beklenmeyen hata:", e)
        sys.exit(1)
