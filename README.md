-- 1) Table unique (comptes, réponses, messages, réglages...)
create table if not exists public.conv_rows (
  coll text not null,
  id text not null,
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (coll, id)
);
alter table public.conv_rows enable row level security;

-- 2) Fonctions d'aide (identifiant et rôle de la personne connectée ; NULL si bloquée)
create or replace function public.my_id() returns text
language sql stable security definer set search_path = public as $$
  select r.id from conv_rows r
  where r.coll = 'users' and r.data->>'uid' = auth.uid()::text
    and coalesce((r.data->>'bloque')::boolean, false) = false
  limit 1 $$;

create or replace function public.my_role() returns text
language sql stable security definer set search_path = public as $$
  select r.data->>'role' from conv_rows r
  where r.coll = 'users' and r.data->>'uid' = auth.uid()::text
    and coalesce((r.data->>'bloque')::boolean, false) = false
  limit 1 $$;

-- 3) Qui peut écrire quoi
create or replace function public.can_write(c text, i text, d jsonb) returns boolean
language sql stable security definer set search_path = public as $$
  select coalesce(
    my_role() = 'owner'
    or (my_role() is not null and (
         (c in ('answers','envois') and d->>'u' = my_id())
      or (c = 'prog' and d->>'u' = my_id() and i = my_id())
      or  c = 'logs'
      or (c = 'messages' and (d->>'f' = my_id() or d->>'to' = my_id()
            or (d->>'to' = '@profs'  and my_role() = 'prof')
            or (d->>'to' = '@owners' and my_role() = 'owner')
            or (d->>'to' = '@eleves' and my_role() = 'eleve')))
      or (c = 'cfg' and i = 'emailProf' and my_role() = 'prof')
    )), false) $$;

-- 4) Politiques de sécurité (RLS)
drop policy if exists lecture on public.conv_rows;
drop policy if exists ecriture_ins on public.conv_rows;
drop policy if exists ecriture_upd on public.conv_rows;
drop policy if exists suppression on public.conv_rows;

create policy lecture on public.conv_rows for select to authenticated using (
  my_role() is not null and (
       coll = 'users'
    or (coll = 'cfg' and id in ('settings','emailProf'))
    or (coll = 'cfg' and id = 'codes' and my_role() = 'owner')
    or (coll in ('answers','prog','envois') and (my_role() in ('owner','prof') or data->>'u' = my_id()))
    or (coll = 'logs' and my_role() = 'owner')
    or (coll = 'messages' and (my_role() = 'owner' or data->>'f' = my_id() or data->>'to' = my_id()
          or (data->>'to' = '@profs'  and my_role() = 'prof')
          or (data->>'to' = '@owners' and my_role() = 'owner')
          or (data->>'to' = '@eleves' and my_role() = 'eleve')))
  ));

create policy ecriture_ins on public.conv_rows for insert to authenticated
  with check (can_write(coll, id, data) and (coll <> 'messages' or data->>'f' = my_id() or my_role() = 'owner'));
create policy ecriture_upd on public.conv_rows for update to authenticated
  using (can_write(coll, id, data)) with check (can_write(coll, id, data));
create policy suppression on public.conv_rows for delete to authenticated
  using (my_role() = 'owner');

-- 5) Création du profil à l'inscription (vérifie les codes côté serveur)
create or replace function public.creer_profil(p_id text, p_role text, p_code text) returns void
language plpgsql security definer set search_path = public as $$
declare codes jsonb; st jsonb; ferme boolean;
begin
  if auth.uid() is null then raise exception 'Non connecté.'; end if;
  if p_id is null or length(trim(p_id)) = 0 then raise exception 'Identifiant vide.'; end if;
  if exists (select 1 from conv_rows where coll='users' and data->>'uid' = auth.uid()::text) then
    raise exception 'Ce compte a déjà un profil.'; end if;
  select data into codes from conv_rows where coll='cfg' and id='codes';
  select data into st    from conv_rows where coll='cfg' and id='settings';
  ferme := coalesce((st->>'inscription')::boolean, true) = false;
  if p_role = 'eleve' then
    if ferme and p_code is distinct from codes->>'owner' then raise exception 'Les inscriptions sont fermées.'; end if;
  elsif p_role = 'prof' then
    if p_code is distinct from codes->>'prof' then raise exception 'Code d''accès incorrect.'; end if;
  elsif p_role = 'owner' then
    if p_code is distinct from codes->>'owner' then raise exception 'Code d''accès incorrect.'; end if;
  else raise exception 'Rôle inconnu.'; end if;
  insert into conv_rows(coll, id, data) values ('users', p_id,
    jsonb_build_object('role', p_role, 'date', (extract(epoch from now())*1000)::bigint, 'uid', auth.uid()::text));
end $$;

-- 6) Outils du propriétaire : changer un mot de passe / supprimer un compte
create or replace function public.admin_passwd(p_id text, p_pw text) returns void
language plpgsql security definer set search_path = public, auth, extensions as $$
declare u uuid;
begin
  if my_role() is distinct from 'owner' then raise exception 'Réservé au propriétaire.'; end if;
  select (data->>'uid')::uuid into u from conv_rows where coll='users' and id = p_id;
  if u is null then raise exception 'Compte introuvable.'; end if;
  update auth.users set encrypted_password = crypt(p_pw, gen_salt('bf')) where id = u;
end $$;

create or replace function public.admin_supprimer(p_id text) returns void
language plpgsql security definer set search_path = public, auth as $$
declare u uuid;
begin
  if my_role() is distinct from 'owner' then raise exception 'Réservé au propriétaire.'; end if;
  select (data->>'uid')::uuid into u from conv_rows where coll='users' and id = p_id;
  delete from conv_rows where (coll='users' and id = p_id) or (coll='prog' and id = p_id)
     or (coll in ('answers','envois') and data->>'u' = p_id) or (coll='messages' and data->>'f' = p_id);
  if u is not null then delete from auth.users where id = u; end if;
end $$;

revoke execute on function public.admin_passwd(text,text) from anon;
revoke execute on function public.admin_supprimer(text) from anon;
revoke execute on function public.creer_profil(text,text,text) from anon;

-- 7) Réglages et codes de départ (à changer ensuite dans l'espace propriétaire)
insert into conv_rows(coll, id, data) values
 ('cfg','codes','{"prof":"prof2026","owner":"owner2026"}'),
 ('cfg','settings','{"nbQuotidien":5,"essais":2,"valMax":100,"masse":true,"volume":true,"libre":false,"inscription":true,"maintenance":false,"annonce":""}')
on conflict (coll, id) do nothing;
