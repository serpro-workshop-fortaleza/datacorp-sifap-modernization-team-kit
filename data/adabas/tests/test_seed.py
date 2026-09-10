import csv
import hashlib
import json
from pathlib import Path
import shutil
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import seed


class SeedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snapshot = seed.load_snapshot()

    def test_should_include_all_four_complete_files(self):
        expected = {
            "beneficiary": (500, 1739),
            "social-program": (6, 361),
            "payment": (2000, 855),
            "audit": (200, 4995),
        }
        for name, (count, width) in expected.items():
            with self.subTest(dataset=name):
                schema = self.snapshot.schemas[name]
                self.assertEqual(count, len(self.snapshot.records[name]))
                self.assertEqual(width, schema.width)
                fields = {field.name for field in schema.fields}
                for record in self.snapshot.records[name]:
                    self.assertEqual(fields, set(record))

    def test_should_preserve_original_binary_snapshot(self):
        for name, records in self.snapshot.records.items():
            with self.subTest(dataset=name):
                schema = self.snapshot.schemas[name]
                fixed = b""
                for record in records:
                    raw = seed.encode_record(schema, record)
                    self.assertEqual(record, seed.decode_record(schema, raw))
                    fixed += raw + b"\n"
                self.assertEqual(
                    self.snapshot.manifest["datasets"][name]["fixed_sha256"],
                    hashlib.sha256(fixed).hexdigest(),
                )

    def test_should_preserve_maria_and_her_four_pending_payments(self):
        maria = next(
            record for record in self.snapshot.records["beneficiary"]
            if record["NUM-CPF"] == "78933359478"
        )
        self.assertEqual("MARIA MARTINS OLIVEIRA", maria["FULL-NAME"])
        self.assertEqual("28566181479", maria["NUM-NIS"])
        self.assertEqual("PBF1", maria["COD-PROGRAM"])
        self.assertEqual("A", maria["STAT-BENEFICIARY"])
        self.assertEqual("19460612", maria["DT-BIRTH"])
        self.assertEqual("20110524", maria["DT-REGISTRATION"])
        self.assertEqual("FORTALEZA", maria["CITY"])
        self.assertEqual("1000.00", maria["AMT-FAMILY-INCOME"])
        self.assertEqual("00", maria["QTY-DEPEND"])
        payments = [
            record for record in self.snapshot.records["payment"]
            if record["NUM-CPF"] == maria["NUM-CPF"]
        ]
        self.assertEqual(
            ["201710", "201711", "201712", "201801"],
            [record["YEAR-MONTH-REF"] for record in payments],
        )
        for payment in payments:
            self.assertEqual("236.67", payment["AMT-GROSS"])
            self.assertEqual("0.00", payment["AMT-DISC-TOTAL"])
            self.assertEqual("236.67", payment["AMT-NET"])
            self.assertEqual("P", payment["STAT-PAYMENT"])

    def test_should_preserve_leading_zeros_and_all_occurrences(self):
        beneficiaries = self.snapshot.records["beneficiary"]
        self.assertTrue(any(row["NUM-CPF"].startswith("000") for row in beneficiaries))
        self.assertTrue(any(row["QTY-DEPEND"] == "10" for row in beneficiaries))
        for row in beneficiaries:
            self.assertEqual(11, len(row["NUM-NIS"]))
            self.assertEqual(8, len(row["CEP"]))
            self.assertEqual(10, len(row["CPF-DEPEND"]))
            self.assertEqual(10, len(row["NAME-DEPEND"]))
            self.assertEqual(5, len(row["NUM-PHONE"]))
        for row in self.snapshot.records["audit"]:
            self.assertEqual(20, len(row["FIELD-UPDATED-PREV"]))
            self.assertEqual(20, len(row["VALUE-PREV"]))

    def test_should_frame_all_records_and_transpose_periodic_groups(self):
        for name, records in self.snapshot.records.items():
            schema = self.snapshot.schemas[name]
            digest = hashlib.sha256()
            for record in records:
                raw = seed.encode_record(schema, record)
                framed = seed.encode_adacmp(schema, raw)
                digest.update(framed)
                self.assertEqual(len(framed) - 4, struct.unpack("<I", framed[:4])[0])
                offset = 4
                reconstructed = bytearray(schema.width)
                seen_groups = set()
                for field in schema.fields:
                    if field.periodic:
                        if field.periodic in seen_groups:
                            continue
                        seen_groups.add(field.periodic)
                        members = [
                            item for item in schema.fields
                            if item.periodic == field.periodic
                        ]
                        self.assertEqual(field.occurs, framed[offset])
                        offset += 1
                    elif field.multiple:
                        self.assertEqual(field.occurs, framed[offset])
                        offset += 1
                        members = [field]
                    else:
                        members = [field]
                    for occurrence in range(field.occurs):
                        for member in members:
                            start = member.offset + occurrence * member.width
                            reconstructed[start:start + member.width] = framed[
                                offset:offset + member.width
                            ]
                            offset += member.width
                self.assertEqual(len(framed), offset)
                self.assertEqual(raw, bytes(reconstructed))
            self.assertEqual(
                self.snapshot.manifest["datasets"][name]["adacmp_sha256"],
                digest.hexdigest(),
            )

    def test_should_have_valid_check_digits_for_beneficiary_identifiers(self):
        def digit(number, weights):
            remainder = sum(int(char) * weight for char, weight in zip(number, weights)) % 11
            return str(0 if remainder < 2 else 11 - remainder)

        for row in self.snapshot.records["beneficiary"]:
            cpf, nis = row["NUM-CPF"], row["NUM-NIS"]
            self.assertGreater(len(set(cpf)), 1)
            self.assertEqual(cpf[9], digit(cpf[:9], range(10, 1, -1)))
            self.assertEqual(cpf[10], digit(cpf[:10], range(11, 1, -1)))
            self.assertEqual(nis[10], digit(nis[:10], [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]))

    def test_should_reject_invalid_decimal_without_rounding(self):
        schema = self.snapshot.schemas["payment"]
        record = dict(self.snapshot.records["payment"][0])
        for value in ["1.001", "NaN", "Infinity", "10000000.00", 236.67]:
            record["AMT-GROSS"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                seed.encode_record(schema, record)

    def test_should_reject_invalid_packed_digits_and_sign(self):
        schema = self.snapshot.schemas["payment"]
        field = next(item for item in schema.fields if item.name == "AMT-GROSS")
        raw = bytearray(seed.encode_record(schema, self.snapshot.records["payment"][0]))
        raw[field.offset] = 0xA0
        with self.assertRaises(ValueError):
            seed.decode_record(schema, raw)
        raw = bytearray(seed.encode_record(schema, self.snapshot.records["payment"][0]))
        raw[field.offset + field.width - 1] = 0x01
        with self.assertRaises(ValueError):
            seed.decode_record(schema, raw)

    def test_should_reject_missing_extra_or_truncated_fields(self):
        schema = self.snapshot.schemas["beneficiary"]
        original = self.snapshot.records["beneficiary"][0]
        missing = dict(original)
        del missing["CPF-REPRESENTATIVE"]
        extra = dict(original, UNKNOWN="value")
        truncated = dict(original, **{"NAME-DEPEND": []})
        oversized = dict(original, **{"FULL-NAME": "X" * 61})
        for record in [missing, extra, truncated, oversized]:
            with self.assertRaises(ValueError):
                seed.encode_record(schema, record)

    def test_should_reject_orphan_and_mismatched_payment(self):
        for field, value in [
            ("NUM-CPF", "00000000000"),
            ("NUM-REGISTRATION", "00000000000"),
            ("COD-PROGRAM", "NONE"),
        ]:
            records = {name: list(rows) for name, rows in self.snapshot.records.items()}
            records["payment"][0] = dict(records["payment"][0], **{field: value})
            with self.subTest(field=field), self.assertRaises(ValueError):
                seed.validate_relations(records)

    def test_should_detect_modified_snapshot_before_export(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            shutil.copytree(seed.DATA_DIR / "snapshot", target / "snapshot")
            shutil.copyfile(seed.DATA_DIR / "manifest.json", target / "manifest.json")
            path = target / "snapshot" / "beneficiary.jsonl"
            with path.open("ab") as stream:
                stream.write(b"\n")
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                seed.load_snapshot(target)

    def test_should_reject_misleading_file_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            manifest = json.loads((seed.DATA_DIR / "manifest.json").read_text())
            manifest["datasets"]["social-program"]["file_number"] = 150
            (target / "manifest.json").write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, "identificacao"):
                seed.load_snapshot(target)

    def test_should_protect_source_directories_from_generated_output(self):
        for directory in [seed.DATA_DIR, seed.DATA_DIR / "snapshot", seed.REPO_DIR, seed.DDM_DIR]:
            with self.subTest(directory=directory), self.assertRaises(ValueError):
                seed.prepare(self.snapshot, directory)

    def test_should_prepare_deterministic_csv_and_safe_postgres_import(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            seed.prepare(self.snapshot, target)
            before = {
                path.relative_to(target): path.read_bytes()
                for path in target.rglob("*") if path.is_file()
            }
            seed.prepare(self.snapshot, target)
            after = {
                path.relative_to(target): path.read_bytes()
                for path in target.rglob("*") if path.is_file()
            }
            self.assertEqual(before, after)
            seed.compare(self.snapshot, target)
            sql = (target / "postgres-load.sql").read_text()
            self.assertIn("\\set ON_ERROR_STOP on", sql)
            self.assertIn("BEGIN;", sql)
            self.assertIn("CREATE SCHEMA sifap_seed;", sql)
            self.assertIn("COMMIT;", sql)
            self.assertNotIn("DROP ", sql)
            self.assertNotIn("TRUNCATE ", sql)
            self.assertNotIn("ON CONFLICT", sql)
            self.assertNotIn("IF NOT EXISTS", sql)
            self.assertIn("NULL '\\N'", sql)

    def test_should_detect_missing_duplicate_and_changed_export(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            seed.prepare(self.snapshot, target)
            path = target / "payment.csv"
            with path.open(newline="") as stream:
                rows = list(csv.reader(stream))
            for changed in [
                rows[:-1],
                rows + [rows[1]],
                [rows[0]] + [list(row) for row in rows[1:]],
            ]:
                if len(changed) == len(rows):
                    changed[1][rows[0].index("AMT-NET")] = "0.01"
                with path.open("w", newline="") as stream:
                    csv.writer(stream).writerows(changed)
                with self.assertRaises(ValueError):
                    seed.compare(self.snapshot, target)

    def test_should_accept_reordered_records_and_equivalent_numeric_scales(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            seed.prepare(self.snapshot, target)
            path = target / "social-program.csv"
            with path.open(newline="") as stream:
                rows = list(csv.DictReader(stream))
            for row in rows:
                row["AMT-BASE-INDIVIDUAL"] = row["AMT-BASE-INDIVIDUAL"].removesuffix(".00")
                row["COD-REGION"] = json.dumps(json.loads(row["COD-REGION"]))
            with path.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(reversed(rows))
            seed.compare(self.snapshot, target)


if __name__ == "__main__":
    unittest.main()
