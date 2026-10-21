/*
  GO TO BED — phone carry test (one ESP32, two "panels")
  Draft, untested. Any ESP32 Arduino board (the SUNDIAL ELEGOO board is fine), ESP32 core 3.x.

  The question: does a phone's browser keep what one panel gave it, and hand it to the next panel?
  All GTB panels answer at http://192.168.4.1, so the browser treats them as the same site.

  This board pretends to be panel A or panel B. Each has its own Wi-Fi name and holds its own test block.
  1. Flash. The board starts as "gtb-test-A".
  2. Phone: join gtb-test-A, open http://192.168.4.1 (try both the Wi-Fi pop-up and a full browser).
     The page shows what the phone carries, and picks up panel A's block.
  3. Tap "switch panel" (or wait for the board to restart as B). The board restarts as "gtb-test-B".
  4. Phone: join gtb-test-B, open the page. If carrying works, the page delivers panel A's block to B,
     B shows "received block A", and the phone now also carries B's block.
  Record per phone and browser: did the block arrive? Did it survive closing the page / a day?
*/
#include <WiFi.h>
#include <WebServer.h>
#include <DNSServer.h>
#include <Preferences.h>

Preferences prefs;
WebServer server(80);
DNSServer dns;
char panel = 'A';
String received;   // blocks delivered to this panel (in RAM)

const char PAGE[] PROGMEM = R"HTML(<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>GTB carry test</title>
<style>body{font-family:sans-serif;margin:16px;max-width:520px}pre{background:#eee;padding:8px;white-space:pre-wrap}
button{font-size:1.1em;padding:10px 14px;margin:6px 0}</style></head><body>
<h2>GO TO BED · carry test · panel <span id=p>?</span></h2>
<p id=s>…</p><h3>This phone carries</h3><pre id=c></pre><h3>This panel has received</h3><pre id=r></pre>
<button onclick="sw()">switch panel (board restarts)</button>
<script>
let bag = {};
try { bag = JSON.parse(localStorage.getItem('gtbBag') || '{}'); } catch (e) { document.getElementById('s').textContent = 'storage unavailable: ' + e; }
async function go() {
  const info = await (await fetch('/info', {cache:'no-store'})).json();
  document.getElementById('p').textContent = info.panel;
  // deliver everything we carry that is not this panel's own
  const give = Object.values(bag).filter(b => b.panel !== info.panel);
  const res = await (await fetch('/deliver', {method:'POST', body: JSON.stringify(give)})).json();
  // pick up this panel's block
  bag[info.block.id] = info.block;
  try { localStorage.setItem('gtbBag', JSON.stringify(bag)); } catch (e) {}
  document.getElementById('s').textContent = give.length ? ('delivered ' + give.length + ' block(s); new to this panel: ' + res.new) : 'nothing to deliver yet (first panel?)';
  document.getElementById('c').textContent = Object.keys(bag).join('\n') || '(nothing)';
  document.getElementById('r').textContent = res.received || '(nothing yet)';
}
async function sw() { await fetch('/switch', {method:'POST'}); document.getElementById('s').textContent = 'switching… join the other gtb-test network'; }
go();
</script></body></html>)HTML";

void handleInfo() {
  String id = String(panel) + "/test";
  server.send(200, "application/json",
    "{\"panel\":\"" + String(panel) + "\",\"block\":{\"id\":\"" + id + "\",\"panel\":\"" + String(panel) +
    "\",\"messages\":[{\"text\":\"hello from panel " + String(panel) + "\"}]}}");
}
void handleDeliver() {
  String body = server.arg("plain");
  int n = 0;
  for (char q = 'A'; q <= 'B'; q++) {
    String id = String(q) + "/test";
    if (q != panel && body.indexOf("\"" + id + "\"") >= 0 && received.indexOf(id) < 0) { received += id + "\n"; n++; }
  }
  server.send(200, "application/json", "{\"new\":" + String(n) + ",\"received\":\"" + (received.length() ? received.substring(0, received.length() - 1) : "") + "\"}");
}
void handleSwitch() {
  server.send(200, "text/plain", "ok");
  prefs.putChar("panel", panel == 'A' ? 'B' : 'A');
  delay(300); ESP.restart();
}
void setup() {
  prefs.begin("gtbtest", false);
  panel = prefs.getChar("panel", 'A');
  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig(IPAddress(192,168,4,1), IPAddress(192,168,4,1), IPAddress(255,255,255,0));
  WiFi.softAP((String("gtb-test-") + panel).c_str());
  dns.start(53, "*", IPAddress(192,168,4,1));
  server.on("/", []() { server.send_P(200, "text/html", PAGE); });
  server.on("/info", handleInfo);
  server.on("/deliver", HTTP_POST, handleDeliver);
  server.on("/switch", HTTP_POST, handleSwitch);
  server.onNotFound([]() { server.sendHeader("Location", "http://192.168.4.1/", true); server.send(302, "text/plain", ""); });
  server.begin();
}
void loop() { dns.processNextRequest(); server.handleClient(); }
