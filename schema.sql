-- ============================================================
-- CRE Pipeline Tracker — Supabase Schema
-- Run this entire file in: Supabase Dashboard → SQL Editor
-- ============================================================

-- 1. Create the deals table
create table if not exists deals (
  id                   uuid        default gen_random_uuid() primary key,
  created_at           timestamptz default timezone('utc', now()) not null,
  updated_at           timestamptz default timezone('utc', now()) not null,

  -- Core deal info
  borrower_name        text        not null,
  property_address     text,
  property_type        text,
  stage                text        not null default 'Prospecting',

  -- Financials
  loan_amount          numeric,
  ltv                  numeric,
  dscr                 numeric,
  commission_fee       numeric,

  -- Counterparties
  lender_name          text,

  -- Dates
  expected_close_date  date,

  -- Notes
  notes                text,

  -- Ownership
  created_by           uuid references auth.users(id)
);

-- 2. Enable Row Level Security (required for multi-user)
alter table deals enable row level security;

-- 3. Policies — all authenticated users share the same pipeline
--    (team members all see and can edit all deals)

create policy "Team: view all deals"
  on deals for select
  using (auth.role() = 'authenticated');

create policy "Team: insert deals"
  on deals for insert
  with check (auth.role() = 'authenticated');

create policy "Team: update deals"
  on deals for update
  using (auth.role() = 'authenticated');

create policy "Team: delete deals"
  on deals for delete
  using (auth.role() = 'authenticated');

-- 4. Auto-update updated_at on any row change
create or replace function update_updated_at()
returns trigger as $$
begin
  new.updated_at = timezone('utc', now());
  return new;
end;
$$ language plpgsql;

create trigger deals_updated_at
  before update on deals
  for each row execute function update_updated_at();

-- 5. Helpful index for stage filtering
create index if not exists idx_deals_stage on deals(stage);
create index if not exists idx_deals_created_by on deals(created_by);
create index if not exists idx_deals_expected_close_date on deals(expected_close_date);

-- Done! Your deals table is ready.
