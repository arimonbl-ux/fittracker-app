#!/usr/bin/env python3
"""
Cargador TrueCoach → Supabase FitTracker
========================================

USO:
    export SUPABASE_URL='https://byrgpddpmpoffgfegmjk.supabase.co'
    export SUPABASE_SERVICE_KEY='eyJ...'  # service_role key (NO anon)
    export ARIEL_USER_UUID='<uuid_real_de_ariel_en_users_de_supabase>'
    python3 load_to_supabase.py [--dry-run] [--limit N]

Requiere: §15.8 VB del Director (toca data real de producción).

Mapea:
- TrueCoach workouts (1093) → tabla `truecoach_imports_workouts` (nueva, separada de sesiones_entreno)
- TrueCoach items (6978) → tabla `truecoach_imports_items` (nueva)

Por qué tabla nueva (no append a sesiones_entreno):
- Separa data importada (histórica) de data nativa FitTracker (motor adaptativo).
- Permite cruce/auditor sin contaminar el motor R1-R7.
- Permite borrar todo el import sin afectar el resto.

Schema SQL (Supabase Studio → SQL Editor):

    -- Migration 001: TrueCoach imports
    CREATE TABLE IF NOT EXISTS truecoach_imports_workouts (
        id BIGSERIAL PRIMARY KEY,
        user_uuid UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
        ext_workout_id BIGINT UNIQUE NOT NULL,
        ext_client_id BIGINT NOT NULL,
        fecha DATE,
        fecha_full TIMESTAMPTZ,
        titulo TEXT,
        state TEXT,
        state_completed_at TIMESTAMPTZ,
        state_started_at TIMESTAMPTZ,
        created_at_ext TIMESTAMPTZ,
        updated_at_ext TIMESTAMPTZ,
        origen TEXT DEFAULT 'truecoach_import',
        coach_externo TEXT DEFAULT 'howard_hwch_howiecoach',
        items_count INT DEFAULT 0,
        raw_workout JSONB,
        imported_at TIMESTAMPTZ DEFAULT NOW()
    );
    CREATE INDEX idx_truecoach_workouts_user ON truecoach_imports_workouts(user_uuid);
    CREATE INDEX idx_truecoach_workouts_fecha ON truecoach_imports_workouts(fecha);
    CREATE INDEX idx_truecoach_workouts_state ON truecoach_imports_workouts(state);

    CREATE TABLE IF NOT EXISTS truecoach_imports_items (
        id BIGSERIAL PRIMARY KEY,
        workout_id BIGINT REFERENCES truecoach_imports_workouts(id) ON DELETE CASCADE,
        ext_item_id BIGINT UNIQUE NOT NULL,
        ext_workout_id BIGINT NOT NULL,
        name TEXT,
        exercise_id_external BIGINT,
        exercise_canonical_name TEXT,
        exercise_muscles_primary JSONB,
        exercise_muscles_secondary JSONB,
        exercise_type JSONB,
        is_circuit BOOLEAN DEFAULT FALSE,
        position INT,
        state TEXT,
        prescribed_raw_info TEXT,
        prescribed_sets INT,
        prescribed_reps_str TEXT,
        prescribed_pcts_1rm INT[],
        prescribed_rir INT,
        prescribed_rpe REAL,
        prescribed_weights JSONB,
        executed_raw_result TEXT,
        executed_has_result BOOLEAN DEFAULT FALSE,
        has_qualitative_only BOOLEAN DEFAULT FALSE
    );
    CREATE INDEX idx_truecoach_items_workout ON truecoach_imports_items(workout_id);
    CREATE INDEX idx_truecoach_items_name ON truecoach_imports_items(name);

    -- RLS strict (solo el dueño ve sus imports)
    ALTER TABLE truecoach_imports_workouts ENABLE ROW LEVEL SECURITY;
    CREATE POLICY truecoach_workouts_owner ON truecoach_imports_workouts
        FOR ALL TO authenticated USING (user_uuid = auth.uid());
    ALTER TABLE truecoach_imports_items ENABLE ROW LEVEL SECURITY;
    CREATE POLICY truecoach_items_owner ON truecoach_imports_items
        FOR ALL TO authenticated
        USING (EXISTS (SELECT 1 FROM truecoach_imports_workouts w WHERE w.id = workout_id AND w.user_uuid = auth.uid()));

PROTOCOLO DE EJECUCIÓN (§15.8 CAMINO B — toca producción):
1. Director provee SUPABASE_URL, SUPABASE_SERVICE_KEY y ARIEL_USER_UUID.
2. Director crea tablas con SQL arriba en Supabase Studio (revisa schema).
3. Director ejecuta este script con --dry-run primero (no escribe nada, solo cuenta).
4. Director revisa output dry-run y aprueba ejecución real.
5. Director ejecuta sin --dry-run con --limit 10 para verificar (carga 10 workouts).
6. Director revisa en Supabase que data llegó OK.
7. Si OK, Director ejecuta sin límite — carga completa de los 1,093 workouts.
"""

import argparse, json, os, sys
from urllib.parse import urljoin
import urllib.request, urllib.error

EXPORT_DIR = "/Users/arielgbs/Library/CloudStorage/OneDrive-GBSBUSINESSADVICELATAM/_DESPACHO_GBS/_OUT_ATLAS/_TRUECOACH_EXPORT"
MAPPED = f"{EXPORT_DIR}/MAPPED_FITTRACKER_READY.json"

def supabase_request(url, key, method, path, body=None, prefer=None):
    full_url = url.rstrip('/') + path
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    if prefer:
        headers['Prefer'] = prefer
    data = None
    if body is not None:
        data = json.dumps(body).encode('utf-8')
    req = urllib.request.Request(full_url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8')) if resp.length else None
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8') or '{}')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true', help='Solo simular, no escribir')
    p.add_argument('--limit', type=int, default=None, help='Cargar solo N workouts (validación)')
    args = p.parse_args()

    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_SERVICE_KEY')
    user_uuid = os.environ.get('ARIEL_USER_UUID')
    if not (url and key and user_uuid):
        print("❌ FALTAN VARIABLES DE ENTORNO: SUPABASE_URL, SUPABASE_SERVICE_KEY, ARIEL_USER_UUID")
        sys.exit(1)

    with open(MAPPED) as f:
        data = json.load(f)
    workouts = data['workouts']
    if args.limit:
        workouts = workouts[:args.limit]
    print(f"Workouts a procesar: {len(workouts)}")
    print(f"Modo: {'DRY-RUN (sin escritura)' if args.dry_run else 'PRODUCCIÓN'}")
    print()

    if args.dry_run:
        # Solo contar y validar
        total_items = sum(w['items_count'] for w in workouts)
        completed = sum(1 for w in workouts if w['state'] == 'completed')
        with_pct = sum(1 for w in workouts for it in w['items'] if it['prescribed'].get('pcts_1rm'))
        print(f"  Total items a insertar:  {total_items}")
        print(f"  Workouts completados:    {completed}")
        print(f"  Items con %1RM:          {with_pct}")
        print()
        print("✅ Dry-run completado. Para ejecutar real, quitá --dry-run")
        return

    # Verificar conexión Supabase
    print("Verificando conexión Supabase...")
    status, body = supabase_request(url, key, 'GET', '/rest/v1/?apikey=' + key)
    if status not in (200, 400):  # 400 puede pasar en root
        print(f"❌ Error de conexión: HTTP {status}: {body}")
        sys.exit(1)
    print(f"  ✅ Status {status}")
    print()

    # Insert workouts
    print(f"Insertando {len(workouts)} workouts...")
    inserted_workouts = 0
    for i, w in enumerate(workouts):
        record = {
            'user_uuid': user_uuid,
            'ext_workout_id': w['ext_workout_id'],
            'ext_client_id': w['ext_client_id'],
            'fecha': w['fecha'],
            'fecha_full': w['fecha_full'],
            'titulo': w['titulo'],
            'state': w['state'],
            'state_completed_at': w.get('state_completed_at'),
            'state_started_at': w.get('state_started_at'),
            'created_at_ext': w.get('created_at_ext'),
            'updated_at_ext': w.get('updated_at_ext'),
            'origen': w['origen'],
            'coach_externo': w['coach_externo'],
            'items_count': w['items_count'],
            'raw_workout': w,
        }
        status, _ = supabase_request(url, key, 'POST', '/rest/v1/truecoach_imports_workouts',
                                      body=record, prefer='resolution=ignore-duplicates')
        if status in (201, 200, 409):
            inserted_workouts += 1
        else:
            print(f"  ❌ Error workout {w['ext_workout_id']}: HTTP {status}")
        if (i + 1) % 50 == 0:
            print(f"  Progreso: {i+1}/{len(workouts)} workouts insertados")
    print(f"  ✅ {inserted_workouts}/{len(workouts)} workouts ingresados")

    # Insert items
    print(f"\nInsertando items...")
    all_items_records = []
    for w in workouts:
        # Resolver workout_id real en Supabase
        status, body = supabase_request(url, key, 'GET',
                                         f'/rest/v1/truecoach_imports_workouts?ext_workout_id=eq.{w["ext_workout_id"]}&select=id')
        if status == 200 and body:
            workout_supa_id = body[0]['id']
        else:
            continue
        for it in w['items']:
            record = {
                'workout_id': workout_supa_id,
                'ext_item_id': it['ext_item_id'],
                'ext_workout_id': it['ext_workout_id'],
                'name': it['name'],
                'exercise_id_external': it.get('exercise_id_external'),
                'exercise_canonical_name': it.get('exercise_canonical_name'),
                'exercise_muscles_primary': it.get('exercise_muscles_primary'),
                'exercise_muscles_secondary': it.get('exercise_muscles_secondary'),
                'exercise_type': it.get('exercise_type'),
                'is_circuit': it.get('is_circuit'),
                'position': it.get('position'),
                'state': it.get('state'),
                'prescribed_raw_info': it['prescribed'].get('raw_info'),
                'prescribed_sets': it['prescribed'].get('sets'),
                'prescribed_reps_str': it['prescribed'].get('reps_str'),
                'prescribed_pcts_1rm': it['prescribed'].get('pcts_1rm'),
                'prescribed_rir': it['prescribed'].get('rir'),
                'prescribed_rpe': it['prescribed'].get('rpe'),
                'prescribed_weights': it['prescribed'].get('weights'),
                'executed_raw_result': it['executed'].get('raw_result'),
                'executed_has_result': it['executed'].get('has_result'),
                'has_qualitative_only': it.get('has_qualitative_only'),
            }
            all_items_records.append(record)

    # Batch insert items 500 a la vez
    inserted_items = 0
    for i in range(0, len(all_items_records), 500):
        batch = all_items_records[i:i+500]
        status, _ = supabase_request(url, key, 'POST', '/rest/v1/truecoach_imports_items',
                                      body=batch, prefer='resolution=ignore-duplicates')
        if status in (201, 200, 409):
            inserted_items += len(batch)
        else:
            print(f"  ❌ Error batch items {i}: HTTP {status}")
        print(f"  Items: {min(i+500, len(all_items_records))}/{len(all_items_records)}")
    print(f"\n✅ TOTAL: {inserted_workouts} workouts + {inserted_items} items en Supabase")

if __name__ == '__main__':
    main()
