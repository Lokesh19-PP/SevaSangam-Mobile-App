# Janhvi — Antigravity Prompt Pack (SevaSangam Mobile)

**You own:** theme/design tokens, `components/ui`, `components/customer`, **Customer dashboard** (`screens/customer`, `hooks/customer`), customer mock data.

**Wait for Ashana's Prompts 1–4** (scaffold, i18n, navigation, AuthContext) to be merged before starting Prompt 1 below — you build inside that skeleton.

Before every prompt: paste `docs/ANTIGRAVITY_MOBILE_CONTEXT.md` as the first message in a new session, then paste the numbered prompt.

---

### Prompt 1 — Theme tokens & NativeWind config
```
Define src/theme/ (colors.js, typography.js, spacing.js, radius.js) mirroring the web SevaSangam design tokens (check frontend/ or docs/design/ if present; otherwise propose a cohesive palette and note the assumption). This app needs to feel EXPRESSIVE and trustworthy, not generic: a confident primary brand color, a distinct accent for the Emergency CTA that reads as urgent-but-not-alarming, clear semantic colors (success/warning/error/info), and a type scale with real hierarchy (display/heading/body/caption). Wire these tokens into tailwind.config.js so NativeWind classes use them. Add a short docs/design/MOBILE_TOKENS.md explaining the palette choices.
```
**Commit:** `feat(mobile-customer): define theme tokens and wire into NativeWind config`

---

### Prompt 2 — Base UI kit
```
Build components/ui/: Button (primary/secondary/ghost/destructive variants, loading state, icon+label support, min 48dp height), Input, Card, Badge, Chip, Avatar, Skeleton, Toast, Modal, Tabs. Every component uses the theme tokens from Prompt 1, supports RN's accessibility props, and has a genuinely polished pressed/disabled/loading visual state — this is the shared vocabulary the whole app is built from, so make it look like a real product's design system, not defaults. Add a small components/ui/UIKitPreview.js dev screen that renders every variant for visual QA (not shipped in nav, just for review).
```
**Commit:** `feat(mobile-customer): build core UI kit (Button, Input, Card, Badge, Chip, Avatar, Skeleton, Toast, Modal, Tabs)`

---

### Prompt 3 — Customer components
```
Build components/customer/: WorkerCard (photo, name, skills, rating, distance, cooperative badge, verified badge, welfare/insurance indicator), ServiceCategoryCard (icon-driven grid item), BookingCard (status-aware styling per booking status enum), EmergencyButton (a visually distinct, always-reachable CTA style — this is the flagship interaction, make it feel immediate and reassuring, not scary). All built on top of components/ui from Prompt 2. No hardcoded strings.
```
**Commit:** `feat(mobile-customer): build WorkerCard, ServiceCategoryCard, BookingCard and EmergencyButton`

---

### Prompt 4 — Customer mock data
```
Create mock/data/ entries needed for the customer flows: services.js (9 categories per section 8: electrician, plumber, carpenter, domestic help, caregiver, driver, gardener, cleaner, technician), workers.js (10-15 workers with full Worker entity shape from the context doc's entity table, varied ratings/distances/availability/cooperatives), bookings.js (a spread across every booking status), reviews.js. Field names must match the entity table exactly. Register these with mock/mockApi.js's expected shape (coordinate with Priti's apiClient.js contract — if it doesn't exist yet, shape the export as a plain array/object for now and leave a TODO comment referencing Priti's mockApi work).
```
**Commit:** `feat(mobile-customer): add customer mock data for services, workers, bookings and reviews`

---

### Prompt 5 — Home screen
```
Build screens/customer/Home.js: greeting, search bar, service category grid (using ServiceCategoryCard), the big Emergency CTA reachable in ≤2 taps, a horizontal "Nearby verified workers" list (WorkerCard), and an active-booking banner when one exists. Loading/empty/error/success states, pull-to-refresh. Wire hooks/customer/useServices.js and useWorkers.js. Make the layout feel alive and inviting — this is the first screen every customer sees, it needs to sell the product in one glance.
```
**Commit:** `feat(mobile-customer): build Home screen with service grid, emergency CTA and nearby workers`

---

### Prompt 6 — Service category / worker list
```
Build screens/customer/WorkerList.js: FlatList (paginated, page/limit/filter params per section 5's golden rules — never .map() inside ScrollView), filters (rating, distance, availability, cooperative) via a filter sheet, sort options, and a "Best match" highlight with a short reason string like "Skilled · Nearby · Available · Fair share" (the reason text comes from the backend mock — coordinate the field name with Yash-Thakur's matching output later). Wire hooks/customer/useWorkers.js with filters/pagination.
```
**Commit:** `feat(mobile-customer): build Worker List screen with filters, sort and best-match highlight`

---

### Prompt 7 — Worker profile screen
```
Build screens/customer/WorkerProfile.js: photo, name, skills, certifications, rating & reviews list, distance, availability, cooperative name + verified badge, welfare/insurance indicator, visit charge, Book and Call actions (Call via services/native/linking.js). Loading/empty/error/success states.
```
**Commit:** `feat(mobile-customer): build Worker Profile screen with trust indicators and book/call actions`

---

### Prompt 8 — Booking flow
```
Build the multi-step booking flow under screens/customer/booking/: service selection → address (GPS auto-fill via services/native/location.js + manual edit) → date/time or "Now" → notes/photos (via imagePicker.js) → price estimate & payment mode (pending/cash only, no gateway) → confirm. Use a shared step-progress UI component. Persist in-progress state in a hook (hooks/customer/useBooking.js) so back-navigation doesn't lose data. Handle GPS-denied gracefully (fall back to manual address entry).
```
**Commit:** `feat(mobile-customer): build multi-step booking flow with GPS address and price estimate`

---

### Prompt 9 — Emergency request
```
Build screens/customer/EmergencyRequest.js: one-tap flow — auto-detect location, pick service type, short description, confirm → "Finding the nearest available worker…" loading state with real personality (not a bare spinner) → assignment result screen. Degrade gracefully to manual address entry if GPS is denied. This must be reachable in ≤2 taps from Home per the design intent — verify that path.
```
**Commit:** `feat(mobile-customer): build Emergency Request flow with auto-location and assignment result`

---

### Prompt 10 — Booking tracking / detail
```
Build screens/customer/BookingDetail.js: status timeline (visual stepper matching the booking status enum), worker card, a mock live map with worker marker + ETA using components/maps (create a MapView wrapper + placeholder fallback if react-native-maps isn't configured yet), contact worker via linking.js, cancel action where the current status allows it.
```
**Commit:** `feat(mobile-customer): build Booking Detail/Tracking screen with status timeline and mock live map`

---

### Prompt 11 — Booking history
```
Build screens/customer/BookingHistory.js: tabs Upcoming / Completed / Cancelled, paginated FlatList using BookingCard, reorder action from a completed booking. Loading/empty/error/success states.
```
**Commit:** `feat(mobile-customer): build Booking History screen with tabs and reorder`

---

### Prompt 12 — Rate & review
```
Build screens/customer/RateReview.js: stars + text + tags, shown after a booking reaches "completed". Wire hooks/customer/useReviews.js.
```
**Commit:** `feat(mobile-customer): build Rate & Review screen`

---

### Prompt 13 — Notifications, Profile, Help
```
Build screens/customer/Profile.js (saved addresses, language switcher, logout) and screens/customer/Help.js (raise a complaint — creates a Complaint entity visible in Ashana's admin Complaints screen; match the field shapes exactly). Notifications screen is shared — confirm it renders correctly for the customer role using Ashana's shared Notifications screen from her Prompt 16 (build a customer-only version now if hers isn't ready yet, and note the TODO to consolidate).
```
**Commit:** `feat(mobile-customer): build Profile and Help/complaint screens`