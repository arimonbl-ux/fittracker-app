-- =============================================================
-- Migration 001: TrueCoach imports → FitTracker Supabase
-- =============================================================
-- Fecha: 2026-06-05
-- Autor: ATLAS + Claude Code (autónomo)
-- Aprobado: PENDIENTE VB Director Ariel Montero (§15.8 CAMINO B)
--
-- Diseño:
-- - Tablas SEPARADAS de `sesiones_entreno` (FitTracker nativo)
-- - Cero riesgo a v1 producción (regla D3 INTOCABLE)
-- - RLS estricta por user_uuid
-- - Index para queries del auditor (motor R1-R7 vs Howard)
-- =============================================================

-- 1) Tabla maestra de workouts importados
CREATE TABLE IF NOT EXISTS truecoach_imports_workouts (
    id BIGSERIAL PRIMARY KEY,
    user_uuid UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    ext_workout_id BIGINT UNIQUE NOT NULL,
    ext_client_id BIGINT NOT NULL,
    fecha DATE,
    fecha_full TIMESTAMPTZ,
    titulo TEXT,
    state TEXT,                            -- 'completed', 'missed', 'pending', etc.
    state_completed_at TIMESTAMPTZ,
    state_started_at TIMESTAMPTZ,
    created_at_ext TIMESTAMPTZ,
    updated_at_ext TIMESTAMPTZ,
    origen TEXT DEFAULT 'truecoach_import',
    coach_externo TEXT DEFAULT 'howard_hwch_howiecoach',
    items_count INT DEFAULT 0,
    raw_workout JSONB,                      -- payload completo para auditor
    imported_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_truecoach_workouts_user ON truecoach_imports_workouts(user_uuid);
CREATE INDEX IF NOT EXISTS idx_truecoach_workouts_fecha ON truecoach_imports_workouts(fecha);
CREATE INDEX IF NOT EXISTS idx_truecoach_workouts_state ON truecoach_imports_workouts(state);
CREATE INDEX IF NOT EXISTS idx_truecoach_workouts_origen ON truecoach_imports_workouts(origen);

-- 2) Tabla de items (ejercicios programados por Howard, con sets/reps/RIR/% parseados)
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
    -- Prescribed (lo que Howard programó)
    prescribed_raw_info TEXT,               -- texto crudo de Howard
    prescribed_sets INT,                    -- parseado
    prescribed_reps_str TEXT,
    prescribed_pcts_1rm INT[],
    prescribed_rir INT,                     -- siempre NULL (Howard no usa RIR)
    prescribed_rpe REAL,                    -- siempre NULL
    prescribed_weights JSONB,
    -- Executed (lo que Ariel reportó)
    executed_raw_result TEXT,
    executed_has_result BOOLEAN DEFAULT FALSE,
    -- Audit flag
    has_qualitative_only BOOLEAN DEFAULT FALSE   -- "pesado", "use buen peso" sin métrica
);

CREATE INDEX IF NOT EXISTS idx_truecoach_items_workout ON truecoach_imports_items(workout_id);
CREATE INDEX IF NOT EXISTS idx_truecoach_items_ext_workout ON truecoach_imports_items(ext_workout_id);
CREATE INDEX IF NOT EXISTS idx_truecoach_items_name ON truecoach_imports_items(name);
CREATE INDEX IF NOT EXISTS idx_truecoach_items_qualitative ON truecoach_imports_items(has_qualitative_only) WHERE has_qualitative_only;

-- 3) Vista para análisis científico (avg sets/sem por muscle, Schoenfeld 2017)
CREATE OR REPLACE VIEW v_truecoach_volume_per_muscle_week AS
SELECT
    w.user_uuid,
    DATE_TRUNC('week', w.fecha) AS week_start,
    EXTRACT(YEAR FROM w.fecha) AS year,
    EXTRACT(WEEK FROM w.fecha) AS week_num,
    jsonb_array_elements_text(i.exercise_muscles_primary) AS muscle_primary,
    SUM(COALESCE(i.prescribed_sets, 3)) AS total_sets,
    COUNT(*) AS exercises_count
FROM truecoach_imports_workouts w
JOIN truecoach_imports_items i ON i.workout_id = w.id
WHERE w.state = 'completed'
GROUP BY w.user_uuid, week_start, year, week_num, muscle_primary;

-- 4) RLS estricta — usuario solo ve sus propios datos
ALTER TABLE truecoach_imports_workouts ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS truecoach_workouts_owner ON truecoach_imports_workouts;
CREATE POLICY truecoach_workouts_owner ON truecoach_imports_workouts
    FOR ALL TO authenticated
    USING (user_uuid = auth.uid())
    WITH CHECK (user_uuid = auth.uid());

ALTER TABLE truecoach_imports_items ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS truecoach_items_owner ON truecoach_imports_items;
CREATE POLICY truecoach_items_owner ON truecoach_imports_items
    FOR ALL TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM truecoach_imports_workouts w
            WHERE w.id = workout_id AND w.user_uuid = auth.uid()
        )
    );

-- 5) Comentarios sobre el origen (auditoría)
COMMENT ON TABLE truecoach_imports_workouts IS 'Workouts importados desde TrueCoach (5-jun-2026). NO se conectan al motor adaptativo R1-R7. Sirven para auditor de plan externo y referencia histórica del usuario.';
COMMENT ON TABLE truecoach_imports_items IS 'Items individuales de workouts importados. Parseo de info field (sets/reps/RIR/%/peso) con confianza variable según especificidad de Howard.';

-- =============================================================
-- ROLLBACK (en caso de necesidad)
-- =============================================================
-- DROP VIEW IF EXISTS v_truecoach_volume_per_muscle_week;
-- DROP TABLE IF EXISTS truecoach_imports_items;
-- DROP TABLE IF EXISTS truecoach_imports_workouts;
-- =============================================================
