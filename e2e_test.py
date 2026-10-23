import asyncio, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True,
              args=["--autoplay-policy=no-user-gesture-required","--no-sandbox"])
        pg = await b.new_page(viewport={"width":1400,"height":1000})
        errs=[]; pg.on("console", lambda m: errs.append(m.type+": "+m.text) if m.type in("error","warning") else None)
        pg.on("pageerror", lambda e: errs.append("pageerror: "+str(e)))
        await pg.goto("http://localhost:8080/")
        await pg.wait_for_timeout(800)
        print("badge:", await pg.text_content("#modeBadge"))
        await pg.fill("#q","Beethoven sonata")
        await pg.click("#searchForm button")
        await pg.wait_for_selector("#results .item", timeout=30000)
        print("results:", await pg.locator("#results .item").count(), "|", await pg.text_content("#searchInfo"))
        print("first:", await pg.locator("#results .item .t").first.text_content())
        await pg.locator("#results .item").first.click()
        await pg.wait_for_selector("#tracks .item", timeout=30000)
        print("tracks:", await pg.locator("#tracks .item").count())
        await pg.locator("#tracks .item button[data-a=play]").first.click()
        await pg.wait_for_function("document.getElementById('audio').currentTime > 3", timeout=60000)
        await pg.wait_for_timeout(2500)
        st = await pg.evaluate("""() => { const a=document.getElementById('audio');
           const f=new Float32Array(N.analyser.frequencyBinCount); N.analyser.getFloatFrequencyData(f);
           let mx=-Infinity; for(const v of f) if(v>mx) mx=v;
           return {src:a.currentSrc, t:a.currentTime, dur:a.duration, paused:a.paused, ctx:ctx.state, sr:ctx.sampleRate, maxDb:mx,
                   fmt:document.getElementById('nowFmt').innerText, title:document.getElementById('nowTitle').innerText, peak:document.getElementById('peakTxt').innerText}; }""")
        print(json.dumps(st, ensure_ascii=False, indent=1))
        # DSP: apply preset, bypass, seek
        await pg.click("#presets button:nth-child(2)")
        await pg.keyboard.press("b"); await pg.wait_for_timeout(300)
        bp = await pg.evaluate("[N.bypass.gain.value.toFixed(2), N.proc.gain.value.toFixed(2), N.eq[0].gain.value.toFixed(1)]")
        print("bypass on -> bypassGain, procGain, eq31:", bp)
        await pg.keyboard.press("b")
        await pg.evaluate("document.getElementById('audio').currentTime = 600")
        await pg.wait_for_timeout(4000)
        print("after seek t=", await pg.evaluate("document.getElementById('audio').currentTime"))
        print("localStorage:", (await pg.evaluate("localStorage.getItem('losslessPlayer.settings.v1')"))[:200])
        await pg.screenshot(path="/workspace/lossless-player-screenshot.png")
        await pg.set_viewport_size({"width":420,"height":900}); await pg.wait_for_timeout(300)
        await pg.screenshot(path="/tmp/mobile.png")
        print("console issues:", errs[:10])
        await b.close()
asyncio.run(main())
