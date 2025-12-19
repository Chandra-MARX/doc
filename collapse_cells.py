import argparse
import nbformat as nbf

varser = argparse.ArgumentParser(description='Collapse code cells in a Jupyter notebook by adding "hide-input" tag to code cells without tags.')
varser.add_argument('notebook', type=str, help='Path to the Jupyter notebook file.')
args = varser.parse_args()
notebook = args.notebook

ntbk = nbf.read(notebook, as_version=nbf.NO_CONVERT)
for cell in ntbk.cells:
    cell_tags = cell.get('metadata', {}).get('tags', [])
    if cell['cell_type'] == 'code' and len(cell_tags) == 0:
        cell_tags.append('hide-input')
    if len(cell_tags) > 0:
            cell['metadata']['tags'] = cell_tags

nbf.write(ntbk, notebook)