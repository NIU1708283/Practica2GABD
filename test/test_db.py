import time
import unittest
from GABDConnect.oracleConnection import oracleConnection as orcl
from typing import Optional, List, Union
import logging
import sys
import os
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '/test/')))
import re
from pprint import pprint
from utils import (check_esquema, check_datasets, obtain_esquema, draw_esquema, check_rol_user,
                   carrega_funcions_des_de_notebook, get_random_dataset_name, delete_dataset, esborra_dataset_total,
                   es_main_gabd)

from reporting import ReportMeta, ReportBuilder, TestStatus, BuilderOptions, DictRenderOptions, autofill_meta
import inspect

USED_PORTS = set()


table_structure = {
    "DATASET": {
        "columns": {
            "ID":         {"type": "NUMBER", "constraints": ["PK", "NOT NULL"]},
            "NAME":       {"type": "VARCHAR2(20)"},
            "FEAT_SIZE":  {"type": "NUMBER"},
            "NUMCLASSES": {"type": "NUMBER"},
            "INFO":       {"type": "JSON"}
        },
        "constraints": {
            "primary_key": ["ID"]
        }
    },
    "SAMPLES": {
        "columns": {
            "ID_DATASET": {"type": "NUMBER", "constraints": ["NOT NULL", "FK"]},
            "ID":         {"type": "NUMBER", "constraints": ["NOT NULL", "PK"]},
            "FEATURES":   {"type": "VECTOR(256, FLOAT32)"},
            "LABEL":      {"type": "VARCHAR2(16)"}
        },
        "constraints": {
            "primary_key": ["ID_DATASET", "ID"],
            "foreign_keys": {
                "ID_DATASET": {"ref_table": "DATASET", "ref_column": "NAME", "on_delete": "CASCADE"}
            }
        }
    }
}


# meta = ReportMeta(
#     repo_name="acme/vision-model",
#     suite_name="Validació Post-Deploy",
#     author="Oriol Ramos",
#     environment="staging",
#     branch="main",
#     commit="a1b2c3d",
#     header_note="Aquest informe resumeix els tests crítics després del desplegament.",
#     footer_note="Contacte: oriol.ramos@uab.cat",
# )



meta = autofill_meta(
    suite_name="Autoavaluació de la Pràctica 2",
    overrides={
        # Pots sobreescriure el que vulguis:
        # "environment": "staging",
        "header_note": "En aquest informe trobareu els elements crítics de la pràctica.",
        "footer_note": "Contacte: oriol.ramos@uab.cat",
    }
)


options = BuilderOptions(
    dict_render=DictRenderOptions(mode="auto", flatten=True, collapse_section=True),
    show_toc=True,
    show_summary=True,
    show_metrics=True,
    show_links=True,
    show_tags=False,
)

rb = ReportBuilder(meta, options)


class Practica2TestCase(unittest.TestCase):
    def setUp(self):
        # Llegir credencials del workflow si no hi ha fitxer local
        ssh_host = os.environ.get("SSH_HOST", "dcccluster.uab.cat")
        ssh_user = os.environ.get("SSH_USER", "student")
        ssh_port = int(os.environ.get("SSH_PORT", 8192))
        ssh_password = os.environ.get("SSH_PASSWORD", "student")
        grup = os.environ.get("GRUP", "grup00")

        if not es_main_gabd(grup):
            self.ssh_server = {
                'ssh': ssh_host,
                'user': ssh_user,
                'pwd': ssh_password,
                'port': ssh_port
            }
        else:
            self.ssh_server = None

        self.oracle_server = f"oracle-1.{grup}.gabd"
        self.port = 1521
        self.serviceName = "FREEPDB1"
        self.user = "GestorUCI"
        self.pwd = grup

        self.sys_user = "sys"
        self.sys_pwd = "oracle"
        self.mode="SYSDBA"



    def tearDown(self):
        # Aquí alliberes túnels després de cada test
        orcl.close_all_tunnels()
        USED_PORTS.clear()

    def test_user_exists(self):
        """
        Comprovem si els usuaris demanats existeixen a la base de dades i tenen els rols que s'especifica a l'enunciat.
        """

        users = {"GestorUCI": "Gestor" , "TestUCI": "Test"}
        start = time.perf_counter()
        status_for_report = TestStatus.PASS
        status_note = None
        metrics = {}
        metrics['Puntuació'] = 0


        try:
            with orcl(
                user=self.sys_user,
                passwd=self.sys_pwd,
                hostname=self.oracle_server,
                ssh_data=self.ssh_server,
                serviceName=self.serviceName ,
                mode=self.mode
            ) as db:
                for user in users.items():
                    rols_user, hi_es = check_rol_user(db, user[0], user[1])
                    metrics[user[0]] = rols_user  # exemple: guardem-ho com a mètrica
                    metrics['Puntuació'] += 1 if hi_es else 0


            # Cridem el constructor
            db = orcl(
                user=self.user,
                passwd=self.pwd,
                hostname=self.oracle_server,
                ssh_data=self.ssh_server,
                serviceName=self.serviceName #,
            )

            puntuacio_total = 0
            for user in users.items():

                with db.open(user=user[0],passwd=self.pwd) as conn:
                    is_open = bool(getattr(conn, "is_open", False))
                    puntuacio_total += 1 if is_open and hi_es else 0



                    if is_open:
                        print(f"L'usuari {user[0]} existeix a l'Oracle {self.oracle_server}")
                    else:
                        print(
                            f"El usuari {user[0]} no existeix. "
                            f"L'heu de crear abans d'executar aquest notebook"
                        )

                # Asserció del test
                self.assertTrue(is_open, f"L'usuari {user[0]} no existeix a {self.oracle_server}")


        except AssertionError as e:
            status_for_report = TestStatus.FAIL
            status_note = str(e)
            raise  # molt important: re-llançar perquè unittest marqui FAIL
        except Exception as e:
            status_for_report = TestStatus.ERROR
            status_note = f"Excepció: {type(e).__name__}: {e}"
            raise  # re-llança perquè unittest marqui ERROR
        finally:
            duration = time.perf_counter() - start
            metrics['Puntuació Total'] = puntuacio_total / len(users)  # exemple de mètrica addicional
            rb.add_test(
                id="ex_1",
                title="Exercici 1",
                general_text=inspect.getdoc(self.test_user_exists),  # <-- docstring com a text,
                status=status_for_report,
                status_note=status_note or "Connexió OK." if status_for_report == TestStatus.PASS else status_note,
                duration_s=duration,
                metrics=metrics,
                # report=... (si vols adjuntar-hi un dict amb més detall)
            )






    def test_esquema_taules_insert(self):
        """
        Comprovem si les taules tenen l'estructura correcta.
        :return:
        """

        start = time.perf_counter()
        status_for_report = TestStatus.PASS
        status_note = None
        metrics = {}
        metrics['Puntuació'] = 0

        try:
            # Cridem el constructor
            db = orcl(user=self.user, passwd=self.pwd, hostname=self.oracle_server,
                      ssh_data=self.ssh_server, serviceName=self.serviceName)

            with db.open() as conn:
                if conn.is_open:
                    resultat, status = check_esquema(conn, table_structure)
                    pprint(resultat)
                    metrics['Puntuació'] = 0
                else:
                    print(f"Les taules no tenen l'estructura correcta a {self.oracle_server}")

            self.assertEqual(True, status)  # add assertion here

        except AssertionError as e:
            status_for_report = TestStatus.FAIL
            status_note = str(e)
            raise  # molt important: re-llançar perquè unittest marqui FAIL

        except Exception as e:
            status_for_report = TestStatus.ERROR
            status_note = f"Excepció: {type(e).__name__}: {e}"
            raise  # re-llança perquè unittest marqui ERROR

        finally:
            duration = time.perf_counter() - start
            #metrics['Puntuació Total'] = puntuacio_total / len(users)  # exemple de mètrica addicional
            rb.add_test(
                id="ex_2",
                title="Exercici 2",
                general_text=inspect.getdoc(self.test_esquema_taules_insert),  # <-- docstring com a text,
                status=status_for_report,
                status_note=status_note or "Connexió OK." if status_for_report == TestStatus.PASS else status_note,
                duration_s=duration,
                metrics=metrics,
                report= resultat, #... (si vols adjuntar-hi un dict amb més detall)
            )


    def test_datasets(self):
        """
        Comprovem que els datasets indicats a l'enunciat estan correctament inserits a la base de dades. Mirem que les dades del dataset estan a la taula DATASET, que el nombre de mostres és correcte a la taula SAMPLES i que s'han inserit correctament.
        """

        UCI_datasets = [
            (1, 'Iris', 4, 3, {'source': 'UCI', 'url': 'https://archive.ics.uci.edu/ml/datasets/iris'}),
            (2, 'Ionosphere', 34, 2, {'source': 'UCI', 'url': 'https://archive.ics.uci.edu/ml/datasets/ionosphere'}),
            (3, 'Breast Cancer Wisconsin (Diagnostic)', 10, 2, {'source': 'UCI', 'url': 'https://archive.ics.uci.edu/ml/datasets/breast+cancer+wisconsin+(diagnostic)'}),
            (4,'Letter Recognition',16,26,{'source':'UCI','url':'https://archive.ics.uci.edu/ml/datasets/letter+recognition'}),
        ]


        start = time.perf_counter()
        status_for_report = TestStatus.PASS
        status_note = None
        metrics = {}

        try:

            db = orcl(user=self.user, passwd=self.pwd, hostname=self.oracle_server,
                      ssh_data=self.ssh_server, serviceName=self.serviceName)

            with db.open() as db_conn:
                report, status = check_datasets(db_conn, [ds[1] for ds in UCI_datasets])


            # Calculem el score final com a mitja dels scores individuals
            metrics['Puntuació Final'] = sum([item['Score'] for item in report.values()]) / len(report)
            #pprint(report)

            # Assert that all datasets are present
            self.assertEqual(True, status)  # add assertion here

        except AssertionError as e:
            status_for_report = TestStatus.FAIL
            status_note = str(e)
            raise  # molt important: re-llançar perquè unittest marqui FAIL
        except Exception as e:
            status_for_report = TestStatus.ERROR
            status_note = f"Excepció: {type(e).__name__}: {e}"
            raise  # re-llança perquè unittest marqui ERROR
        finally:
            duration = time.perf_counter() - start
            rb.add_test(
                id="ex_2.1",
                title="Exercici 2.1",
                general_text=inspect.getdoc(self.test_datasets),
                status=status_for_report,
                status_note=status_note,
                duration_s=duration,
                metrics=metrics,
                report={'Datasets':UCI_datasets,**report},
                level=2
            )

    def test_estructura_completa_db(self):
        """
        Obtenim totes les taules de la base de dades i comprovem que tenen l'estructura correcta. El resultat de l'analisis el trobareu a la Figura \ref{fig:esquema}.
        :return:
        """

        start = time.perf_counter()
        status_for_report = TestStatus.PASS
        status_note = None
        metrics = {}

        try:

            db = orcl(user=self.user, passwd=self.pwd, hostname=self.oracle_server,
                      ssh_data=self.ssh_server, serviceName=self.serviceName)

            with db.open() as db_conn:
                G = obtain_esquema(db_conn, schema=self.user )
                draw_esquema(G, output_file=f"esquema_{self.user}.png")
                images = {
                    "schema": {"label": "fig:esquema", "path": f"esquema_{self.user}.png",
                               "caption": f"""Esquema de la BD de la UCI per grup {self.user}. Cada node representa una 
                               taula i les fletxes les relacions FK entre elles."""},
                }
                status = True

            self.assertEqual(True, status)  # add assertion here

        except AssertionError as e:
            status_for_report = TestStatus.FAIL
            status_note = str(e)
            raise  # molt important: re-llançar perquè unittest marqui FAIL
        except Exception as e:
            status_for_report = TestStatus.ERROR
            status_note = f"Excepció: {type(e).__name__}: {e}"
            raise  # re-llança perquè unittest marqui ERROR
        finally:
            duration = time.perf_counter() - start
            rb.add_test(
                id="ex_3",
                title="Exercici 3",
                general_text=inspect.getdoc(self.test_estructura_completa_db),
                status=status_for_report,
                status_note=status_note,
                duration_s=duration,
                metrics=metrics,
                images=images
            )


    # Exemple de test
    def test_insert_dataset(self):
        """
        Comprovem que la funció d'inserció del notebook inserData funcioni correctament.
        """



        start = time.perf_counter()
        status_for_report = TestStatus.PASS
        status_note = None
        metrics = {}
        insertVectorDataset, _ = carrega_funcions_des_de_notebook("../src/insertData.ipynb")
        name = "Iris"
        metrics['Puntuació'] = 0
        report = {}

        try:
            db = orcl(user=self.user, passwd=self.pwd, hostname=self.oracle_server,
                      ssh_data=self.ssh_server, serviceName=self.serviceName)

            with db.open() as db_conn:
                name = get_random_dataset_name(db_conn)
                res = insertVectorDataset(db_conn, name)
                report, status_1 = check_datasets(db_conn, name)
                esborrat = delete_dataset(db_conn, name)
                if esborrat:
                    report, status_2 = check_datasets(db_conn, name)
                    if status_2:
                        esborra_dataset_total(db_conn, name)


            self.assertEqual(True, res)  # add assertion here
            metrics['insertVectorDataset'] = 1 if res else 0
            self.assertEqual(True, status_1)  # add assertion here
            metrics[f'Dataset {name}'] = "S'ha inserit correctament" if status_1 else "No s'ha inserit correctament"
            self.assertEqual(False, status_2)  # add assertion here
            metrics[f'Dataset {name} esborrat'] = "S'ha esborrat correctament" if not status_2 else "No s'ha esborrat correctament"
            metrics['Puntuació Final'] = (res + status_1 + (not status_2) )/3.0

        except AssertionError as e:
            status_for_report = TestStatus.FAIL
            status_note = str(e)
            report = {'missatge': f'La funció no ha inserit correctament el dataset {name}.', **report}
            raise  # molt important: re-llançar perquè unittest marqui FAIL

        except Exception as e:
            status_for_report = TestStatus.ERROR
            status_note = f"Excepció: {type(e).__name__}: {e}"
            raise  # re-llança perquè unittest marqui ERROR

        finally:
            duration = time.perf_counter() - start
            rb.add_test(
                id="ex_2.2",
                title="Exercici 2.2",
                general_text=inspect.getdoc(self.test_insert_dataset),
                status=status_for_report,
                status_note=status_note,
                duration_s=duration,
                metrics=metrics,
                report=report,
            )




def tearDownModule():
    rb.set_order_by_ids(["ex_1", "ex_2", "ex_2.1", "ex_3"])
    rb.meta.file_name = f'Avaluacio{os.environ.get("GRUP", "grup00")}'
    rb.to_markdown()
    #print(md)
    rb.save()
    #rb.to_html().save("Avaluacio.html")

    # HTML (amb CSS opcional)
    #css = "body{font-family:system-ui,Segoe UI,Roboto,Helvetica,Arial,sans-serif; max-width: 900px; margin: 2rem auto; line-height:1.5;} h1,h2,h3{margin-top:2rem}"
    #html = rb.to_html(css=css)

    #with open("informe.html", "w", encoding="utf-8") as f:
    #    f.write(html)

    # LaTeX
    # tex = rb.to_latex()

    # PDF (escriu directament al fitxer indicat)
    # pdf_path = rb.to_pdf("informe.pdf", engine="pdflatex", runs=1, keep_tex=True)


if __name__ == '__main__':
    unittest.main()





