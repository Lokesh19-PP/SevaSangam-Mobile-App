# Ashana — Antigravity Prompt Pack (SevaSangam Mobile)

**You own:** project scaffold, `navigation/*`, Auth screens + `AuthContext`, i18n, `services/native/*`, **Admin dashboard** (`screens/admin`, `components/admin`, `hooks/admin`), admin mock data.

**You are the foundation.** Janhvi and Priti cannot meaningfully start until Prompts 1–4 are merged. Do those first, in order, before anything else.

Before every prompt below: open a new Antigravity session and paste the full contents of `docs/ANTIGRAVITY_MOBILE_CONTEXT.md` as your first message. Then paste the numbered prompt as your task.

---

### Prompt 1 — Expo scaffold + folder structure
```
Scaffold the mobile/ app: Expo blank JavaScript template (no TypeScript), install NativeWind v4 + Tailwind v3 config, react-navigation core deps, react-native-safe-area-context, react-native-screens, expo-secure-store, expo-location, expo-image-picker, expo-notifications, @react-native-community/netinfo, react-native-maps, expo-linking, react-native-svg. Build the full src/ folder structure exactly as listed in section 6 of the context doc (empty folders with .gitkeep where needed). Create app.config.js, App.js (providers + RootNavigator placeholder only), babel.config.js, tailwind.config.js, .env.example with EXPO_PUBLIC_USE_MOCK, EXPO_PUBLIC_API_BASE_URL placeholders and the Android emulator/physical-device networking note as a comment. Set up ESLint + Prettier. Confirm it boots in Expo Go with zero red/yellow screens.
```
**Commit:** `chore(mobile-core): scaffold Expo app, folder structure, NativeWind and lint config`

---

### Prompt 2 — i18n setup
```
Set up src/i18n/index.js with i18next + react-i18next, language persisted via expo-secure-store (or AsyncStorage if simpler — note the choice), instant switching without restart. Create src/i18n/locales/en.json, hi.json, mr.json with empty namespaces: common, auth, customer, worker, admin, errors, status. Populate the common and auth namespaces fully in all 3 languages (buttons like Continue/Back/Retry/Cancel, splash/onboarding copy, login/OTP copy). Missing-key fallback must resolve to English, never show raw keys. Add a LanguageContext.
```
**Commit:** `feat(mobile-core): add i18next setup with en/hi/mr locales and common+auth namespaces`

---

### Prompt 3 — Navigation shells & routes.js
```
Create navigation/routes.js with named route constants for every screen listed in sections 8-10 of the context doc (no magic strings anywhere downstream). Create RootNavigator.js that switches between Auth / Customer / Worker / WorkerAccountStatus / Admin based on AuthContext state (stub the context call for now, return a hardcoded role for testing). Create empty-shell CustomerNavigator.js, WorkerNavigator.js, AdminNavigator.js (bottom tabs matching sections 8/9/10 tab lists) and AuthNavigator.js, each with placeholder screens that just render the screen name in text so navigation is testable end-to-end before real screens exist.
```
**Commit:** `feat(mobile-core): add navigation shells for Auth/Customer/Worker/Admin with role-based RootNavigator`

---

### Prompt 4 — AuthContext + secureStorage wrapper
```
Create src/services/native/secureStorage.js as a thin wrapper around expo-secure-store exposing getToken/setToken/clearToken (never import expo-secure-store anywhere else). Create context/AuthContext.js managing { user, role, token, status, login, logout, restoreSession }, restoring the session from secure storage before the splash screen hides. Wire it into RootNavigator.js from Prompt 3 for real (no more hardcoded role). Admin sessions get a shorter mock token expiry; all context state clears on logout for every role.
```
**Commit:** `feat(mobile-core): add AuthContext and secureStorage wrapper, wire into RootNavigator`

---

### Prompt 5 — Auth screens (Splash → RoleSelect)
```
Build screens/auth/Splash.js, LanguageSelect.js, Onboarding.js (first-launch only, 2-3 swipeable slides), Login.js (phone number input, +91 default), VerifyOtp.js (6-digit OTP input using an OtpInput-style component — a simple local one for now, Priti owns the shared one later; accept "123456" as the mock success code), RoleSelect.js (Customer | Worker only — never show Admin). All copy through t('auth.*'). Make this feel like a polished consumer app: an expressive splash animation (Reanimated/LayoutAnimation is fine, keep it light), clean onboarding illustrations (placeholder SVG is fine), a confident, uncluttered login/OTP flow. Wire into AuthContext.login on OTP success.
```
**Commit:** `feat(mobile-core): build Splash, LanguageSelect, Onboarding, Login, VerifyOtp and RoleSelect screens`

---

### Prompt 6 — WorkerAccountStatus screen
```
Build screens/auth/WorkerAccountStatus.js: shows pending/rejected/suspended state with a clear icon, status-specific message, and reason (from mock worker data) via t('worker.*')/t('status.*'). For pending/rejected, add "Edit profile" and "Re-upload certificates" actions that navigate to worker profile/certificate screens (stub navigation targets — Priti builds the real screens later). This user must never be able to reach WorkerNavigator while in this state; verify RootNavigator enforces that.
```
**Commit:** `feat(mobile-core): add WorkerAccountStatus screen with pending/rejected/suspended states`

---

### Prompt 7 — Native device wrappers
```
Build the remaining src/services/native/ wrappers, each with a real and mock mode behind EXPO_PUBLIC_USE_MOCK (read only via src/config/env.js): location.js (expo-location, foreground only, clear localized permission rationale, graceful denied/services-off handling), imagePicker.js (expo-image-picker, compress before returning, used for profile photo/certificate/complaint photo), notifications.js (expo-notifications — STUB only: register a listener + local-notification mock, no real FCM), linking.js (expo-linking — dial a number, open maps app with lat/lng). Every wrapper returns a well-defined result object even on denial/failure, never throws uncaught.
```
**Commit:** `feat(mobile-core): add native wrappers for location, image picker, notifications stub and linking`

---

### Prompt 8 — Admin Overview
```
Build screens/admin/Overview.js: KPI cards (bookings today, active workers, pending verifications, open complaints, emergency requests, average rating) using Priti's KpiCard component (stub it locally with the same prop shape if she hasn't landed it yet, then swap the import), plus a "Needs attention" list combining unassigned emergency bookings, oldest pending verifications, and escalated complaints, each row deep-linking to its detail list. Implement loading/empty/error/success states and pull-to-refresh. Pull data from a new hooks/admin/useAdminOverview.js hook backed by mock/data (create minimal admin mock data for KPIs if it doesn't exist yet — coordinate the shape with the entity table in the context doc).
```
**Commit:** `feat(mobile-admin): add Admin Overview screen with KPI cards and needs-attention list`

---

### Prompt 9 — Worker verification queue
```
Build screens/admin/VerificationQueue.js (paginated FlatList of pending workers) and screens/admin/VerificationDetail.js: worker profile, skills, cooperative membership, and a CertificateViewer component (components/admin/CertificateViewer.js — zoomable image + mocked OCR result text/confidence). Actions: Approve, Reject (reason required, confirm dialog), Request re-upload. Wire to hooks/admin/useVerificationQueue.js and services/api/adminWorkersApi.js (create the api file with mock-first signatures per section 7's data-flow contract).
```
**Commit:** `feat(mobile-admin): add worker verification queue, detail and CertificateViewer`

---

### Prompt 10 — Workers directory
```
Build screens/admin/WorkersDirectory.js (search + filter sheet: skill, status, cooperative, availability; paginated FlatList, card-based not table) and screens/admin/WorkerDetailAdmin.js (stats, ratings, recent jobs, current workload, insurance status; suspend/reactivate actions with confirm dialogs). Wire hooks/admin/useAdminWorkers.js and extend adminWorkersApi.js.
```
**Commit:** `feat(mobile-admin): add Workers directory and worker detail with suspend/reactivate`

---

### Prompt 11 — Bookings monitor
```
Build screens/admin/BookingsMonitor.js (filters: status, type=emergency, date, service, area; emergency bookings visually highlighted) and screens/admin/BookingDetailAdmin.js (full status timeline, customer/worker cards, the AI match reason text, manual reassign action for unassigned/failed emergencies — mock only). Wire hooks/admin/useAdminBookings.js and services/api/adminBookingsApi.js.
```
**Commit:** `feat(mobile-admin): add Bookings monitor and detail with manual reassign`

---

### Prompt 12 — Fair distribution & utilisation (flagship)
```
Build screens/admin/FairDistribution.js: jobs-per-worker distribution chart, utilisation % (overall / per skill / per cooperative) using Priti's chart components, a fairness gauge/score with a plain-language explanation, and lists of under-utilised and over-loaded workers with a "nudge/flag" mock action. This is the flagship differentiator screen — make it visually the most polished screen in the admin app: clear color coding (fair vs. imbalanced), a confident hero metric, legible on a small phone. All computation is backend-mocked; the device only renders. Wire hooks/admin/useUtilization.js and services/api/analyticsApi.js.
```
**Commit:** `feat(mobile-admin): add Fair Distribution & Utilisation flagship screen`

---

### Prompt 13 — Complaints
```
Build screens/admin/Complaints.js (status tabs: open/in_review/resolved) and screens/admin/ComplaintDetail.js (parties, booking link if present, description, actions: start review, add note, resolve, reject). Wire hooks/admin/useComplaints.js and services/api/complaintsApi.js.
```
**Commit:** `feat(mobile-admin): add Complaints list and detail with review/resolve actions`

---

### Prompt 14 — Analytics & forecast
```
Build screens/admin/AnalyticsForecast.js: demand by service/area/time-of-day, bookings & ratings trends, earnings summary, and the AI demand forecast (next 7 days by category) rendered from the mock backend response, with a date-range picker. Charts must stay simple and legible on a small screen using Priti's chart components. Wire hooks/admin/useAnalytics.js.
```
**Commit:** `feat(mobile-admin): add Analytics & Forecast screen with 7-day AI demand forecast display`

---

### Prompt 15 — Welfare programmes
```
Build screens/admin/WelfarePrograms.js (list with enrolment counts + worker insurance coverage overview) and a create/edit programme flow (title, description, eligibility, status) plus an "announce to workers" mock action. Wire hooks/admin/useWelfarePrograms.js and services/api/welfareApi.js.
```
**Commit:** `feat(mobile-admin): add Welfare Programmes list, create/edit flow and announce action`

---

### Prompt 16 — Admin Notifications/Settings + demo accounts doc
```
Build screens/shared/Notifications.js (works for all 3 roles via a role param) and screens/admin/Settings.js (language, profile, logout). Then write docs/mobile/DEMO_ACCOUNTS.md with 5 mock demo logins: 1 customer, 1 verified worker, 1 pending worker, 1 suspended worker, 1 admin — phone numbers + the fixed OTP code — so any teammate can test every path end-to-end.
```
**Commit:** `feat(mobile-admin): add shared Notifications and Admin Settings; document demo accounts`