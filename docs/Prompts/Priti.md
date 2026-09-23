# Priti — Antigravity Prompt Pack (SevaSangam Mobile)

**You own:** **Worker dashboard** (`screens/worker`, `components/worker`, `hooks/worker`), `components/common`/`components/forms`/`components/charts`, `services/api/*` + `apiClient.js` + `mockApi.js`.

**Wait for Ashana's Prompts 1–4** (scaffold, i18n, navigation, AuthContext) to be merged before starting. Your Prompts 1–2 (API layer + mockApi) are themselves foundational — Ashana's admin screens and Janhvi's customer screens both depend on them, so do those first and merge fast.

Before every prompt: paste `docs/ANTIGRAVITY_MOBILE_CONTEXT.md` as the first message in a new session, then paste the numbered prompt.

---

### Prompt 1 — apiClient.js + env wiring
```
Create src/config/env.js as the ONLY file reading process.env — exports { USE_MOCK, API_BASE_URL } from EXPO_PUBLIC_* vars. Create services/apiClient.js: the single switch point between mock/mockApi.js and a future FastAPI fetch client, using USE_MOCK from env.js. It must expose one consistent call signature (e.g. apiClient.get/post/put/delete(path, opts)) so that flipping EXPO_PUBLIC_USE_MOCK later requires touching only this file, never screens or hooks. Include the Android emulator (10.0.2.2) vs physical device (LAN IP) note as a code comment referencing .env.example.
```
**Commit:** `feat(mobile-core): add apiClient.js as the single mock/live switch point`

---

### Prompt 2 — mockApi.js core
```
Build mock/mockApi.js: simulates latency (300-800ms random), supports pagination (page/limit), filters and search on list endpoints, and can inject errors behind a dev flag so loading/error states get properly tested. Response shapes must match the entity table in the context doc exactly. Include a role-based rejection: admin-namespaced calls made by a non-admin session must reject the same way the real backend will. This is the single source every services/api/*.js file will call through apiClient.js.
```
**Commit:** `feat(mobile-core): build mockApi.js with pagination, filters, search and error injection`

---

### Prompt 3 — services/api files (skeletons + core ones)
```
Create services/api/ with one file per domain matching section 6's list (authApi, servicesApi, workersApi, bookingsApi, emergencyApi, reviewsApi, jobsApi, earningsApi, profileApi, notificationsApi, adminWorkersApi, adminBookingsApi, complaintsApi, analyticsApi, welfareApi). Every function goes Screen→hook→services/api/xxxApi.js→apiClient.js→mockApi.js, never skips a layer. Fully implement authApi.js, servicesApi.js, workersApi.js, bookingsApi.js, emergencyApi.js and reviewsApi.js now (the ones customer screens need); leave the rest as typed-looking stubs with a clear TODO and the expected function signature, for the admin/worker work to fill in as those land.
```
**Commit:** `feat(mobile-core): add services/api layer with auth, services, workers, bookings, emergency, reviews implemented`

---

### Prompt 4 — components/common
```
Build components/common/: Header, EmptyState, ErrorState (with retry), LoadingState (skeleton), OfflineBanner (wired to @react-native-community/netinfo, non-blocking), LanguageSwitcher, ScreenWrapper (safe-area + KeyboardAvoidingView + consistent padding), StatusBadge (renders any of the booking/worker/complaint status enums with correct color). These are used by every screen in the app across all 3 roles — make them visually excellent, since a bad EmptyState/ErrorState undermines every screen that uses it.
```
**Commit:** `feat(mobile-core): build shared common components (Header, EmptyState, ErrorState, OfflineBanner, StatusBadge, etc.)`

---

### Prompt 5 — components/forms
```
Build components/forms/: OtpInput (6-digit, auto-advance, used by Auth), AddressForm (manual address entry + GPS-filled state), ScheduleForm (date/time or "Now" picker), RatingForm (stars + text + tags), FilterSheet (a reusable bottom-sheet filter component parameterized by filter config, used by Worker List, Workers Directory, Bookings Monitor, etc.).
```
**Commit:** `feat(mobile-core): build shared form components (OtpInput, AddressForm, ScheduleForm, RatingForm, FilterSheet)`

---

### Prompt 6 — components/charts
```
Build components/charts/ using react-native-svg (or react-native-gifted-charts if it verifiably runs in Expo Go — otherwise fall back to hand-rolled SVG bars/lines and note why): BarChart, LineChart, DonutChart, KpiCard, TrendSparkline. These power Worker Earnings, Admin Fair Distribution, and Admin Analytics — keep them simple, legible on a small screen, theme-token-driven, and genuinely good-looking (this is a differentiator screen for Admin, so the charts can't look like an afterthought).
```
**Commit:** `feat(mobile-core): build shared chart components (BarChart, LineChart, DonutChart, KpiCard, TrendSparkline)`

---

### Prompt 7 — components/worker
```
Build components/worker/: JobRequestCard (service, distance, area, time, price, emergency tag, Accept/Reject buttons, expiry countdown), EarningCard, AvailabilityToggle (large, always-visible, satisfying to tap), WelfareCard. Icon-driven, large touch targets, minimal text — these are for field workers on mid/low-end Android per the design intent.
```
**Commit:** `feat(mobile-worker): build JobRequestCard, EarningCard, AvailabilityToggle and WelfareCard`

---

### Prompt 8 — Worker Home
```
Build screens/worker/Home.js: the AvailabilityToggle front and center, today's summary (jobs, earnings), pending-request badge, a workload/fair-share indicator ("3 jobs this week — you're in line for the next request"), and a shortcut to the active job if one exists. Wire hooks/worker/useAvailability.js and useJobRequests.js.
```
**Commit:** `feat(mobile-worker): build Worker Home screen with availability toggle and fair-share indicator`

---

### Prompt 9 — Job requests
```
Build screens/worker/JobRequests.js: FlatList of JobRequestCard with Accept/Reject actions, a short required reason on reject, and a visible expiry countdown per card. Accepting a job should be reachable in ≤3 taps. Wire hooks/worker/useJobRequests.js.
```
**Commit:** `feat(mobile-worker): build Job Requests screen with accept/reject and expiry countdown`

---

### Prompt 10 — Active job
```
Build screens/worker/ActiveJob.js: step buttons On the way → Started → Completed, navigate-to-customer (maps app via linking.js), call customer, mark cash received. Wire hooks/worker/useActiveJob.js. Confirm destructive/irreversible actions (e.g. marking completed).
```
**Commit:** `feat(mobile-worker): build Active Job screen with status steps and navigate/call actions`

---

### Prompt 11 — Job history & Earnings
```
Build screens/worker/Earnings.js: day/week/month totals using KpiCard/BarChart from components/charts, per-job breakdown list, payment status per job. Wire hooks/worker/useEarnings.js.
```
**Commit:** `feat(mobile-worker): build Job History & Earnings screen with charts`

---

### Prompt 12 — Ratings & reviews, Profile & skills, Welfare card
```
Build screens/worker/Ratings.js (average, distribution, recent comments), screens/worker/ProfileSkills.js (edit skills/experience/service area, upload certificates via imagePicker.js — upload stubbed, OCR is backend-only, show verification status via StatusBadge), and screens/worker/Welfare.js (cooperative name, membership ID, insurance status/coverage, welfare schemes — read-only mock). Wire hooks/worker/useWelfare.js.
```
**Commit:** `feat(mobile-worker): build Ratings, Profile & Skills, and Welfare screens`