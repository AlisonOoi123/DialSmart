-- Setup Oracle 11g Auto-Increment using Sequences and Triggers
-- Run this as dialsmart_user

-- Drop existing sequences if they exist (ignore errors if they don't exist)
BEGIN
   EXECUTE IMMEDIATE 'DROP SEQUENCE users_seq';
EXCEPTION
   WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP SEQUENCE brands_seq';
EXCEPTION
   WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP SEQUENCE phones_seq';
EXCEPTION
   WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP SEQUENCE phone_specifications_seq';
EXCEPTION
   WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP SEQUENCE user_preferences_seq';
EXCEPTION
   WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP SEQUENCE recommendations_seq';
EXCEPTION
   WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP SEQUENCE comparisons_seq';
EXCEPTION
   WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP SEQUENCE chat_history_seq';
EXCEPTION
   WHEN OTHERS THEN NULL;
END;
/

-- Create sequences for auto-increment
CREATE SEQUENCE users_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE brands_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE phones_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE phone_specifications_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE user_preferences_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE recommendations_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE comparisons_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE chat_history_seq START WITH 1 INCREMENT BY 1;

-- Drop existing triggers if they exist
BEGIN
   EXECUTE IMMEDIATE 'DROP TRIGGER users_id_trigger';
EXCEPTION
   WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TRIGGER brands_id_trigger';
EXCEPTION
   WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TRIGGER phones_id_trigger';
EXCEPTION
   WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TRIGGER phone_specifications_id_trigger';
EXCEPTION
   WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TRIGGER user_preferences_id_trigger';
EXCEPTION
   WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TRIGGER recommendations_id_trigger';
EXCEPTION
   WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TRIGGER comparisons_id_trigger';
EXCEPTION
   WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TRIGGER chat_history_id_trigger';
EXCEPTION
   WHEN OTHERS THEN NULL;
END;
/

-- Create triggers to auto-populate IDs
CREATE OR REPLACE TRIGGER users_id_trigger
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
  IF :new.id IS NULL THEN
    SELECT users_seq.NEXTVAL INTO :new.id FROM dual;
  END IF;
END;
/

CREATE OR REPLACE TRIGGER brands_id_trigger
BEFORE INSERT ON brands
FOR EACH ROW
BEGIN
  IF :new.id IS NULL THEN
    SELECT brands_seq.NEXTVAL INTO :new.id FROM dual;
  END IF;
END;
/

CREATE OR REPLACE TRIGGER phones_id_trigger
BEFORE INSERT ON phones
FOR EACH ROW
BEGIN
  IF :new.id IS NULL THEN
    SELECT phones_seq.NEXTVAL INTO :new.id FROM dual;
  END IF;
END;
/

CREATE OR REPLACE TRIGGER phone_specifications_id_trigger
BEFORE INSERT ON phone_specifications
FOR EACH ROW
BEGIN
  IF :new.id IS NULL THEN
    SELECT phone_specifications_seq.NEXTVAL INTO :new.id FROM dual;
  END IF;
END;
/

CREATE OR REPLACE TRIGGER user_preferences_id_trigger
BEFORE INSERT ON user_preferences
FOR EACH ROW
BEGIN
  IF :new.id IS NULL THEN
    SELECT user_preferences_seq.NEXTVAL INTO :new.id FROM dual;
  END IF;
END;
/

CREATE OR REPLACE TRIGGER recommendations_id_trigger
BEFORE INSERT ON recommendations
FOR EACH ROW
BEGIN
  IF :new.id IS NULL THEN
    SELECT recommendations_seq.NEXTVAL INTO :new.id FROM dual;
  END IF;
END;
/

CREATE OR REPLACE TRIGGER comparisons_id_trigger
BEFORE INSERT ON comparisons
FOR EACH ROW
BEGIN
  IF :new.id IS NULL THEN
    SELECT comparisons_seq.NEXTVAL INTO :new.id FROM dual;
  END IF;
END;
/

CREATE OR REPLACE TRIGGER chat_history_id_trigger
BEFORE INSERT ON chat_history
FOR EACH ROW
BEGIN
  IF :new.id IS NULL THEN
    SELECT chat_history_seq.NEXTVAL INTO :new.id FROM dual;
  END IF;
END;
/

-- Verify sequences were created
SELECT sequence_name FROM user_sequences;

-- Verify triggers were created
SELECT trigger_name, status FROM user_triggers WHERE trigger_name LIKE '%_ID_TRIGGER';

-- Success message
SELECT 'Oracle 11g sequences and triggers created successfully!' AS status FROM dual;
