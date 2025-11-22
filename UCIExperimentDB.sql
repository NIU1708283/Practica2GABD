--------------------------------------------------------
--  File created - divendres-de setembre-20-2019
--------------------------------------------------------
DROP TABLE "DATASET" cascade constraints;
DROP TABLE "SAMPLES" cascade constraints;
--------------------------------------------------------
--  DDL for Table DATASET
--------------------------------------------------------

-- ------------------------------
-- Taula DATASET
-- ------------------------------
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE DATASET CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN
            RAISE;
        END IF;
END;
/

CREATE TABLE DATASET (
    ID          number primary key,
    NAME        VARCHAR2(40),
    FEAT_SIZE   NUMBER,
    NUMCLASSES  NUMBER,
    INFO        JSON
);

-- ------------------------------
-- Taula SAMPLES
-- ------------------------------
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE SAMPLES CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN
            RAISE;
        END IF;
END;
/

CREATE TABLE SAMPLES (
    ID_DATASET  number NOT NULL,
    ID          NUMBER       NOT NULL,
    FEATURES    VECTOR,
    LABEL       VARCHAR2(16),
    CONSTRAINT  SAMPLES_PK PRIMARY KEY (ID_DATASET, ID),
    CONSTRAINT  SAMPLES_FK FOREIGN KEY (id_DATASET)
                REFERENCES DATASET(ID) ON DELETE CASCADE
);
