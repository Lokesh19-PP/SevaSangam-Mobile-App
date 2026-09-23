# Yash-Thakur — Antigravity Prompt Pack (SevaSangam AI & Integrations)

**You own:** the AI/ML layer (`backend/app/ai/`) — smart matching, fair-distribution analytics, demand forecasting, OCR — plus Twilio integration.

**Wait for Lokesh's Prompts 1–3** (schema) before starting. You can work in parallel with Yash once the schema lands; sync with him whenever your endpoint needs a new route mounted.

Before every prompt: paste `docs/ANTIGRAVITY_CONTEXT.md` as the first message in a new session, then paste the numbered prompt.

---

### Prompt 1 — Smart matching service
```
Build backend/app/ai/matching.py: a scikit-learn-based scoring function that ranks candidate workers for a booking by combining skill match, distance (using Lokesh's geo helpers), availability, rating, and current workload — with workload weighted so busier workers rank lower (this is the "fair job distribution" differentiator, not just nearest/highest-rated). Return the top match plus a short, mobile-displayable reason string like "Skilled · Nearby · Available · Fair share" (the exact phrase Janhvi's mobile Worker List screen expects — keep the format short and human-readable). Write it as a pure, testable function first, then wire it into Yash's POST /bookings as the real matching_service (replacing his nearest-worker stub).
```
**Commit:** `feat(ai): implement scikit-learn smart matching with skill+distance+availability+rating+workload scoring`

---

### Prompt 2 — Fairness & utilisation analytics
```
Build backend/app/ai/fairness.py: compute per-worker jobs-assigned counts over a rolling window, utilisation % (overall / per skill / per cooperative), and a fairness score/gauge value with a plain-language explanation string. Build app/api/v1/admin/analytics_utilization.py exposing this (GET /admin/analytics/utilization) matching the shape Ashana's Fair Distribution mobile screen expects (jobs-per-worker distribution, utilisation %, fairness score+explanation, under-utilised/over-loaded worker lists).
```
**Commit:** `feat(ai): add fairness/utilisation analytics computation and admin endpoint`

---

### Prompt 3 — AI demand forecasting
```
Build backend/app/ai/forecasting.py: a lightweight time-series forecast (a simple scikit-learn regression or moving-average-based model is fine for an MVP — don't over-engineer) predicting booking demand for the next 7 days by service category, trained/computed from the seeded booking history. Build app/api/v1/admin/analytics_forecast.py (GET /admin/analytics/forecast?days=7) returning the shape Ashana's Analytics & Forecast mobile screen expects. Document the model's limitations honestly in docs/ai/MODEL_NOTES.md (it's a hackathon MVP, not a production forecasting system).
```
**Commit:** `feat(ai): add 7-day demand forecasting model and admin forecast endpoint`

---

### Prompt 4 — OCR pipeline for certificate verification
```
Build backend/app/ai/ocr.py: OpenCV preprocessing (deskew/threshold) + Tesseract OCR on an uploaded certificate image, returning { text, confidence }. Wire it into Yash's POST /workers/{id}/certificates endpoint (replace his TODO stub) so a newly uploaded certificate gets an OCR pass and the result is stored for Ashana's CertificateViewer screen to display. Handle low-confidence/unreadable images gracefully (return a clear low-confidence result, never crash the upload).
```
**Commit:** `feat(ai): add OpenCV+Tesseract OCR pipeline for certificate verification`

---

### Prompt 5 — Twilio integration (mock-first)
```
Build backend/app/integrations/twilio_client.py: a thin wrapper around Twilio SMS/WhatsApp send, defaulting to a MOCK mode (logs the message instead of sending) controlled by an env flag, matching the "never wire real Twilio unless explicitly told" rule. Wire it into two places: the OTP request flow (Yash's auth.py, behind the same mock flag he already uses) and a new-booking/emergency-assigned notification. Document how to flip it to live mode later in docs/api/INTEGRATIONS.md, including required Twilio env vars (never commit real credentials).
```
**Commit:** `feat(integrations): add mock-first Twilio wrapper for OTP and booking notifications`

---

### Prompt 6 — Contract check with mobile AI-facing screens
```
Read Janhvi's Worker List "best match" reason usage, Ashana's Fair Distribution and Analytics & Forecast mobile screens (or their prompt files if the screens aren't built yet), and confirm your endpoints from Prompts 1-3 return exactly the field names/shapes those screens expect. Log any gaps in docs/api/MOBILE_API_REQUESTS.md under an "AI endpoints" section and fix what's clearly a naming mismatch now.
```
**Commit:** `docs(ai): reconcile AI/analytics endpoint shapes against mobile screen expectations`