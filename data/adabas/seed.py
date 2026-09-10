#!/usr/bin/env python3
"""Prepara e confere a massa sintetica do SIFAP, sem conectar a bancos."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
import struct

DATA_DIR = Path(__file__).resolve().parent
REPO_DIR = DATA_DIR.parents[1]
DDM_DIR = REPO_DIR / "01-archaeology/legacy-sifap/adabas-ddms"
DATASETS = {
    "social-program": ("SOCPROG.ddm", 151, "COD-PROGRAM"),
    "beneficiary": ("BENEFIC.ddm", 150, "NUM-REGISTRATION"),
    "payment": ("PAYMENT.ddm", 152, "NUM-PAYMENT"),
    "audit": ("AUDIT.ddm", 153, "NUM-AUDIT"),
}
FIELD_RE = re.compile(
    r"^(M\s+)?([12])\s+([A-Z0-9]{2})\s+([A-Z0-9-]+)\s+"
    r"([ANP])\s+([0-9]+)(?:[,.]([0-9]+))?\s*(.*)$"
)
GROUP_RE = re.compile(r"^([GP])\s+1\s+([A-Z0-9]{2})\s+([A-Z0-9-]+)\s*(.*)$")
Scalar = str
Record = dict[str, Scalar | list[Scalar]]


@dataclass(frozen=True)
class Field:
    code: str
    name: str
    fmt: str
    digits: int
    scale: int
    occurs: int
    offset: int
    periodic: str | None = None
    multiple: bool = False

    @property
    def width(self) -> int:
        return (self.digits + 2) // 2 if self.fmt == "P" else self.digits

    @property
    def repeated(self) -> bool:
        return self.multiple or self.periodic is not None


@dataclass(frozen=True)
class Schema:
    ddm: str
    file_number: int
    fields: tuple[Field, ...]

    @property
    def width(self) -> int:
        return sum(field.width * field.occurs for field in self.fields)


@dataclass
class Snapshot:
    manifest: dict
    schemas: dict[str, Schema]
    records: dict[str, list[Record]]


def occurrences(text: str) -> int:
    match = re.search(r"\(1:([0-9]+)\)", text)
    if not match or not 1 <= int(match[1]) <= 255:
        raise ValueError("DDM: quantidade de ocorrencias ausente ou invalida")
    return int(match[1])


def read_schema(path: Path) -> Schema:
    text = path.read_text(encoding="utf-8")
    identity = re.search(r"DDM NAME:\s+(\w+)", text)
    file_number = re.search(r"FNR:\s+([0-9]+)", text)
    if not identity or not file_number:
        raise ValueError(f"{path.name}: identificacao DDM ausente")
    fields = []
    periodic = None
    repeat = 1
    offset = 0
    for number, line in enumerate(text.splitlines(), 1):
        if "DERIVED DESCRIPTORS" in line or "COLUMN LEGEND" in line:
            break
        line = line.strip()
        if not line or line.startswith("*"):
            continue
        group = GROUP_RE.fullmatch(line)
        field = FIELD_RE.fullmatch(line)
        if group:
            periodic = group[2] if group[1] == "P" else None
            repeat = occurrences(group[4]) if periodic else 1
        elif field:
            multiple, level, code, name, fmt, digits, scale, rest = field.groups()
            if level == "1":
                periodic, repeat = None, 1
            count = occurrences(rest) if multiple else repeat
            item = Field(
                code, name, fmt, int(digits), int(scale or 0), count, offset,
                periodic, bool(multiple),
            )
            if any(old.code == code or old.name == name for old in fields):
                raise ValueError(f"{path.name}:{number}: campo duplicado")
            if multiple and periodic:
                raise ValueError(f"{path.name}:{number}: MU dentro de PE nao suportado")
            fields.append(item)
            offset += item.width * count
        elif fields:
            raise ValueError(f"{path.name}:{number}: linha DDM nao reconhecida")
    if not fields:
        raise ValueError(f"{path.name}: nenhum campo encontrado")
    return Schema(identity[1], int(file_number[1]), tuple(fields))


def encode_scalar(field: Field, value: Scalar) -> bytes:
    if not isinstance(value, str):
        raise ValueError(f"{field.name}: valor deve ser uma string exata")
    if field.fmt == "A":
        if len(value) > field.width or any(not 32 <= ord(char) <= 126 for char in value):
            raise ValueError(f"{field.name}: texto fora do formato ASCII/largura")
        return value.ljust(field.width).encode("ascii")
    if field.fmt == "N":
        if not re.fullmatch(rf"[0-9]{{{field.digits}}}", value):
            raise ValueError(f"{field.name}: numero deve preservar a largura e os zeros")
        return value.encode("ascii")
    if not re.fullmatch(rf"-?[0-9]+\.[0-9]{{{field.scale}}}", value):
        raise ValueError(f"{field.name}: decimal deve preservar a escala {field.scale}")
    amount = Decimal(value)
    scaled = int(amount.copy_abs().scaleb(field.scale))
    digits = str(scaled).zfill(field.digits)
    if len(digits) > field.digits:
        raise ValueError(f"{field.name}: overflow de decimal compactado")
    nibbles = digits + ("D" if amount.is_signed() else "C")
    return bytes.fromhex(nibbles.zfill(field.width * 2))


def decode_scalar(field: Field, raw: bytes) -> Scalar:
    if len(raw) != field.width:
        raise ValueError(f"{field.name}: largura incorreta")
    if field.fmt == "P":
        nibbles = raw.hex().upper()
        digits, sign = nibbles[:-1], nibbles[-1]
        if sign not in {"C", "D", "F"} or not re.fullmatch(r"[0-9]+", digits):
            raise ValueError(f"{field.name}: BCD ou sinal invalido")
        amount = Decimal(("-" if sign == "D" else "") + digits).scaleb(-field.scale)
        value = f"{amount:.{field.scale}f}"
    else:
        value = raw.decode("ascii").rstrip(" ") if field.fmt == "A" else raw.decode("ascii")
    encode_scalar(field, value)
    return value


def encode_record(schema: Schema, record: Record) -> bytes:
    if not isinstance(record, dict) or set(record) != {field.name for field in schema.fields}:
        raise ValueError(f"{schema.ddm}: conjunto de campos incompleto ou desconhecido")
    chunks = []
    for field in schema.fields:
        value = record[field.name]
        values = value if field.repeated else [value]
        if not isinstance(values, list) or len(values) != field.occurs:
            raise ValueError(f"{field.name}: quantidade de ocorrencias incorreta")
        chunks.extend(encode_scalar(field, item) for item in values)
    return b"".join(chunks)


def decode_record(schema: Schema, raw: bytes) -> Record:
    if len(raw) != schema.width:
        raise ValueError(f"{schema.ddm}: largura do registro incorreta")
    result = {}
    for field in schema.fields:
        values = [
            decode_scalar(
                field, raw[field.offset + index * field.width:field.offset + (index + 1) * field.width]
            )
            for index in range(field.occurs)
        ]
        result[field.name] = values if field.repeated else values[0]
    return result


def encode_adacmp(schema: Schema, raw: bytes) -> bytes:
    if len(raw) != schema.width:
        raise ValueError(f"{schema.ddm}: largura do registro incorreta")
    body = bytearray()
    seen_groups = set()
    for field in schema.fields:
        if field.periodic:
            if field.periodic in seen_groups:
                continue
            seen_groups.add(field.periodic)
            members = [item for item in schema.fields if item.periodic == field.periodic]
            body.append(field.occurs)
        else:
            members = [field]
            if field.multiple:
                body.append(field.occurs)
        # O ADACMP recebe PE por ocorrencia, nao todos os valores de um campo juntos.
        for index in range(field.occurs):
            for member in members:
                start = member.offset + index * member.width
                body.extend(raw[start:start + member.width])
    return struct.pack("<I", len(body)) + body


def unique_index(records: list[Record], key: str) -> dict[str, Record]:
    index = {}
    for row in records:
        value = row[key]
        if not isinstance(value, str) or value in index:
            raise ValueError(f"{key}: chave invalida ou duplicada")
        index[value] = row
    return index


def validate_relations(records: dict[str, list[Record]]) -> None:
    for name, (_, _, key) in DATASETS.items():
        unique_index(records[name], key)
    programs = unique_index(records["social-program"], "COD-PROGRAM")
    beneficiaries = unique_index(records["beneficiary"], "NUM-CPF")
    unique_index(records["beneficiary"], "NUM-NIS")
    unique_index(records["beneficiary"], "NUM-BENEFIT")
    for row in beneficiaries.values():
        if row["COD-PROGRAM"] not in programs:
            raise ValueError("beneficiary: programa inexistente")
        if not 0 <= int(row["QTY-DEPEND"]) <= 10:
            raise ValueError("beneficiary: quantidade de dependentes fora do PE")
    for row in records["payment"]:
        beneficiary = beneficiaries.get(row["NUM-CPF"])
        if beneficiary is None:
            raise ValueError("payment: beneficiario inexistente")
        if any(row[key] != beneficiary[key] for key in ["NUM-REGISTRATION", "COD-PROGRAM"]):
            raise ValueError("payment: vinculo de matricula/programa divergente")
    for row in records["audit"]:
        if row["NUM-CPF-AFFECTED"] not in beneficiaries:
            raise ValueError("audit: beneficiario inexistente")


def profile(records: dict[str, list[Record]]) -> dict:
    payments = records["payment"]
    periods = []
    for period in sorted({row["YEAR-MONTH-REF"] for row in payments}):
        rows = [row for row in payments if row["YEAR-MONTH-REF"] == period]
        periods.append({
            "period": period,
            "records": len(rows),
            **{
                field: f"{sum((Decimal(row[field]) for row in rows), Decimal(0)):.2f}"
                for field in ["AMT-GROSS", "AMT-DISC-TOTAL", "AMT-NET"]
            },
        })
    return {
        "records": {name: len(rows) for name, rows in records.items()},
        "periods": periods,
        "beneficiary_status": dict(sorted(Counter(
            row["STAT-BENEFICIARY"] for row in records["beneficiary"]
        ).items())),
        "payment_status": dict(sorted(Counter(row["STAT-PAYMENT"] for row in payments).items())),
        "observed_anomalies": {
            "gross_minus_discount_differs_from_net": sum(
                Decimal(row["AMT-GROSS"]) - Decimal(row["AMT-DISC-TOTAL"]) != Decimal(row["AMT-NET"])
                for row in payments
            ),
            "pending_with_confirmation_date": sum(
                row["STAT-PAYMENT"] == "P" and row["DT-CONFIRMATION"] != "00000000"
                for row in payments
            ),
            "non_reversal_with_origin": sum(
                row["IND-REVERSAL"] == "N" and row["NUM-PAYMENT-ORIGIN"] != "000000000000000"
                for row in payments
            ),
        },
    }


def check_hash(raw: bytes, expected: str, label: str) -> None:
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError(f"{label}: SHA-256 divergente; nao altere a massa silenciosamente")


def load_snapshot(data_dir: Path = DATA_DIR) -> Snapshot:
    manifest = json.loads((data_dir / "manifest.json").read_text(encoding="utf-8"))
    if manifest["version"] != 1 or manifest["synthetic"] is not True:
        raise ValueError("Manifesto: versao ou declaracao de dados sinteticos invalida")
    if set(manifest["datasets"]) != set(DATASETS):
        raise ValueError("Manifesto: os quatro arquivos Adabas sao obrigatorios")
    schemas, records = {}, {}
    for name, (ddm, fnr, key) in DATASETS.items():
        metadata = manifest["datasets"][name]
        ddm_path = DDM_DIR / ddm
        if (
            metadata["file_number"] != fnr or metadata["key"] != key
            or metadata["ddm"] != str(ddm_path.relative_to(REPO_DIR))
        ):
            raise ValueError(f"{name}: identificacao do arquivo no manifesto divergente")
        check_hash(ddm_path.read_bytes(), metadata["ddm_sha256"], ddm)
        schema = read_schema(ddm_path)
        if schema.file_number != fnr or schema.width != metadata["record_bytes"]:
            raise ValueError(f"{name}: FNR ou largura divergente")
        if len(schema.fields) != metadata["fields"]:
            raise ValueError(f"{name}: quantidade de campos divergente")
        raw = (data_dir / "snapshot" / f"{name}.jsonl").read_bytes()
        check_hash(raw, metadata["jsonl_sha256"], name)
        rows = [json.loads(line) for line in raw.decode("utf-8").splitlines()]
        if len(rows) != metadata["records"]:
            raise ValueError(f"{name}: quantidade de registros divergente")
        fixed = b"".join(encode_record(schema, row) + b"\n" for row in rows)
        check_hash(fixed, metadata["fixed_sha256"], f"{name}.dat")
        compressed_input = b"".join(
            encode_adacmp(schema, encode_record(schema, row)) for row in rows
        )
        check_hash(compressed_input, metadata["adacmp_sha256"], f"{name}.cmpin")
        schemas[name], records[name] = schema, rows
    validate_relations(records)
    if profile(records) != manifest["profile"]:
        raise ValueError("Totais ou cenarios do snapshot divergentes")
    return Snapshot(manifest, schemas, records)


def sql_name(value: str) -> str:
    return '"' + value.lower().replace("-", "_") + '"'


def write_postgres(snapshot: Snapshot, directory: Path) -> None:
    load = [
        "\\set ON_ERROR_STOP on", "BEGIN;", "CREATE SCHEMA sifap_seed;",
        "-- Schema existente causa erro: nunca substituir dados ja carregados.",
    ]
    export = ["\\set ON_ERROR_STOP on", "BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY;"]
    for name, (_, _, key) in DATASETS.items():
        schema = snapshot.schemas[name]
        table = "sifap_seed." + sql_name(name)
        definitions = []
        for field in schema.fields:
            sql_type = "jsonb" if field.repeated else ("numeric" if field.fmt == "P" else "text")
            constraint = " PRIMARY KEY" if field.name == key else ""
            if name == "beneficiary" and field.name in {"NUM-CPF", "NUM-NIS", "NUM-BENEFIT"}:
                constraint = " UNIQUE"
            definitions.append(f"  {sql_name(field.name)} {sql_type} NOT NULL{constraint}")
        if name == "beneficiary":
            definitions.extend([
                '  UNIQUE ("num_cpf", "num_registration", "cod_program")',
                '  FOREIGN KEY ("cod_program") REFERENCES sifap_seed."social_program" ("cod_program")',
            ])
        elif name == "payment":
            definitions.append(
                '  FOREIGN KEY ("num_cpf", "num_registration", "cod_program") '
                'REFERENCES sifap_seed."beneficiary" ("num_cpf", "num_registration", "cod_program")'
            )
        elif name == "audit":
            definitions.append(
                '  FOREIGN KEY ("num_cpf_affected") REFERENCES sifap_seed."beneficiary" ("num_cpf")'
            )
        load.append(f"CREATE TABLE {table} (\n" + ",\n".join(definitions) + "\n);")
        load.append(
            f"\\copy {table} FROM '{name}.csv' WITH (FORMAT csv, HEADER true, NULL '\\N')"
        )
        count = len(snapshot.records[name])
        load.append(
            f"DO $$ BEGIN IF (SELECT count(*) FROM {table}) <> {count} THEN "
            f"RAISE EXCEPTION 'Contagem divergente: {name}'; END IF; END $$;"
        )
        columns = ", ".join(f'{sql_name(field.name)} AS "{field.name}"' for field in schema.fields)
        export.append(
            f"\\copy (SELECT {columns} FROM {table} ORDER BY {sql_name(key)}) "
            f"TO 'actual/{name}.csv' WITH (FORMAT csv, HEADER true, NULL '\\N')"
        )
    load.extend(["COMMIT;", "\\echo Carga sintetica concluida no schema sifap_seed."])
    export.extend(["COMMIT;", "\\echo Exportacao de conferencia concluida."])
    (directory / "postgres-load.sql").write_text("\n\n".join(load) + "\n", encoding="utf-8")
    (directory / "postgres-export.sql").write_text("\n\n".join(export) + "\n", encoding="utf-8")


def prepare(snapshot: Snapshot, directory: Path) -> None:
    directory = directory.resolve()
    for protected in [DATA_DIR / "snapshot", DDM_DIR]:
        if directory == DATA_DIR or directory.is_relative_to(protected) or protected.is_relative_to(directory):
            raise ValueError("A pasta de saida nao pode substituir o snapshot ou o corpus")
    directory.mkdir(parents=True, exist_ok=True)
    adabas = directory / "adabas"
    adabas.mkdir(exist_ok=True)
    (directory / "actual").mkdir(exist_ok=True)
    for name, schema in snapshot.schemas.items():
        rows = snapshot.records[name]
        fixed = [encode_record(schema, row) for row in rows]
        (adabas / f"{name}.dat").write_bytes(b"".join(raw + b"\n" for raw in fixed))
        (adabas / f"{name}.cmpin").write_bytes(b"".join(encode_adacmp(schema, raw) for raw in fixed))
        (adabas / f"{name}.cmp").write_text("RECORD_STRUCTURE=E4LENGTH_PREFIX\n", encoding="ascii")
        layout = ["DB FIELD FORMAT DIGITS SCALE OCCURS OFFSET WIDTH"]
        layout.extend(
            f"{field.code} {field.name} {field.fmt} {field.digits} {field.scale} "
            f"{field.occurs} {field.offset} {field.width}"
            for field in schema.fields
        )
        (adabas / f"layout-{name}.txt").write_text("\n".join(layout) + "\n", encoding="ascii")
        with (directory / f"{name}.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=[field.name for field in schema.fields])
            writer.writeheader()
            for row in rows:
                writer.writerow({
                    key: json.dumps(value, separators=(",", ":")) if isinstance(value, list) else value
                    for key, value in row.items()
                })
    write_postgres(snapshot, directory)
    (directory / "summary.json").write_text(
        json.dumps(snapshot.manifest["profile"], indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    hashes = {
        str(path.relative_to(directory)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.iterdir())
        if path.is_file() and path.name in {
            *(f"{name}.csv" for name in DATASETS), "summary.json",
            "postgres-load.sql", "postgres-export.sql",
        }
    }
    hashes.update({
        str(path.relative_to(directory)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(adabas.iterdir()) if path.is_file()
    })
    (directory / "checksums.json").write_text(
        json.dumps(hashes, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def normalize_export(field: Field, value: str) -> Scalar | list[Scalar]:
    def scalar(item: str) -> str:
        if not isinstance(item, str):
            raise ValueError(f"{field.name}: exporte valores como strings")
        if field.fmt == "P":
            try:
                number = Decimal(item)
                rounded = number.quantize(Decimal(1).scaleb(-field.scale))
            except InvalidOperation:
                raise ValueError(f"{field.name}: decimal exportado invalido") from None
            if not number.is_finite() or number != rounded:
                raise ValueError(f"{field.name}: perda de precisao na exportacao")
            return f"{rounded:.{field.scale}f}"
        if field.fmt == "N" and re.fullmatch(r"[0-9]+", item):
            return item.zfill(field.digits)
        return item
    if field.repeated:
        items = json.loads(value)
        if not isinstance(items, list):
            raise ValueError(f"{field.name}: ocorrencias devem ser um array JSON")
        return [scalar(item) for item in items]
    return scalar(value)


def compare(snapshot: Snapshot, directory: Path) -> None:
    for name, (_, _, key) in DATASETS.items():
        schema = snapshot.schemas[name]
        expected = unique_index(snapshot.records[name], key)
        actual = {}
        with (directory / f"{name}.csv").open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            names = [field.name for field in schema.fields]
            if reader.fieldnames is None or sorted(reader.fieldnames) != sorted(names):
                raise ValueError(f"{name}: cabecalho CSV divergente")
            for row_number, row in enumerate(reader, 2):
                if None in row or any(value is None for value in row.values()):
                    raise ValueError(f"{name}:{row_number}: linha CSV incompleta")
                record = {
                    field.name: normalize_export(field, row[field.name]) for field in schema.fields
                }
                encode_record(schema, record)
                identity = record[key]
                if identity in actual:
                    raise ValueError(f"{name}:{row_number}: chave duplicada")
                if identity not in expected:
                    raise ValueError(f"{name}:{row_number}: registro inesperado")
                for field in schema.fields:
                    if record[field.name] != expected[identity][field.name]:
                        raise ValueError(f"{name}:{row_number}: campo divergente: {field.name}")
                actual[identity] = record
        if len(actual) != len(expected):
            raise ValueError(f"{name}: registros ausentes na exportacao")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("verify", help="confere hashes, campos, vinculos e totais")
    prepare_parser = commands.add_parser("prepare", help="gera ADACMP, CSV e SQL, sem executar carga")
    prepare_parser.add_argument("--output", type=Path, default=DATA_DIR / "generated")
    compare_parser = commands.add_parser("compare", help="compara um export com todos os campos da massa")
    compare_parser.add_argument("--actual-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        snapshot = load_snapshot()
        if args.command == "prepare":
            prepare(snapshot, args.output)
        elif args.command == "compare":
            compare(snapshot, args.actual_dir)
    except (OSError, ValueError) as error:
        parser.exit(1, f"ERRO: {error}\n")
    for name, rows in snapshot.records.items():
        print(f"OK {name}: {len(rows)} registros completos")
    print(f"OK {args.command}: nenhum acesso automatico a banco de dados")


if __name__ == "__main__":
    main()
