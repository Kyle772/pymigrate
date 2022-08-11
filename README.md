# Pymigrate - v0.0.1

Takes CSV files and converts them to json using a schema as a structure. Primarily built to assist with wordpress migrations but can easily be expanded to migrate any CSV file to any JSON structure.

Give it a shot!

## Running

Run `pymigrate.convert(migration_source_pathname, schema_pathname, middleware_pathname, delimiter, quotechar)`
OR
Run `pymigrate.convertFiles(["sample", "customers", "products"], delimeter="|", quotechar=",")`

Your converted file in json format will be generated and saved into `/migrated/`

`csv.sample.json`
```
[{"business_name": "Sample Business", "address": {"street": "123 Address st", "city": "San Diego", "state": "CA", "zip": "12312", "country": "United States"}}]
```

## Setting up templates and sources

Put CSV files in `/migration-sources/`

`/migration-sources/sample.csv`
```
ID|Title|Content|Excerpt|Date|"Post Type"|Permalink|URL|Title|Caption|Description|"Alt Text"|Featured|URL|"Store Categories"|_wpas_done_all|custom_page_title|laborator_meta_description|laborator_meta_keywords|laborator_meta_robots_index|laborator_meta_robots_follow|wpsl_address|wpsl_city|wpsl_state|wpsl_zip|wpsl_country|wpsl_country_iso|wpsl_lat|wpsl_lng|wpsl_phone|wpsl_url|_vc_post_settings|slide_template|wpsl_hours|wpsl_email|wpsl_address2|rs_page_bg_color|wpsl_fax|_wp_trash_meta_status|_wp_trash_meta_time|_wp_desired_post_slug|Status|"Author ID"|"Author Username"|"Author Email"|"Author First Name"|"Author Last Name"|Slug|Format|Template|Parent|"Parent Slug"|Order|"Comment Status"|"Ping Status"|"Post Modified Date"
1|"Sample Business"|||"2016-01-07 14:19:38"|wpsl_stores|||sample-business|||||||||||||"123 Address st"|"San Diego"|CA|12312|"United States"|US|00.00|00.00|555-123-1234||"a:2:{s:7:""vc_grid"";a:0:{}s:10:""vc_grid_id"";a:0:{}}"|default|"Monday: 10:00 AM - 7:00 PM
Tuesday: 10:00 AM - 7:00 PM
Wednesday: 10:00 AM - 7:00 PM
Thursday: 10:00 AM - 7:00 PM
Friday: 10:00 AM - 7:00 PM
Saturday: 10:00 AM - 6:00 PM
Sunday: Closed

*Hours subject to change*"|""|||||||publish|1|user|user@user.com|User|Name|sample-business|||0|0|0|closed|closed|"2019-01-24 17:57:29"
```

Put JSON Schemas in `/schemas/`

`/schemas/sample.json`
```
{
    "business_name": "{{ Title }}",
    "address": {
        "street": "{{ wpsl_address }}",
        "city": "{{ wpsl_city }}",
        "state": "{{ wpsl_state }}",
        "zip": "{{ wpsl_zip }}",
        "country": "{{ wpsl_country }}"
    }
}
```

## Creating Middlewares

You can create functions that match column names to cast types or parse values into certain formats. If the module exists for the file and the column name exists as a function it will run on every iteration.

Put Middlewares in `/middleware/`

`/middleware/sample.py`
```
# from flask import current_app as app
# use above import to access app.logger for troubleshooting

# all function names should be in PascalCase
# ie column_name/key = sign uP
#    function name = SignUp
def Title(value):
    value = value.lower().title()
    return value
```

## Quick start
Inside this repo is a docker-compose file that will launch a flask app locally for you to test the converter. I will turn this into a package eventually but it's still under development

# Todo
Get this set up as a package without flask as a requirement

Please submit issues and PRs with feature additions! I will likely only update this for my own use until this gets a following.
