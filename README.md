# DL4H-Project

---

## Resources
- [MIT-LCP/mimic-code](https://github.com/MIT-LCP/mimic-code) -> MIMIC Code Repository: Code shared by the research community for the MIMIC family of databases
- [MLforHealth/MIMIC_Extract](https://github.com/MLforHealth/MIMIC_Extract) -> A Data Extraction, Preprocessing, and Representation Pipeline for MIMIC-III
- [MIMIC-III Clinical Database](https://physionet.org/content/mimiciii/1.4/) via PhysioNet


## Instructions

### Dependencies
- PostgreSQL
- Conda
- Git

The below steps outline how to successfully build MIMIC-III and run the MIMIC-Extract program. This was tested on a 2021 MacBook Pro with an Apple M1 Max and 64 GB of RAM, using PostgreSQL 13.5.

### 1. Build MIMIC-III

1. Gain access to the MIMIC-III Clinical Database on PhysioNet
	1. Register for an account on the [PhysioNet website](https://physionet.org/), which hosts the MIMIC-III database.
	2. Become a credentialed user on PhysioNet.
	3. [Complete the CITI Program training](https://physionet.org/about/citi-course/) in human subjects research and HIPAA privacy rules.
	4. Sign the data use agreement (DUA) form for the dataset (at the bottom of the MIMIC-III PhsyioNet page).
2. Download the ZIP file for the MIMIC-III Clinical Database (~6.2 GB in size)
3. Clone [mimic-code](https://github.com/MIT-LCP/mimic-code)
4. Configure a new PostgreSQL database with the name  `mimic`
5. Follow the steps in mimic-code to [create MIMIC-III in a local Postgres database](https://github.com/MIT-LCP/mimic-code/blob/main/mimic-iii/buildmimic/postgres/README.md)
	1. Unzip the MIMIC-III database
	2. Open `mimic-code/mimic-iii/buildmimic/postgres/` in Terminal
	3. Run `make create-user mimic-gz datadir="/path/to/mimic/zip/"`
		1. NOTE: This will likely take many (6+) hours to complete
		2. By default, the Makefile uses the following parameters:
			-   Database name: `mimic`
			-   User name: `postgres`
			-   Password: `postgres`
			-   Schema: `mimiciii`
			-   Host: none (defaults to localhost)
			-   Port: none (defaults to 5432)
6. Follow the steps in mimic-code to [generate concepts in PostgreSQL](https://github.com/MIT-LCP/mimic-code/blob/main/mimic-iii/concepts/README.md#generating-the-concepts-in-bigquery)
	1. Change directory to `mimic-code/mimic-iii/concepts_postgres/`
	2. Run `psql -d mimic`
	3. Run `SET search_path TO mimiciii;`
	4. Run `\i postgres-functions.sql`
	5. Run `\i postgres-make-concepts.sql`
	6. Exist the database with `\q`


### 2. Run MIMIC-Extract
1. Clone  [MIMIC_Extract](https://github.com/MLforHealth/MIMIC_Extract)
2. Create the Conda environment (See [updated Conda .yml in atwalsh/MIMIC-Extract](https://github.com/atwalsh/MIMIC_Extract/blob/project-draft/mimic_extract_env_py36.yml))
	1. Open the cloned `MIMIC_Extract/utils/` folder in Terminal
	2. Run `export MACOSX_DEPLOYMENT_TARGET=10.9`
	3. Run `conda env create --force -f ../mimic_extract_env_py36.yml`
	4. Activate the environment with `conda activate mimic_data_extraction`
	5. Install the english language model for spacy: `python -m spacy download en_core_web_sm`
3. Build additional MIMIC-Extract concepts in PostgreSQL
	1. Run `bash postgres_make_extended_concepts.sh`
	2. Run `psql -d mimic`
	3. Run `\i niv-durations.sql`
4. Run the extraction script with `python mimic_direct_extract.py`
	1. Set the `--out-path` parameter to the desired extraction output location
	2. Set the `--pop_size` parameter to set a population size 
