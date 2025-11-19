-- Migration: Create audit_logs table
-- Date: 2025-11-19
-- Description: Creates audit log table for tracking admin actions

-- Create audit_logs table
CREATE TABLE audit_logs (
    id NUMBER(10) NOT NULL,
    user_id NUMBER(10),
    target_user_id NUMBER(10),
    action_type VARCHAR2(100) NOT NULL,
    description CLOB,
    ip_address VARCHAR2(50),
    user_agent VARCHAR2(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    extra_data CLOB,
    CONSTRAINT pk_audit_logs PRIMARY KEY (id),
    CONSTRAINT fk_audit_logs_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_audit_logs_target_user FOREIGN KEY (target_user_id) REFERENCES users(id)
);

-- Create sequence for auto-increment ID
CREATE SEQUENCE audit_logs_seq START WITH 1 INCREMENT BY 1;

-- Create trigger for auto-increment
CREATE OR REPLACE TRIGGER audit_logs_bir
BEFORE INSERT ON audit_logs
FOR EACH ROW
BEGIN
    IF :new.id IS NULL THEN
        SELECT audit_logs_seq.NEXTVAL INTO :new.id FROM dual;
    END IF;
END;
/

-- Create index on created_at for faster queries
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);

-- Create index on user_id for faster queries
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);

-- Add comments for documentation
COMMENT ON TABLE audit_logs IS 'Audit log for tracking admin and important user actions';
COMMENT ON COLUMN audit_logs.user_id IS 'Who performed the action';
COMMENT ON COLUMN audit_logs.target_user_id IS 'Who was affected by the action';
COMMENT ON COLUMN audit_logs.action_type IS 'Type of action (e.g., admin_created, password_changed)';
COMMENT ON COLUMN audit_logs.extra_data IS 'Additional data stored as JSON';

COMMIT;
