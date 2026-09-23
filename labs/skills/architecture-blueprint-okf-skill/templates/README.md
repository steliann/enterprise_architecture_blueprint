# Template Set

`template-registry.yaml` is the authoritative contract for the Architecture Blueprint OKF structure.

For every document type it identifies:

- the Jinja template;
- the JSON Schema for YAML front matter;
- the current document schema version;
- the required headings and their order;
- the collection folder;
- the stable ID prefix;
- the filename pattern.

Change templates, schemas, the registry, migration notes, and tests together. Run `blueprint-okf validate-templates` before releasing a new template-set version.
