import os
import nbformat
import nbconvert
from traitlets.config import Config


nbdir = 'notebooks'
template_dir = 'templates'
template_name = 'kbpress.tpl'

c = Config()
c.HTMLExporter.preprocessors = [
    'nbconvert.preprocessors.ExecutePreprocessor',
    'nbconvert.preprocessors.ExtractOutputPreprocessor'
]
c.FilesWriter.build_directory = '_build'
c.ExecutePreprocessor.timeout = 600

template_file = os.path.join(template_dir,template_name)

exporter = nbconvert.HTMLExporter(config=c)
writer = nbconvert.writers.FilesWriter(config=c)

exporter.template_file = template_file

for fname in os.listdir(nbdir):
    basename, ext = os.path.splitext(fname)
    if ext.lower() != '.ipynb':
        continue
    nb = nbformat.read(os.path.join(nbdir,fname),nbformat.NO_CONVERT)
    if nb.cells[0].cell_type != 'raw' or 'PUBLISH' not in nb.cells[0].source:
        continue
    # if 'status' not in nb.metadata or nb.metadata.status != 'PUBLISH':
    #     continue
    nb.cells = nb.cells[1:]
    HTML, resources = exporter.from_notebook_node(nb)
    HTML = HTML.replace('.ipynb', '.html')
    writer.write(HTML,resources,basename)

