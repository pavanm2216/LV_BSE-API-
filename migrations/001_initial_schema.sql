-- =============================================================================
-- Migration 001 — Initial Schema
-- Phases 1, 3, 4, 5, 6, 7
-- =============================================================================

-- ---------------------------------------------------------------------------
-- Phase 1 — Authentication
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS bse_auth (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    member_code         VARCHAR(50)  NOT NULL,
    username            VARCHAR(255) NOT NULL,
    password_encrypted  TEXT         NOT NULL,
    access_token        TEXT,
    token_expires_at    TIMESTAMPTZ,
    login_status        VARCHAR(20),
    last_login_at       TIMESTAMPTZ,
    created_at          TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bse_api_logs (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    endpoint            VARCHAR(255) NOT NULL,
    http_method         VARCHAR(10)  NOT NULL,
    request_id          VARCHAR(100),
    user_id             UUID,
    bse_status_code     INTEGER,
    response_status     VARCHAR(50),
    error_code          VARCHAR(100),
    error_message       TEXT,
    request_timestamp   TIMESTAMPTZ,
    response_timestamp  TIMESTAMPTZ,
    duration_ms         INTEGER
);

-- ---------------------------------------------------------------------------
-- Phase 3 — Mutual Fund Master
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS bse_amcs (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    amc_code    VARCHAR(50)  NOT NULL UNIQUE,
    amc_name    VARCHAR(255) NOT NULL,
    rta_name    VARCHAR(255),
    status      VARCHAR(30),
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bse_schemes (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scheme_code  VARCHAR(100) NOT NULL UNIQUE,
    amc_id       UUID         NOT NULL REFERENCES bse_amcs(id),
    scheme_name  VARCHAR(500) NOT NULL,
    isin         VARCHAR(50),
    category     VARCHAR(100),
    sub_category VARCHAR(100),
    risk_level   VARCHAR(50),
    status       VARCHAR(30),
    created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bse_scheme_plans (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scheme_id           UUID         NOT NULL REFERENCES bse_schemes(id),
    plan                VARCHAR(50),
    option              VARCHAR(50),
    purchase_allowed    BOOLEAN      NOT NULL DEFAULT FALSE,
    redemption_allowed  BOOLEAN      NOT NULL DEFAULT FALSE,
    switch_allowed      BOOLEAN      NOT NULL DEFAULT FALSE,
    sip_allowed         BOOLEAN      NOT NULL DEFAULT FALSE,
    minimum_purchase    DECIMAL(18,2),
    minimum_sip         DECIMAL(18,2),
    created_at          TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Phase 4 — Investment
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS bse_orders (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id              UUID,
    scheme_id            UUID         REFERENCES bse_schemes(id),
    order_type           VARCHAR(50)  NOT NULL,
    transaction_type     VARCHAR(50)  NOT NULL,
    amount               DECIMAL(18,2),
    units                DECIMAL(18,4),
    folio_number         VARCHAR(100),
    bse_order_id         VARCHAR(100),
    bse_order_number     VARCHAR(100),
    order_status         VARCHAR(50),
    bse_response_code    VARCHAR(50),
    bse_response_message TEXT,
    order_date           TIMESTAMPTZ,
    created_at           TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bse_order_status (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id         UUID        NOT NULL REFERENCES bse_orders(id),
    status           VARCHAR(50) NOT NULL,
    bse_status       VARCHAR(100),
    response_code    VARCHAR(50),
    response_message TEXT,
    checked_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bse_payments (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id             UUID          NOT NULL REFERENCES bse_orders(id),
    user_id              UUID,
    payment_reference    VARCHAR(255),
    bse_payment_id       VARCHAR(100),
    amount               DECIMAL(18,2) NOT NULL,
    payment_method       VARCHAR(50),
    payment_status       VARCHAR(50),
    payment_date         TIMESTAMPTZ,
    response_code        VARCHAR(50),
    response_message     TEXT,
    created_at           TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Phase 5 — SIP
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS bse_sips (
    id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id            UUID,
    scheme_id          UUID          REFERENCES bse_schemes(id),
    amount             DECIMAL(18,2) NOT NULL,
    frequency          VARCHAR(30)   NOT NULL,
    start_date         DATE          NOT NULL,
    end_date           DATE,
    installment_count  INTEGER,
    bse_sip_id         VARCHAR(100),
    status             VARCHAR(50),
    created_at         TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at         TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bse_sip_installments (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sip_id              UUID          NOT NULL REFERENCES bse_sips(id),
    installment_number  INTEGER       NOT NULL,
    due_date            DATE          NOT NULL,
    amount              DECIMAL(18,2) NOT NULL,
    order_id            UUID          REFERENCES bse_orders(id),
    status              VARCHAR(50),
    processed_at        TIMESTAMPTZ,
    created_at          TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    UNIQUE (sip_id, installment_number)
);

-- ---------------------------------------------------------------------------
-- Phase 6 — Transactions
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS bse_transactions (
    id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id            UUID,
    order_id           UUID         REFERENCES bse_orders(id),
    scheme_id          UUID         REFERENCES bse_schemes(id),
    transaction_type   VARCHAR(50)  NOT NULL,
    transaction_date   TIMESTAMPTZ,
    amount             DECIMAL(18,2),
    units              DECIMAL(18,4),
    nav                DECIMAL(18,6),
    bse_transaction_id VARCHAR(100),
    status             VARCHAR(50),
    created_at         TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Phase 7 — Other Transactions
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS bse_redemptions (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id          UUID,
    scheme_id        UUID         REFERENCES bse_schemes(id),
    order_id         UUID         REFERENCES bse_orders(id),
    folio_number     VARCHAR(100),
    redemption_type  VARCHAR(30),
    units            DECIMAL(18,4),
    amount           DECIMAL(18,2),
    bse_order_id     VARCHAR(100),
    status           VARCHAR(50),
    created_at       TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bse_switches (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID,
    from_scheme_id  UUID         REFERENCES bse_schemes(id),
    to_scheme_id    UUID         REFERENCES bse_schemes(id),
    order_id        UUID         REFERENCES bse_orders(id),
    units           DECIMAL(18,4),
    amount          DECIMAL(18,2),
    bse_order_id    VARCHAR(100),
    status          VARCHAR(50),
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- updated_at auto-update trigger
-- ---------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

DO $$
DECLARE
    t TEXT;
BEGIN
    FOREACH t IN ARRAY ARRAY[
        'bse_auth','bse_amcs','bse_schemes','bse_scheme_plans',
        'bse_orders','bse_payments','bse_sips',
        'bse_transactions','bse_redemptions','bse_switches'
    ] LOOP
        EXECUTE format(
            'DROP TRIGGER IF EXISTS trg_%s_updated_at ON %I;
             CREATE TRIGGER trg_%s_updated_at
             BEFORE UPDATE ON %I
             FOR EACH ROW EXECUTE FUNCTION set_updated_at();',
            t, t, t, t
        );
    END LOOP;
END;
$$;
