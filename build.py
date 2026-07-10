
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET
import bsdiff4

BIN_DIR = Path('bin')
EXT_DIR = Path('ext')
OBJ_DIR = Path('obj')
PROJECT_DIR = Path('.')
SRC_DIR = Path('src')

ORIGINAL_FILENAME = 'Original.nes'

def assemble_file(src_path: Path, obj_path: Path) -> bool:
    print(f"Assembling {src_path}")
    result = subprocess.run([
        str(EXT_DIR / 'ca65'),
        str(src_path),
        '-o', str(obj_path),
        '--bin-include-dir', str(BIN_DIR)
    ])

    if result.returncode != 0:
        print()
        return False
    return True

def assemble_files(src_files, obj_files):
    print("Assemble!")

    # Assemble each file
    for src, obj in zip(src_files, obj_files):
        if not assemble_file(src, obj):
            print(f"Failed to assemble: {src}")
            sys.exit(1)

def check_requirements():
    print("Checking requirements")

    EXT_DIR.mkdir(exist_ok=True)
    OBJ_DIR.mkdir(exist_ok=True)
    BIN_DIR.mkdir(exist_ok=True)

    missing_tools = []
    if not (EXT_DIR / 'ca65.exe').exists():
        missing_tools.append('ca65.exe')
    if not (EXT_DIR / 'ld65.exe').exists():
        missing_tools.append('ld65.exe')
    if not (EXT_DIR / ORIGINAL_FILENAME).exists():
        missing_tools.append(ORIGINAL_FILENAME)

    if missing_tools:
        raise FileNotFoundError(
            f"Missing external files. Ensure ext directory contains: {', '.join(missing_tools)}"
        )

def extract_bins():
    print("Extracting")

    binary_path = EXT_DIR / ORIGINAL_FILENAME
    bin_xml_path = SRC_DIR / 'bins.xml'

    tree = ET.parse(bin_xml_path)
    root = tree.getroot()
    image = binary_path.read_bytes()

    for bin_node in root.findall('./Binary'):
        filename = bin_node.get('FileName')
        if not filename:
            continue

        offset = int(bin_node.get('Offset', '0')) + 16
        length = int(bin_node.get('Length', '0'))

        bin_path = BIN_DIR / filename
        bin_path.parent.mkdir(parents=True, exist_ok=True)

        buf = image[offset:offset+length]
        bin_path.write_bytes(buf)

def link(obj_files):
    print("Linking")

    link_cmd = [
        str(EXT_DIR / 'ld65'),
        '-o', str(BIN_DIR / 'Z.nes'),
        '-Ln', str(BIN_DIR / 'labels.txt'),
        '-C', str(SRC_DIR / 'Z.cfg')
    ] + [str(obj) for obj in obj_files]

    link_result = subprocess.run(link_cmd)
    if link_result.returncode != 0:
        sys.exit(link_result.returncode)
    
def get_exported_labels() -> list[tuple[str, int]]:
    print("Exporting labels")

    labels_path = BIN_DIR / 'labels.txt'
    with labels_path.open('r') as f:
        lines = f.readlines()
    
    labels = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 3 or parts[0] != 'al':
            continue

        label = parts[2]
        is_bank_address = label.startswith(".bank_")
        if not is_bank_address:
            continue

        asm_symbol = label.replace(".bank_", "", 1)[3:]

        bank_num = int(label[6:8], 16)
        addr_pc = int(parts[1], 16)
        addr_pc = 16 + (bank_num * 0x4000) + (addr_pc % 0x4000)

        labels.append((asm_symbol, addr_pc))

    return labels

def write_addresses_file():
    print("Writing addresses")

    out_lines = []
    for (asm_symbol, pc_address) in get_exported_labels():
        out_lines.append(f"{asm_symbol} = 0x{pc_address:X}")

    address_path = PROJECT_DIR / 'Z.py'
    with address_path.open('w') as f:
        f.write('\n'.join(out_lines) + '\n')

def write_diff_file():
    print("Writing bsdiff")

    bsdiff4.file_diff(
        str(EXT_DIR / ORIGINAL_FILENAME), 
        str(BIN_DIR / 'Z.nes'), 
        str(PROJECT_DIR / 'Z.bsdiff'))

def main():
    os.chdir(Path(__file__).resolve().parent)
    check_requirements()
    extract_bins()

    src_files = list(SRC_DIR.glob(f'*.asm'))
    obj_files = [OBJ_DIR / src.with_suffix('.o').name for src in src_files]

    assemble_files(src_files, obj_files)
    link(obj_files)
    write_addresses_file()
    write_diff_file()

    print("Done")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)