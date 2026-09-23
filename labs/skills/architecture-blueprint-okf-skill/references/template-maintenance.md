# Template Maintenance

Templates are the contract for public blueprint documents. JSON Schemas define front-matter structure, while `template-registry.yaml` defines paths, ID patterns, filenames, required headings, and ordering.

## Change procedure

1. Change the Jinja template.
2. Change the matching JSON Schema.
3. Change registry headings or relationship metadata.
4. Bump the document `schema_version`.
5. Bump `template_set_version` for cross-document contract changes.
6. Add a migration note.
7. Update or add tests.
8. Validate the synthetic example.

Automatic migration may add metadata or missing sections. It must not delete or reinterpret customer content.
