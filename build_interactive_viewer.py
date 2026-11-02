import json
import os

SLIDES_JSON = r"H:\Youtube agent\slides\slides_manifest.json"
TRANSCRIPT_JSON = r"H:\Youtube agent\transcript.json"
OUT_HTML = r"H:\Youtube agent\SLIDES_AND_TRANSCRIPT_VIEWER.html"

def main():
    with open(SLIDES_JSON, "r", encoding="utf-8") as f:
        slides_data = json.load(f)["slides"]

    with open(TRANSCRIPT_JSON, "r", encoding="utf-8") as f:
        transcript_data = json.load(f)

    slides_js = json.dumps(slides_data)
    segments_js = json.dumps(transcript_data["segments"])

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>YouTube Agent - Presentation Slides & Full Transcript Viewer</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #0a0d14;
      --bg-card: rgba(18, 24, 38, 0.85);
      --border-color: rgba(255, 255, 255, 0.08);
      --accent: #3b82f6;
      --accent-hover: #60a5fa;
      --text-main: #f1f5f9;
      --text-muted: #94a3b8;
      --highlight: rgba(59, 130, 246, 0.25);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', -apple-system, sans-serif;
      background: var(--bg-dark);
      color: var(--text-main);
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}
    header {{
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-color);
      padding: 12px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 10;
    }}
    .header-title {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .badge {{
      background: linear-gradient(135deg, #2563eb, #1d4ed8);
      color: white;
      font-size: 11px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .header-links {{
      display: flex;
      gap: 10px;
    }}
    .btn {{
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 6px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }}
    .btn:hover {{
      background: rgba(255, 255, 255, 0.12);
      border-color: var(--accent);
      color: white;
    }}
    .btn-primary {{
      background: var(--accent);
      border-color: var(--accent);
    }}
    .btn-primary:hover {{
      background: var(--accent-hover);
    }}
    .main-container {{
      display: flex;
      flex: 1;
      height: calc(100vh - 65px);
      overflow: hidden;
    }}
    /* Left Slide Panel */
    .slide-panel {{
      flex: 1.25;
      display: flex;
      flex-direction: column;
      background: #06080d;
      border-right: 1px solid var(--border-color);
      position: relative;
    }}
    .slide-stage {{
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
      position: relative;
    }}
    .slide-img {{
      max-width: 100%;
      max-height: 100%;
      border-radius: 8px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.08);
      object-fit: contain;
      transition: opacity 0.15s ease;
    }}
    .slide-controls {{
      padding: 12px 24px;
      background: rgba(15, 23, 42, 0.9);
      border-top: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .slide-info {{
      display: flex;
      align-items: center;
      gap: 14px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
    }}
    .timestamp-tag {{
      background: rgba(59, 130, 246, 0.15);
      color: var(--accent-hover);
      padding: 3px 8px;
      border-radius: 4px;
      border: 1px solid rgba(59, 130, 246, 0.3);
    }}
    .filmstrip {{
      height: 96px;
      background: #090d16;
      border-top: 1px solid var(--border-color);
      display: flex;
      gap: 8px;
      padding: 10px;
      overflow-x: auto;
      overflow-y: hidden;
      white-space: nowrap;
    }}
    .filmstrip::-webkit-scrollbar {{ height: 6px; }}
    .filmstrip::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.2); border-radius: 3px; }}
    .thumb-item {{
      flex: 0 0 130px;
      height: 100%;
      border-radius: 6px;
      cursor: pointer;
      position: relative;
      border: 2px solid transparent;
      overflow: hidden;
      transition: all 0.15s;
    }}
    .thumb-item img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}
    .thumb-item.active {{
      border-color: var(--accent);
      box-shadow: 0 0 12px rgba(59, 130, 246, 0.5);
    }}
    .thumb-badge {{
      position: absolute;
      bottom: 2px;
      right: 4px;
      background: rgba(0,0,0,0.75);
      font-size: 9px;
      font-family: 'JetBrains Mono', monospace;
      padding: 1px 4px;
      border-radius: 3px;
    }}

    /* Right Transcript Panel */
    .transcript-panel {{
      flex: 0.95;
      display: flex;
      flex-direction: column;
      background: #0f172a;
    }}
    .search-bar-container {{
      padding: 14px 20px;
      border-bottom: 1px solid var(--border-color);
      background: rgba(18, 24, 38, 0.7);
    }}
    .search-input {{
      width: 100%;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 13px;
      outline: none;
      transition: border-color 0.2s;
    }}
    .search-input:focus {{
      border-color: var(--accent);
    }}
    .transcript-list {{
      flex: 1;
      overflow-y: auto;
      padding: 16px 20px;
    }}
    .transcript-list::-webkit-scrollbar {{ width: 6px; }}
    .transcript-list::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.2); border-radius: 3px; }}
    .segment-item {{
      padding: 10px 12px;
      border-radius: 8px;
      margin-bottom: 8px;
      cursor: pointer;
      transition: background 0.15s;
      border-left: 3px solid transparent;
    }}
    .segment-item:hover {{
      background: rgba(255, 255, 255, 0.04);
    }}
    .segment-item.active {{
      background: var(--highlight);
      border-left-color: var(--accent);
    }}
    .segment-meta {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 4px;
    }}
    .segment-time {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: var(--accent-hover);
      font-weight: 500;
    }}
    .segment-text {{
      font-size: 13.5px;
      line-height: 1.5;
      color: #cbd5e1;
    }}
  </style>
</head>
<body>
  <header>
    <div class="header-title">
      <h2>YouTube Presentation & Transcript Studio</h2>
      <span class="badge">Shane Hummus Webinar</span>
    </div>
    <div class="header-links">
      <a class="btn btn-primary" href="extracted_slides.pdf" target="_blank">📄 Download Slides PDF (206 Slides)</a>
      <a class="btn" href="FULL_TRANSCRIPT.md" target="_blank">📝 Markdown Transcript</a>
      <a class="btn" href="transcript.srt" download>⏱️ Subtitles (.SRT)</a>
      <a class="btn" href="transcript.txt" download>📄 Text (.TXT)</a>
    </div>
  </header>

  <div class="main-container">
    <!-- Left: Slide View -->
    <div class="slide-panel">
      <div class="slide-stage">
        <img id="current-slide" class="slide-img" src="" alt="Slide">
      </div>
      <div class="slide-controls">
        <div class="slide-info">
          <span id="slide-num">Slide 1 of 206</span>
          <span id="slide-time" class="timestamp-tag">00:12:50</span>
        </div>
        <div style="display: flex; gap: 8px;">
          <button class="btn" onclick="prevSlide()">◀ Prev (Left Arrow)</button>
          <button class="btn btn-primary" onclick="nextSlide()">Next (Right Arrow) ▶</button>
        </div>
      </div>
      <div class="filmstrip" id="filmstrip"></div>
    </div>

    <!-- Right: Transcript View -->
    <div class="transcript-panel">
      <div class="search-bar-container">
        <input type="text" id="search-box" class="search-input" placeholder="🔍 Search transcript text... (30,873 words)">
      </div>
      <div class="transcript-list" id="transcript-list"></div>
    </div>
  </div>

  <script>
    const slides = {slides_js};
    const segments = {segments_js};

    let currentIndex = 0;

    const imgEl = document.getElementById('current-slide');
    const numEl = document.getElementById('slide-num');
    const timeEl = document.getElementById('slide-time');
    const filmstripEl = document.getElementById('filmstrip');
    const transcriptListEl = document.getElementById('transcript-list');
    const searchBox = document.getElementById('search-box');

    function renderSlide(index) {{
      if (index < 0) index = 0;
      if (index >= slides.length) index = slides.length - 1;
      currentIndex = index;

      const slide = slides[currentIndex];
      imgEl.src = 'slides/' + slide.filename;
      numEl.textContent = `Slide ${{slide.slide_number}} of ${{slides.length}}`;
      timeEl.textContent = slide.timestamp_formatted;

      // Update filmstrip active state
      document.querySelectorAll('.thumb-item').forEach((item, i) => {{
        item.classList.toggle('active', i === currentIndex);
      }});

      // Auto scroll filmstrip
      const activeThumb = filmstripEl.children[currentIndex];
      if (activeThumb) {{
        activeThumb.scrollIntoView({{ behavior: 'smooth', block: 'nearest', inline: 'center' }});
      }}

      // Highlight closest segment
      highlightTranscriptForTime(slide.timestamp_seconds);
    }}

    function nextSlide() {{ renderSlide(currentIndex + 1); }}
    function prevSlide() {{ renderSlide(currentIndex - 1); }}

    // Build filmstrip
    slides.forEach((slide, idx) => {{
      const div = document.createElement('div');
      div.className = 'thumb-item' + (idx === 0 ? ' active' : '');
      div.onclick = () => renderSlide(idx);
      div.innerHTML = `
        <img src="slides/${{slide.filename}}" loading="lazy" alt="Slide ${{slide.slide_number}}">
        <span class="thumb-badge">${{slide.timestamp_formatted}}</span>
      `;
      filmstripEl.appendChild(div);
    }});

    // Build transcript list
    function renderTranscript(filter = '') {{
      transcriptListEl.innerHTML = '';
      const filterLower = filter.toLowerCase();

      segments.forEach((seg, i) => {{
        if (filter && !seg.text.toLowerCase().includes(filterLower)) return;

        const item = document.createElement('div');
        item.className = 'segment-item';
        item.dataset.index = i;
        item.dataset.start = seg.start;
        item.onclick = () => {{
          jumpToClosestSlide(seg.start);
        }};

        const startMin = Math.floor(seg.start / 60);
        const startSec = Math.floor(seg.start % 60);
        const timeFormatted = `${{String(startMin).padStart(2, '0')}}:${{String(startSec).padStart(2, '0')}}`;

        item.innerHTML = `
          <div class="segment-meta">
            <span class="segment-time">${{timeFormatted}}</span>
          </div>
          <div class="segment-text">${{highlightText(seg.text, filter)}}</div>
        `;
        transcriptListEl.appendChild(item);
      }});
    }}

    function highlightText(text, query) {{
      if (!query) return text;
      const regex = new RegExp(`(${{query}})`, 'gi');
      return text.replace(regex, '<mark style="background:#f59e0b;color:#000;border-radius:2px;padding:0 2px;">$1</mark>');
    }}

    function jumpToClosestSlide(timeSec) {{
      // Find the slide that appeared at or immediately before this timestamp
      let bestIndex = 0;
      for (let i = 0; i < slides.length; i++) {{
        if (slides[i].timestamp_seconds <= timeSec) {{
          bestIndex = i;
        }} else {{
          break;
        }}
      }}
      renderSlide(bestIndex);
    }}

    function highlightTranscriptForTime(timeSec) {{
      let activeItem = null;
      document.querySelectorAll('.segment-item').forEach(el => {{
        const start = parseFloat(el.dataset.start);
        if (Math.abs(start - timeSec) < 30 && !activeItem) {{
          activeItem = el;
        }}
        el.classList.remove('active');
      }});

      if (activeItem) {{
        activeItem.classList.add('active');
        activeItem.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      }}
    }}

    // Keybindings
    window.addEventListener('keydown', (e) => {{
      if (document.activeElement === searchBox) return;
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'j') nextSlide();
      if (e.key === 'ArrowLeft' || e.key === 'k') prevSlide();
    }});

    // Search filter
    searchBox.addEventListener('input', (e) => {{
      renderTranscript(e.target.value);
    }});

    // Initialize
    renderSlide(0);
    renderTranscript();
  </script>
</body>
</html>
"""

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated standalone interactive studio: {OUT_HTML}")

if __name__ == "__main__":
    main()
