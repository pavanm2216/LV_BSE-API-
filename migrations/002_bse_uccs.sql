-- Local audit and reconciliation records for UCC onboarding submissions.

CREATE TABLE IF NOT EXISTS bse_uccs (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    request_client_code VARCHAR(50),
    bse_client_code     VARCHAR(50),
    member_code         VARCHAR(50),
    bse_ucc_status      VARCHAR(50),
    submission_status   VARCHAR(20) NOT NULL DEFAULT 'SUBMITTING',
    request_payload     JSONB NOT NULL,
    response_payload    JSONB,
    failure_detail      JSONB,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_bse_uccs_request_client_code ON bse_uccs (request_client_code);
CREATE INDEX IF NOT EXISTS ix_bse_uccs_bse_client_code ON bse_uccs (bse_client_code);

DROP TRIGGER IF EXISTS trg_bse_uccs_updated_at ON bse_uccs;
CREATE TRIGGER trg_bse_uccs_updated_at
BEFORE UPDATE ON bse_uccs
FOR EACH ROW EXECUTE FUNCTION set_updated_at();
