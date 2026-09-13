-- HOUMBA H initial schema
create extension if not exists pgcrypto;

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  name text not null,
  created_at timestamptz not null default now()
);

create table if not exists public.publications (
  id uuid primary key default gen_random_uuid(),
  author_id uuid not null references public.profiles(id) on delete cascade,
  title text not null,
  description text not null default '',
  category text not null default 'Général',
  cover_url text,
  created_at timestamptz not null default now()
);

create table if not exists public.comments (
  id uuid primary key default gen_random_uuid(),
  publication_id uuid not null references public.publications(id) on delete cascade,
  author_id uuid not null references public.profiles(id) on delete cascade,
  text text not null,
  created_at timestamptz not null default now()
);

create table if not exists public.likes (
  publication_id uuid not null references public.publications(id) on delete cascade,
  user_id uuid not null references public.profiles(id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (publication_id, user_id)
);

alter table public.profiles enable row level security;
alter table public.publications enable row level security;
alter table public.comments enable row level security;
alter table public.likes enable row level security;

do $$ begin
  if not exists (select 1 from pg_policies where policyname='profiles_select' and tablename='profiles') then
    create policy profiles_select on public.profiles for select to authenticated using (true);
  end if;
  if not exists (select 1 from pg_policies where policyname='profiles_insert' and tablename='profiles') then
    create policy profiles_insert on public.profiles for insert to authenticated with check ((select auth.uid()) = id);
  end if;
  if not exists (select 1 from pg_policies where policyname='profiles_update' and tablename='profiles') then
    create policy profiles_update on public.profiles for update to authenticated using ((select auth.uid()) = id) with check ((select auth.uid()) = id);
  end if;
  if not exists (select 1 from pg_policies where policyname='publications_select' and tablename='publications') then
    create policy publications_select on public.publications for select using (true);
  end if;
  if not exists (select 1 from pg_policies where policyname='publications_insert' and tablename='publications') then
    create policy publications_insert on public.publications for insert to authenticated with check ((select auth.uid()) = author_id);
  end if;
  if not exists (select 1 from pg_policies where policyname='publications_update' and tablename='publications') then
    create policy publications_update on public.publications for update to authenticated using ((select auth.uid()) = author_id) with check ((select auth.uid()) = author_id);
  end if;
  if not exists (select 1 from pg_policies where policyname='publications_delete' and tablename='publications') then
    create policy publications_delete on public.publications for delete to authenticated using ((select auth.uid()) = author_id);
  end if;
  if not exists (select 1 from pg_policies where policyname='comments_select' and tablename='comments') then
    create policy comments_select on public.comments for select using (true);
  end if;
  if not exists (select 1 from pg_policies where policyname='comments_insert' and tablename='comments') then
    create policy comments_insert on public.comments for insert to authenticated with check ((select auth.uid()) = author_id);
  end if;
  if not exists (select 1 from pg_policies where policyname='comments_delete' and tablename='comments') then
    create policy comments_delete on public.comments for delete to authenticated using ((select auth.uid()) = author_id);
  end if;
  if not exists (select 1 from pg_policies where policyname='likes_select' and tablename='likes') then
    create policy likes_select on public.likes for select using (true);
  end if;
  if not exists (select 1 from pg_policies where policyname='likes_insert' and tablename='likes') then
    create policy likes_insert on public.likes for insert to authenticated with check ((select auth.uid()) = user_id);
  end if;
  if not exists (select 1 from pg_policies where policyname='likes_delete' and tablename='likes') then
    create policy likes_delete on public.likes for delete to authenticated using ((select auth.uid()) = user_id);
  end if;
end $$;
