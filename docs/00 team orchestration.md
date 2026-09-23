# SevaSangam — Team Orchestration & Antigravity Workflow

This file sits alongside the 6 per-member prompt packs:
`Ashana_prompt.md`, `Janhvi_prompt.md`, `Priti_prompt.md`, `Lokesh_prompt.md`, `Yash_prompt.md`, `Yash-Thakur_prompt.md`

Read this first. It tells the team **who works on what, in what order, in what pairs, and how to keep the GitHub history clean.**

---

## 1. The two working groups

| Group | Members | Owns |
| ----- | ------- | ---- |
| **Frontend / Mobile trio** | Ashana, Janhvi, Priti | Everything in `mobile/` (React Native + Expo app) |
| **Backend / Database trio** | Lokesh, Yash, Yash-Thakur | Everything in `backend/` (FastAPI + PostgreSQL/PostGIS + AI) |

Each trio has its own prompt-pack sequence. Within a trio, work is **not** fully parallel from day one — one person lays the foundation, then the other two build on it in parallel.

## 2. Build order (why it isn't a free-for-all)

**Mobile trio:**
1. **Ashana goes first** — Expo scaffold, folder structure, navigation shells, i18n, AuthContext. Nothing else can start until this exists.
2. Once Ashana's Prompts 1–4 are merged, **Janhvi and Priti work in parallel**: Janhvi on theme + UI kit + Customer dashboard, Priti on services/api + mock API + common/forms/charts + Worker dashboard.
3. Ashana continues in parallel on the Admin dashboard, using Priti's chart components and Janhvi's UI kit as they land.

**Backend trio:**
1. **Lokesh goes first** — Docker/Postgres/PostGIS setup and the SQLAlchemy/Pydantic models for every entity. Nothing else can start until schema exists.
2. Once Lokesh's Prompts 1–3 are merged, **Yash and Yash-Thakur work in parallel**: Yash on FastAPI routers/auth/CRUD endpoints, Yash-Thakur on the AI matching/fairness/forecast/OCR modules and Twilio integration.

## 3. Suggested pairs (for review & sync, not exclusive ownership)

Since each trio has 3 people, pairs rotate around whoever's work touches whose:

| Pair | Sync about |
| ---- | ---------- |
| Ashana ↔ Janhvi | Navigation shell wiring into Customer screens |
| Ashana ↔ Priti | Navigation shell wiring into Worker screens + `apiClient.js` usage from screens |
| Lokesh ↔ Yash | Schema ↔ endpoint field-name alignment |
| Lokesh ↔ Yash-Thakur | Schema ↔ AI/matching input alignment (skills, location, workload fields) |
| Priti ↔ Yash | Mobile mock API contract ↔ real FastAPI contract (do this pass before Phase 5 integration) |
| Janhvi ↔ Yash-Thakur | "Best match" reason text shown to customers ↔ actual matching engine output shape |
| Ashana ↔ Yash-Thakur | Admin fairness/forecast screens ↔ analytics endpoint shapes |
| Ashana ↔ Lokesh | Admin data needs (verification queue, complaints) ↔ schema fields |

Run these as short 15–20 min syncs, ideally right before the dependent prompt is started, not after.

## 4. How to use the prompt-pack files

- Every fresh Antigravity session starts by pasting the relevant master context file **verbatim as the first message**:
  - Mobile members (Ashana, Janhvi, Priti) → `docs/ANTIGRAVITY_MOBILE_CONTEXT.md`
  - Backend members (Lokesh, Yash, Yash-Thakur) → `docs/ANTIGRAVITY_CONTEXT.md`
- Then paste **exactly one** numbered prompt from your file as the task message.
- Review the diff, run/test it, fix anything obviously broken, **then commit using the suggested commit message** before moving to the next prompt.
- Don't skip ahead — later prompts assume earlier ones already landed on your branch.
- Merge to your branch often (after every 1–2 prompts) so pairs aren't blocked on stale code.

## 5. The aesthetic mandate (applies to every UI prompt)

Every screen/component prompt for Ashana, Janhvi and Priti carries this instruction baked in:

> Build an **expressive, modern, visually confident UI** — not a bare MVP look. Use the theme tokens deliberately: strong visual hierarchy, generous spacing, purposeful color and elevation, tasteful micro-interactions (press states, subtle transitions), and genuinely well-designed empty/loading/error states — not placeholder gray boxes. This is a hackathon demo that needs to *look* like a funded product, while still respecting the accessibility rules (48dp touch targets, font scaling, low-end Android performance) in the context doc.

## 6. Commit convention

```
type(scope): short, specific description
```

- **Types:** `feat`, `fix`, `chore`, `docs`, `style`, `refactor`
- **Scopes:** `mobile-core`, `mobile-customer`, `mobile-worker`, `mobile-admin`, `api`, `db`, `ai`

Examples:
- `feat(mobile-customer): add Home screen with emergency CTA and nearby worker list`
- `feat(db): add Worker, Certificate and Cooperative models with PostGIS location column`
- `feat(ai): implement scikit-learn matching service with skill+distance+workload scoring`

Each numbered prompt in the per-member files ends with its own ready-to-use commit message — copy it as-is or tighten it once you see the actual diff.

## 7. Weekly sync checklist (each member, each sync)

- [ ] Did any mock data / schema field I added match the entity table in the context doc?
- [ ] Did I log any backend gaps or mismatches in `docs/api/MOBILE_API_REQUESTS.md`?
- [ ] Did I touch only my owned folders (see ownership table in the context doc, section 16)?
- [ ] Did I commit after each prompt (small commits), not one giant end-of-week commit?
- [ ] Did I run the relevant Definition-of-Done checklist (section 19 of the mobile context doc, or your backend equivalent) before calling a prompt "done"?