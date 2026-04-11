# CRE Pipeline Tracker

A multi-user commercial real estate deal pipeline tracker built with React + Supabase.
Supports kanban board and list views, real-time team sync, and full deal tracking across 6 pipeline stages.

---

## Setup: 3 steps (about 10 minutes total)

### Step 1 — Create your Supabase project (free)

1. Go to [supabase.com](https://supabase.com) and sign up / log in
2. Click **New Project**, give it a name (e.g. `cre-pipeline`), set a database password, choose a region
3. Wait ~2 minutes for the project to provision
4. Go to **SQL Editor** (left sidebar) → click **New query**
5. Paste the entire contents of `schema.sql` into the editor and click **Run**
6. Confirm you see a `deals` table under **Table Editor**

**Get your API keys:**
- Go to **Project Settings → API**
- Copy your **Project URL** (looks like `https://xxxx.supabase.co`)
- Copy your **anon public** key

### Step 2 — Configure the app

```bash
# Clone or unzip this project, then:
cd cre-pipeline

# Install dependencies
npm install

# Create your .env file
cp .env.example .env
```

Open `.env` and fill in your Supabase values:

```
VITE_SUPABASE_URL=https://your-project-ref.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

**Test locally:**
```bash
npm run dev
```
Open [http://localhost:5173](http://localhost:5173), create an account, and add a test deal.

### Step 3 — Deploy to Vercel (free, takes 2 minutes)

1. Push this folder to a GitHub repo (or use Vercel CLI)
2. Go to [vercel.com](https://vercel.com) → **New Project** → import your repo
3. In the **Environment Variables** section, add:
   - `VITE_SUPABASE_URL` = your Supabase project URL
   - `VITE_SUPABASE_ANON_KEY` = your Supabase anon key
4. Click **Deploy**
5. Share the Vercel URL with your team

---

## Adding team members

Each person signs up at your deployed URL with their work email. All accounts share the same live pipeline — any deal added, edited, or advanced in stage appears immediately for everyone.

To require email confirmation (recommended):
- Supabase Dashboard → **Authentication → Providers → Email**
- Enable "Confirm email" toggle

---

## Pipeline stages

| Stage | Description |
|-------|-------------|
| Prospecting | Initial outreach / qualification |
| Application / NDA | Borrower has engaged, NDA signed |
| LOI / Term Sheet | LOI or term sheet issued |
| Due Diligence | Lender underwriting in progress |
| Closing | Docs out, closing imminent |
| Funded / Closed | Transaction complete |

---

## Deal fields

| Field | Type | Notes |
|-------|------|-------|
| Borrower Name | Text | Required |
| Property Address | Text | |
| Property Type | Select | Multifamily, Office, Retail, Industrial, etc. |
| Stage | Select | See stages above |
| Loan Amount | Number | Displayed as $M / $K |
| LTV | Number | Percentage |
| DSCR | Number | Decimal (e.g. 1.25) |
| Lender Name | Text | |
| Expected Close Date | Date | |
| Commission / Fee | Number | Displayed as $M / $K |
| Notes / Next Steps | Text | Free-form |

---

## Tech stack

- **Frontend:** React 18 + Vite
- **Styling:** CSS variables + Tailwind CSS
- **Database:** Supabase (Postgres)
- **Auth:** Supabase Auth (email/password)
- **Real-time:** Supabase Realtime (Postgres changes)
- **Hosting:** Vercel (recommended) or any static host

---

## Local development

```bash
npm install       # install dependencies
npm run dev       # start dev server at localhost:5173
npm run build     # production build → dist/
npm run preview   # preview production build locally
```

---

## Customization

**Add a property type:** Edit `src/lib/constants.js` → `PROPERTY_TYPES` array.

**Change pipeline stages:** Edit `STAGES` and `STAGE_COLORS` in `src/lib/constants.js`.
Then update `schema.sql` if redeploying from scratch (the stage column is just a text field, no enum constraint).

**Restrict deal edits to deal creator:** In `schema.sql`, replace the update/delete policies with:
```sql
create policy "Owners can update their deals"
  on deals for update
  using (auth.uid() = created_by);
```

---

## Troubleshooting

**"Missing Supabase environment variables"** — Make sure your `.env` file exists and has both `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` set. Restart the dev server after editing `.env`.

**Can't sign up** — Check Supabase Dashboard → Authentication → Users. If email confirmation is on, check your inbox.

**Deals not saving** — Open browser console for errors. Most common cause: RLS policies not applied. Re-run `schema.sql` in Supabase SQL Editor.

**Real-time not working** — Supabase Dashboard → Database → Replication → confirm `deals` table is in the publication list.
