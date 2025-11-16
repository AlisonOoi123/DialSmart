-- Create sequence and trigger for contact_messages table
-- This fixes the ORA-01400 error when inserting contact messages

-- Create sequence for contact_messages ID
CREATE SEQUENCE contact_messages_seq
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

-- Create trigger to auto-populate ID from sequence
CREATE OR REPLACE TRIGGER contact_messages_bi
BEFORE INSERT ON contact_messages
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        SELECT contact_messages_seq.NEXTVAL INTO :NEW.id FROM DUAL;
    END IF;
END;
/

-- Verify the sequence was created
SELECT sequence_name FROM user_sequences WHERE sequence_name = 'CONTACT_MESSAGES_SEQ';

-- Verify the trigger was created
SELECT trigger_name, status FROM user_triggers WHERE trigger_name = 'CONTACT_MESSAGES_BI';
