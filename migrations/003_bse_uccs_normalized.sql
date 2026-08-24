-- Migration 003 — Add normalized columns to bse_uccs

ALTER TABLE bse_uccs
    ADD COLUMN IF NOT EXISTS holding_nature       VARCHAR(10),
    ADD COLUMN IF NOT EXISTS tax_status           VARCHAR(10),
    ADD COLUMN IF NOT EXISTS tax_code             VARCHAR(10),
    ADD COLUMN IF NOT EXISTS rdmp_idcw_pay_mode   VARCHAR(10),
    ADD COLUMN IF NOT EXISTS is_client_physical   BOOLEAN,
    ADD COLUMN IF NOT EXISTS is_client_demat      BOOLEAN,
    ADD COLUMN IF NOT EXISTS is_nomination_opted  BOOLEAN,
    ADD COLUMN IF NOT EXISTS comm_mode            VARCHAR(5),
    ADD COLUMN IF NOT EXISTS onboarding           VARCHAR(10),
    ADD COLUMN IF NOT EXISTS is_multi_ucc         BOOLEAN,
    ADD COLUMN IF NOT EXISTS parent_client_code   VARCHAR(50),

    -- Primary holder (holder_rank = 1)
    ADD COLUMN IF NOT EXISTS primary_pan          VARCHAR(20),
    ADD COLUMN IF NOT EXISTS primary_first_name   VARCHAR(100),
    ADD COLUMN IF NOT EXISTS primary_last_name    VARCHAR(100),
    ADD COLUMN IF NOT EXISTS primary_dob          VARCHAR(20),
    ADD COLUMN IF NOT EXISTS primary_gender       VARCHAR(5),
    ADD COLUMN IF NOT EXISTS primary_email        VARCHAR(255),
    ADD COLUMN IF NOT EXISTS primary_mobile       VARCHAR(20),
    ADD COLUMN IF NOT EXISTS kyc_type             VARCHAR(10),

    -- Communication address
    ADD COLUMN IF NOT EXISTS comm_address_line_1  VARCHAR(255),
    ADD COLUMN IF NOT EXISTS comm_city            VARCHAR(100),
    ADD COLUMN IF NOT EXISTS comm_state           VARCHAR(100),
    ADD COLUMN IF NOT EXISTS comm_postalcode      VARCHAR(20),
    ADD COLUMN IF NOT EXISTS comm_country         VARCHAR(100),

    -- Primary bank account
    ADD COLUMN IF NOT EXISTS bank_ifsc            VARCHAR(20),
    ADD COLUMN IF NOT EXISTS bank_acc_num         VARCHAR(50),
    ADD COLUMN IF NOT EXISTS bank_acc_type        VARCHAR(10);

CREATE INDEX IF NOT EXISTS ix_bse_uccs_primary_pan ON bse_uccs (primary_pan);
