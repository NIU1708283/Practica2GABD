-- testUCI
CREATE USER testUCI IDENTIFIED BY "grup06"
        PROFILE perfil_test
        DEFAULT TABLESPACE users
        TEMPORARY TABLESPACE temp
        QUOTA 150M ON users;
    GRANT Test to testUCI;

    
-- GestorUCI
CREATE USER GestorUCI IDENTIFIED BY "grup06"
        PROFILE perfil_gestor
        DEFAULT TABLESPACE users
        TEMPORARY TABLESPACE temp
        QUOTA 500M ON users;
    GRANT Gestor to GestorUCI;