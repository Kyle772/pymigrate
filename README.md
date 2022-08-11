# Pymigrate - v0.0.0.1 - stable and working - not easy to use yet

Takes CSV files and converts them to json using a schema as a structure. Primarily built to assist with wordpress migrations but can easily be expanded to migrate any CSV file to any JSON structure.

Give it a shot!

Put CSV files in `/migration-sources/`
Put JSON Schemas in `/schemas/`

Run pymigrate.convert(migration_source_pathname, schema_pathname)

Your converted file in json format will be generated and saved into `/migrated/`

# Todo
Implement Jinja to allow for functions inside of the json tempalate (importing multiple object in one entry for example)

Please submit issues and PRs with feature additions! I will likely only update this for my own use until this gets a following.
